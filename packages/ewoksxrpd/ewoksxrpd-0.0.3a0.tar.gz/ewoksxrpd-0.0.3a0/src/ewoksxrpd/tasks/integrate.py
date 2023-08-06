import os
import json
from contextlib import contextmanager
from numbers import Number
from typing import Optional

import numpy
import h5py
import pyFAI
from silx.io import h5py_utils
from ewokscore import Task
from ewoksdata.data import bliss
from ewoksdata.data import nexus
from ewoksdata.data.hdf5.dataset_writer import DatasetWriter

from .worker import persistent_worker
from .utils import xrpd_utils
from .utils import data_utils


__all__ = ["Integrate1D", "IntegrateBlissScan"]


class _BaseIntegrate(
    Task,
    input_names=["detector", "geometry", "energy"],
    optional_input_names=["mask", "integration_options", "worker_options"],
    register=False,
):
    """The intensity will be normalized to the reference:

    .. code:

        Inorm = I / monitor * reference
    """

    @contextmanager
    def _worker(self):
        worker_options = self._get_worker_options()
        integration_options = self._get_integration_config()
        with persistent_worker(worker_options, integration_options) as worker:
            yield worker, integration_options

    def _get_integration_config(self) -> dict:
        geometry = data_utils.data_from_storage(self.inputs.geometry)
        xrpd_utils.validate_geometry(geometry)
        integration_options = self.inputs.integration_options
        if integration_options:
            config = {**integration_options, **geometry}
        else:
            config = dict(geometry)
        config.setdefault("unit", "2th_deg")
        config["detector"] = data_utils.data_from_storage(self.inputs.detector)
        config["wavelength"] = xrpd_utils.energy_wavelength(self.inputs.energy)
        if not self.missing_inputs.mask and self.inputs.mask is not None:
            config["mask"] = bliss.get_image(
                data_utils.data_from_storage(self.inputs.mask)
            )
        return config

    def _get_worker_options(self) -> dict:
        if self.inputs.worker_options:
            return data_utils.data_from_storage(self.inputs.worker_options)
        return dict()


class Integrate1D(
    _BaseIntegrate,
    input_names=["image"],
    optional_input_names=["monitor", "reference"],
    output_names=["x", "y", "yerror", "xunits", "info"],
):
    """1D integrate a single diffraction pattern.

    The intensity will be normalized to the reference:

    .. code:

        Inorm = I / monitor * reference
    """

    def run(self):
        raw_data = bliss.get_image(self.inputs.image)
        normalization_factor, monitor, reference = self.get_normalization()

        with self._worker() as (worker, config):
            result = worker.process(raw_data, normalization_factor=normalization_factor)

            self.outputs.x = result.radial
            self.outputs.y = result.intensity
            if result.sigma is None:
                self.outputs.yerror = numpy.full_like(self.outputs.y, numpy.nan)
            else:
                self.outputs.yerror = result.sigma
            self.outputs.xunits = result.unit.name

            info = {
                "detector": config["detector"],
                "energy": xrpd_utils.energy_wavelength(config["wavelength"]),
                "geometry": {
                    k: config[k]
                    for k in ["dist", "poni1", "poni2", "rot1", "rot2", "rot3"]
                },
            }
            info["monitor"] = monitor
            info["reference"] = reference
            self.outputs.info = info

    def get_normalization(self) -> tuple:
        # Inorm = I / normalization_factor
        monitor = self.inputs.monitor
        reference = self.inputs.reference
        if data_utils.is_data(reference):
            if not data_utils.is_data(monitor):
                raise ValueError("provide a 'monitor' when providing a 'reference'")
            monitor = bliss.get_data(monitor)
            reference = bliss.get_data(reference)
            normalization_factor = monitor / reference
        else:
            if data_utils.is_data(monitor):
                monitor = bliss.get_data(monitor)
            else:
                monitor = float("nan")
            reference = float("nan")
            normalization_factor = None
        return normalization_factor, monitor, reference


