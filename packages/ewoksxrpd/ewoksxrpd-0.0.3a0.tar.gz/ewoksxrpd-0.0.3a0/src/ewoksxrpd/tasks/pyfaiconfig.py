import json
from pyFAI.io.ponifile import PoniFile
from ewokscore import Task

from .utils.xrpd_utils import energy_wavelength

__all__ = ["PyFaiConfig"]


class PyFaiConfig(
    Task,
    optional_input_names=[
        "filename",
        "energy",
        "geometry",
        "mask",
        "detector",
        "calibrant",
        "integration_options",
        "worker_options",
    ],
    output_names=[
        "energy",
        "geometry",
        "detector",
        "calibrant",
        "mask",
        "integration_options",
        "worker_options",
    ],
):
    def run(self):
        all_options = self.from_file()
        if self.inputs.integration_options:
            all_options = {**self.inputs.integration_options, **all_options}
        if self.inputs.worker_options:
            all_options = {**self.inputs.worker_options, **all_options}

        # Required outputs
        energy = self.inputs.energy
        wavelength = all_options.pop("wavelength", None)
        if self.missing_inputs.energy and wavelength is not None:
            energy = energy_wavelength(wavelength)

        detector = self.inputs.detector
        cdetector = all_options.pop("detector", None)
        if self.missing_inputs.detector and cdetector is not None:
            detector = cdetector

        geometry = self.inputs.geometry
        cgeometry = {
            k: all_options.pop(k)
            for k in ["dist", "poni1", "poni2", "rot1", "rot2", "rot3"]
            if k in all_options
        }
        if self.missing_inputs.geometry and len(cgeometry) == 6:
            geometry = cgeometry

        # Optional outputs
        calibrant = self.get_input_value("calibrant", None)

        mask = self.get_input_value("mask", None)
        cmask = all_options.pop("mask_file", None)
        if self.missing_inputs.mask and cmask is not None:
            mask = cmask

        # Split integration and worker options
        worker_options = {
            k: all_options.pop(k)
            for k in ["integrator_name", "extra_options"]
            if k in all_options
        }

        self.outputs.energy = energy
        self.outputs.geometry = geometry
        self.outputs.detector = detector
        self.outputs.calibrant = calibrant
        self.outputs.mask = mask
        self.outputs.integration_options = all_options
        self.outputs.worker_options = worker_options

    def from_file(self) -> dict:
        filename = self.inputs.filename
        if not filename:
            return dict()
        if filename.endswith(".json"):
            with open(filename, "r") as fp:
                return json.load(fp)
        else:
            return PoniFile(filename).as_dict()
