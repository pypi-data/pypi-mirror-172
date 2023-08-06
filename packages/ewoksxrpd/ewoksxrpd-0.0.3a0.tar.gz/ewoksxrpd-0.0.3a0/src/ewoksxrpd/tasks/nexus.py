import pyFAI
import h5py
import numpy
from silx.io.dictdump import dicttonx

from ewokscore import Task
from ewokscore.task import TaskInputError
from ewoksdata.data import nexus

from .utils.xrpd_utils import energy_wavelength
from .utils.data_utils import is_data


__all__ = ["SaveNexusPattern1D"]


class SaveNexusPattern1D(
    Task,
    input_names=[
        "url",
        "x",
        "y",
        "xunits",
    ],
    optional_input_names=["header", "yerror", "metadata"],
    output_names=["saved"],
):
    def run(self):
        url = nexus.create_url(self.inputs.url)
        with h5py.File(url.file_path(), "a") as parent:
            parent = parent[url.data_path()]
            self.save_diffractogram(parent)
            self.save_metadata(parent)
            self.save_nxprocess(parent)
        self.outputs.saved = True

    def save_diffractogram(self, parent):
        xunits = self.inputs.xunits
        if xunits:
            if isinstance(xunits, numpy.ndarray):
                xunits = xunits.item()
            tpl = xunits.split("_")
        else:
            tpl = tuple()
        if len(tpl) != 2:
            raise TaskInputError("xunits")
        xname, xunits = tpl
        x = self.inputs.x
        y = self.inputs.y
        yerror = self.inputs.yerror

        yname = "data"
        if "diffractogram" in parent:
            del parent["diffractogram"]
        nxdata = parent.create_group("diffractogram")
        nxdata.attrs["NX_class"] = "NXdata"
        nexus.select_default_plot(nxdata)
        nxdata.attrs["axes"] = [xname]
        nxdata.attrs["signal"] = yname
        xdset = nxdata.create_dataset(xname, data=x)
        xdset.attrs["units"] = xunits
        nxdata.create_dataset(yname, data=y)
        if is_data(yerror):
            nxdata.create_dataset(f"{yname}_errors", data=yerror)

    def save_metadata(self, parent):
        metadata = self.inputs.metadata
        if not metadata:
            return
        dicttonx(metadata, parent, update_mode="add")

    def save_nxprocess(self, parent):
        if "process" in parent:
            del parent["process"]
        nxprocess = parent.create_group("process")
        nxprocess.attrs["NX_class"] = "NXprocess"
        nxprocess["program"] = "pyFAI"
        nxprocess["version"] = pyFAI.version
        self.save_configuration(nxprocess)

    def save_configuration(self, nxprocess):
        header = self.inputs.header
        if not header:
            return
        if "configuration" in nxprocess:
            del nxprocess["configuration"]
        configuration = nxprocess.create_group("configuration")
        configuration.attrs["NX_class"] = "NXcollection"

        info = dict(header)

        if info.get("energy") or info.get("wavelength"):
            energy = info.pop("energy", None)
            wavelength = info.pop("wavelength", None)
            if not energy:
                energy = energy_wavelength(wavelength)
            elif not wavelength:
                wavelength = energy_wavelength(energy)
            dset = configuration.create_dataset("energy", data=energy)
            dset.attrs["units"] = "keV"
            dset = configuration.create_dataset("wavelength", data=wavelength)
            dset.attrs["units"] = "Angstrom"

        if info.get("detector"):
            configuration["detector"] = str(info.pop("detector"))

        if info.get("geometry"):
            cgeometry = configuration.create_group("geometry")
            cgeometry.attrs["NX_class"] = "NXcollection"

            geometry = info.pop("geometry")
            for k, v in geometry.items():
                if k == "dist":
                    dset = cgeometry.create_dataset("dist", data=v)
                    dset.attrs["units"] = "m"
                elif k == "poni1":
                    dset = cgeometry.create_dataset("poni1", data=v)
                    dset.attrs["units"] = "m"
                elif k == "poni2":
                    dset = cgeometry.create_dataset("poni2", data=v)
                    dset.attrs["units"] = "m"
                elif k == "rot1":
                    dset = cgeometry.create_dataset("rot1", data=v)
                    dset.attrs["units"] = "rad"
                elif k == "rot2":
                    dset = cgeometry.create_dataset("rot2", data=v)
                    dset.attrs["units"] = "rad"
                elif k == "rot3":
                    dset = cgeometry.create_dataset("rot3", data=v)
                    dset.attrs["units"] = "rad"

        if info:
            dicttonx(info, configuration)