class IntegrateBlissScan(
    _BaseIntegrate,
    input_names=["filename", "scan", "detector_name", "output_filename"],
    optional_input_names=[
        "counter_names",
        "monitor_name",
        "reference",
        "subscan",
        "retry_timeout",
        "retry_period",
        "demo",
    ],
):
    """1D or 2D integrate data from one detector of a single Bliss scan.

    The intensity will be normalized to the reference:

    .. code:

        Inorm = I / monitor * reference
    """

    def run(self):
        with self._worker() as (worker, config):
            if self.inputs.counter_names:
                counter_names = list(self.inputs.counter_names)
            else:
                counter_names = list()
            detector_name = self.inputs.detector_name
            monitor_name = self.get_input_value("monitor_name", None)
            if monitor_name and monitor_name not in counter_names:
                counter_names.append(monitor_name)
            reference = self.get_input_value("reference", None)
            reference_name = None
            if isinstance(reference, str):
                reference_name = reference
                if reference not in counter_names:
                    counter_names.append(reference)
            retry_timeout = self.get_input_value("retry_timeout", None)
            retry_period = self.get_input_value("retry_period", 0.5)
            subscan = self.get_input_value("subscan", None)

            with self.output_context() as outentry:
                outentry[f"{self._nxprocess_name}/configuration/data"] = json.dumps(
                    config
                )
                nxdata = outentry[f"{self._nxprocess_name}/integrated"]
                measurement = outentry["measurement"]
                h5data = None
                h5errors = None
                h5counters = dict()

                for index, ptdata in bliss.iter_bliss_data(
                    self.inputs.filename,
                    self.inputs.scan,
                    lima_names=[detector_name],
                    counter_names=counter_names,
                    retry_timeout=retry_timeout,
                    retry_period=retry_period,
                    subscan=subscan,
                ):
                    normalization_factor = self.get_normalization(
                        ptdata.get(monitor_name), ptdata.get(reference_name, reference)
                    )
                    image = ptdata[detector_name]
                    if self.inputs.demo:
                        image = image[:-1, :-1]
                    result = worker.process(
                        image, normalization_factor=normalization_factor
                    )
                    if h5data is None:
                        axes = list()
                        if result.intensity.ndim == 2:
                            xname = "azimuth"
                            xunits = "deg"
                            nxdata[xname] = result.azimuthal
                            nxdata[xname].attrs["units"] = xunits
                            axes.append(xname)
                        xname = result.unit.name
                        xunits = result.unit.unit_symbol
                        nxdata[xname] = result.radial
                        nxdata[xname].attrs["units"] = xunits
                        axes.append(xname)

                        nxdata.attrs["signal"] = "data"
                        if result.intensity.ndim == 2:
                            nxdata.attrs["interpretation"] = "image"
                        else:
                            nxdata.attrs["interpretation"] = "spectrum"

                        h5data = DatasetWriter(nxdata, "data")
                        if result.sigma is not None:
                            h5errors = DatasetWriter(nxdata, "data_errors")
                        for name in counter_names:
                            h5counters[name] = DatasetWriter(measurement, name)

                    flush = h5data.add_point(result.intensity)
                    if result.sigma is not None:
                        flush |= h5errors.add_point(result.sigma)
                    for name in counter_names:
                        flush |= h5counters[name].add_point(ptdata[name])
                    if flush:
                        outentry.file.flush()

                if h5data is None:
                    raise RuntimeError("No scan data")
                h5data.flush_buffer()
                if h5errors is not None:
                    h5errors.flush_buffer()

                nxdata["points"] = numpy.arange(h5data.dataset.shape[0])
                nxdata.attrs["axes"] = ["points"] + axes

    def get_normalization(
        self, monitor: Optional[Number], reference: Optional[Number]
    ) -> tuple:
        # Inorm = I / normalization_factor
        if reference is None:
            normalization_factor = None
        else:
            if monitor is None:
                raise ValueError(
                    "provide a 'monitor_name' when providing a 'reference_name'"
                )
            normalization_factor = monitor / reference
        return normalization_factor

    @property
    def _nxprocess_name(self):
        return f"{self.inputs.detector_name}_integrated"

    @contextmanager
    def output_context(self):
        scan = self.inputs.scan
        subscan = self.get_input_value("subscan", 1)
        url = f"silx://{self.inputs.output_filename}?path=/{scan}.{subscan}"
        retryoptions = self._get_retry_options()
        url = nexus.create_url(url, **retryoptions)
        with h5py_utils.open_item(
            url.file_path(), "/", mode="a", **retryoptions
        ) as root:
            root.attrs["NX_class"] = "NXroot"
            entry = root[url.data_path()]
            measurement = entry.create_group("measurement")
            measurement.attrs["NX_class"] = "NXcollection"

            process = entry.create_group(self._nxprocess_name)
            process.attrs["NX_class"] = "NXprocess"
            process["program"] = "pyFAI"
            process["version"] = pyFAI.version

            configuration = process.create_group("configuration")
            configuration.attrs["NX_class"] = "NXnote"
            configuration["type"] = "application/json"

            data = process.create_group("integrated")
            data.attrs["NX_class"] = "NXdata"

            process.attrs["default"] = "integrated"
            entry.attrs["default"] = self._nxprocess_name
            root.attrs["default"] = url.data_path()

            yield entry

            self.link_inputs(entry)

    def _get_retry_options(self):
        retry_timeout = self.get_input_value("retry_timeout", None)
        retry_period = self.get_input_value("retry_period", 0.5)
        return {"retry_timeout": retry_timeout, "retry_period": retry_period}

    @h5py_utils.retry()
    def link_inputs(self, outentry):
        scan = self.inputs.scan
        subscan = self.get_input_value("subscan", 1)
        out_filename = outentry.file.filename
        ext_filename = os.path.relpath(
            out_filename, os.path.dirname(self.inputs.filename)
        )
        if ".." in ext_filename:
            ext_filename = self.inputs.filename
        retryoptions = self._get_retry_options()
        with h5py_utils.open_item(
            self.inputs.filename, f"{scan}.{subscan}", mode="r", **retryoptions
        ) as inentry:
            if "instrument" not in outentry:
                outentry["instrument"] = h5py.ExternalLink(
                    ext_filename, inentry["instrument"].name
                )
            imeasurement = inentry["measurement"]
            omeasurement = outentry["measurement"]
            for name in imeasurement.keys():
                if name in omeasurement:
                    continue
                if name not in omeasurement:
                    omeasurement[name] = h5py.ExternalLink(
                        ext_filename, imeasurement[name].name
                    )
            name = f"{self._nxprocess_name}/integrated/data"
            if name in outentry:
                omeasurement[self._nxprocess_name] = h5py.SoftLink(outentry[name].name)
