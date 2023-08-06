import os
from numbers import Number
import numpy
from numpy.typing import ArrayLike

try:
    import matplotlib.pyplot as plt
    from matplotlib.colors import SymLogNorm
except ModuleNotFoundError:
    plt = SymLogNorm = None

import pyFAI
import pyFAI.azimuthalIntegrator

from ewokscore import Task
from ewoksdata.data import bliss

from .calibrate import calculate_geometry
from .utils import data_utils
from .utils import xrpd_utils


__all__ = [
    "DiagnoseCalibrateSingleResults",
    "DiagnoseCalibrateMultiResults",
    "DiagnoseIntegrate1D",
]


class _DiagnoseTask(
    Task,
    optional_input_names=["show", "pause", "filename"],
    output_names=["saved"],
    register=False,
):
    def show(self):
        if self.inputs.show:
            if self.inputs.pause and numpy.isfinite(self.inputs.pause):
                plt.pause(self.inputs.pause)
            else:
                plt.show()
        if self.inputs.filename:
            path = os.path.dirname(self.inputs.filename)
            if path:
                os.makedirs(path, exist_ok=True)
            plt.gcf().savefig(self.inputs.filename)
            self.outputs.saved = True
        else:
            self.outputs.saved = False


class _DiagnoseCalibrateResults(
    _DiagnoseTask,
    input_names=["detector", "calibrant"],
    register=False,
):
    def plot_calibration(
        self,
        ax1,
        ax2,
        image: ArrayLike,
        control_pts: dict,
        geometry: dict,
        energy: Number,
        title=None,
    ):
        colornorm = SymLogNorm(
            1,
            base=10,
            vmin=numpy.nanmin(image),
            vmax=numpy.nanmax(image),
        )
        if title:
            title = f"{title}: "
        else:
            title = ""

        ax1.imshow(image, origin="lower", cmap="inferno", norm=colornorm)
        ax1.set_title(f"{title}Rings")
        if control_pts:
            ax2.imshow(image, origin="lower", cmap="inferno", norm=colornorm)
            ax2.set_title(f"{title}Control points")

        # Calibrant rings on 2D pattern
        detector = data_utils.data_from_storage(self.inputs.detector)
        detector = pyFAI.detectors.detector_factory(detector)
        calibrant = data_utils.data_from_storage(self.inputs.calibrant)
        calibrant = pyFAI.calibrant.get_calibrant(calibrant)
        wavelength = xrpd_utils.energy_wavelength(energy)
        ai = pyFAI.azimuthalIntegrator.AzimuthalIntegrator(
            detector=detector, **geometry, wavelength=wavelength
        )
        calibrant.set_wavelength(wavelength)
        tth = calibrant.get_2th()
        ttha = ai.twoThetaArray()
        ax1.contour(
            ttha, levels=tth, cmap="autumn", linewidths=1
        )  # linestyles="dashed"

        # Detected points on 2D pattern
        for label, points in control_pts.items():
            ax2.scatter(points["p1"], points["p0"], label=label, marker=".")

    def show(self):
        # Diagnose
        # plt.legend(loc="center left", bbox_to_anchor=(1, 0.5))
        plt.tight_layout()
        super().show()


class DiagnoseCalibrateSingleResults(
    _DiagnoseCalibrateResults,
    input_names=["image", "geometry", "energy"],
    optional_input_names=["rings"],
):
    def run(self):
        if self.inputs.filename:
            if os.path.exists(self.inputs.filename):
                self.outputs.saved = True
                return
        if plt is None:
            raise RuntimeError("'matplotlib' is not installed")

        rings = self.inputs.rings
        if rings:
            _, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(20, 10))
        else:
            rings = dict()
            _, ax1 = plt.subplots(nrows=1, ncols=1, figsize=(10, 10))
            ax2 = None

        self.plot_calibration(
            ax1,
            ax2,
            bliss.get_image(self.inputs.image),
            data_utils.data_from_storage(rings),
            data_utils.data_from_storage(self.inputs.geometry),
            self.inputs.energy,
        )
        self.show()


class DiagnoseCalibrateMultiResults(
    _DiagnoseCalibrateResults,
    input_names=[
        "images",
        "positions",
        "parametrization",
        "parameters",
    ],
    optional_input_names=["show", "pause", "rings"],
):
    def run(self):
        if self.inputs.filename:
            if os.path.exists(self.inputs.filename):
                self.outputs.saved = True
                return
        if plt is None:
            raise RuntimeError("'matplotlib' is not installed")
        nimages = len(self.inputs.images)
        rings = self.inputs.rings
        if rings:
            rings = {int(k): v for k, v in rings.items()}
            _, axes = plt.subplots(nrows=nimages, ncols=2, figsize=(20, 10 * nimages))
        else:
            rings = {i: dict() for i in range(nimages)}
            _, axes = plt.subplots(nrows=nimages, ncols=1, figsize=(10, 10 * nimages))
            axes = [(ax1, None) for ax1 in axes]

        for image, position, ringsi, (ax1, ax2) in zip(
            self.inputs.images, self.inputs.positions, sorted(rings), axes
        ):
            image = bliss.get_image(image)
            position = bliss.get_data(position)
            title = f"position={position}"
            parametrization = data_utils.data_from_storage(self.inputs.parametrization)
            geometry, energy = calculate_geometry(
                parametrization, self.inputs.parameters, position
            )
            control_pts = data_utils.data_from_storage(rings[ringsi])
            self.plot_calibration(
                ax1, ax2, image, control_pts, geometry, energy, title=title
            )
        self.show()


class DiagnoseIntegrate1D(
    _DiagnoseTask,
    input_names=[
        "x",
        "y",
        "xunits",
    ],
    optional_input_names=["calibrant", "energy"],
):
    def run(self):
        if self.inputs.filename:
            if os.path.exists(self.inputs.filename):
                self.outputs.saved = True
                return
        if plt is None:
            raise RuntimeError("'matplotlib' is not installed")
        plt.figure(figsize=(20, 10))
        plt.plot(self.inputs.x, self.inputs.y)
        plt.yscale("symlog")
        plt.xlabel(self.inputs.xunits)
        if self.inputs.calibrant:
            assert self.inputs.energy, "'energy' task parameter is missing"
            self.plot_calibrant_lines()
        self.show()

    def plot_calibrant_lines(self):
        calibrant = data_utils.data_from_storage(self.inputs.calibrant)
        calibrant = pyFAI.calibrant.get_calibrant(calibrant)
        wavelength = xrpd_utils.energy_wavelength(self.inputs.energy)
        calibrant.set_wavelength(wavelength)

        xvalues = calibrant.get_peaks()
        mask = (xvalues >= min(self.inputs.x)) & (xvalues <= max(self.inputs.x))
        xvalues = xvalues[mask]
        if xvalues.size:
            yvalues = numpy.interp(xvalues, self.inputs.x, self.inputs.y)
            labels = xrpd_utils.calibrant_ring_labels(calibrant)
            labels = numpy.array(labels[: mask.size])[mask]
            ymin = min(self.inputs.y)
            for label, x, ymax in zip(labels, xvalues, yvalues):
                plt.plot([x, x], [ymin, ymax])
                # plt.text(x, ymax, label)
