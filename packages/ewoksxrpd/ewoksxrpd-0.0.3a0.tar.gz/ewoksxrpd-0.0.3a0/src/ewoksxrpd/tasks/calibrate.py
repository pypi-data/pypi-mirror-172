import logging
from numbers import Number
from typing import Dict, List, Optional, Set, Tuple

import pyFAI.detectors
import pyFAI.calibrant
import pyFAI.goniometer

from ewokscore import TaskWithProgress, Task
from ewoksdata.data import bliss

from .utils import xrpd_utils
from .utils import data_utils


__all__ = ["CalibrateSingle", "CalibrateMulti", "CalculateGeometry"]


logger = logging.getLogger(__name__)


def parse_fixed(
    fixed: Optional[List[str]], parametrization: Dict[str, List[str]]
) -> Set[str]:
    if not fixed:
        return set()
    allowed = {"dist", "poni1", "poni2", "rot1", "rot2", "rot3", "energy"}
    existing = set(fixed)
    unexpected = existing - allowed
    if unexpected:
        raise ValueError(f"'fixed' has unexpected parameters {sorted(unexpected)}")
    out = set()
    for param in fixed:
        out |= set(parametrization.get(param, {param}))
    return out


class CalibrateSingle(
    TaskWithProgress,
    input_names=["image", "detector", "calibrant", "geometry", "energy"],
    optional_input_names=["fixed", "max_rings", "robust"],
    output_names=["geometry", "energy", "detector", "rings", "chi2"],
):
    """Single distance and energy calibration."""

    def run(self):
        detector = data_utils.data_from_storage(self.inputs.detector)
        detector = pyFAI.detectors.detector_factory(detector)
        calibrant = data_utils.data_from_storage(self.inputs.calibrant)
        calibrant = pyFAI.calibrant.get_calibrant(calibrant)
        geometry0 = data_utils.data_from_storage(self.inputs.geometry)
        xrpd_utils.validate_geometry(geometry0)
        wavelength0 = xrpd_utils.energy_wavelength(self.inputs.energy)

        # Define setup
        setup = pyFAI.goniometer.SingleGeometry(
            "single",
            image=bliss.get_image(self.inputs.image),
            detector=detector,
            geometry=dict(geometry0),
            calibrant=calibrant,
        )

        setup.set_wavelength(wavelength0)

        # Find diffraction rings and fit
        self._refine(setup)

        # Parse results
        results = setup.geometry_refinement.get_config()
        geometry = {
            k: v for k, v in results.items() if k in xrpd_utils.GEOMETRY_PARAMETERS
        }
        energy = xrpd_utils.energy_wavelength(results["wavelength"])
        rings = xrpd_utils.points_to_rings(setup.geometry_refinement.data, calibrant)

        self.outputs.geometry = geometry
        self.outputs.energy = energy
        self.outputs.detector = self.inputs.detector
        self.outputs.rings = rings
        if setup.geometry_refinement.data.ndim != 2:
            self.outputs.chi2 = float("nan")
        else:
            self.outputs.chi2 = setup.geometry_refinement.chi2()

    def _refine(self, setup: pyFAI.goniometer.GoniometerRefinement) -> None:
        """Find diffraction rings and fit"""
        parametrization = {"energy": ["wavelength"]}
        force_fixed = parse_fixed(self.inputs.fixed, parametrization)
        fixed = fixed_prev = set(xrpd_utils.GEOMETRY_PARAMETERS) | {
            "wavelength"
        }  # all fixed

        max_rings = self.inputs.max_rings
        if max_rings:
            if max_rings < 0:
                max_rings = None
        else:
            max_rings = None

        def fit(*release):
            nonlocal fixed, fixed_prev
            set_free = set(release) - force_fixed
            if not set_free:
                return
            fixed -= set_free
            setup.extract_cp(max_rings=max_rings)
            if setup.geometry_refinement.data.ndim != 2:
                logger.warning("No rings detected for calibration")
                return
            setup.geometry_refinement.refine3(fix=fixed)  # method="slsqp"
            fixed_prev = fixed

        if self.inputs.robust:
            releases = [
                ["dist"],
                ["poni1", "poni2"],
                ["rot1", "rot2", "rot3"],
                ["wavelength"],
            ]
        else:
            releases = [
                ["dist", "poni1", "poni2", "rot1", "rot2", "rot3", "wavelength"]
            ]
        n = len(releases)
        for i, release in enumerate(releases, 1):
            fit(*release)
            self.progress = i / n * 100


class CalibrateMulti(
    TaskWithProgress,
    input_names=[
        "images",
        "positions",
        "detector",
        "calibrant",
        "geometry",
        "energy",
    ],
    optional_input_names=[
        "reference_position",
        "sample_position",
        "positionunits_in_meter",
        "fixed",
        "max_rings",
        "robust",
    ],
    output_names=[
        "geometry",
        "energy",
        "detector",
        "rings",
        "chi2",
        "parametrization",
        "parameters",
    ],
):
    """Single energy, multi distance calibration with 1 distance motor.

    The `images` and `positions` are the diffraction patterns and the motor positions at which those were measured.

    The `reference_position` is the detector position that corresponds to `geometry` (`positions[0]` by default).

    The `sample_position` is the position where sample and detector would theoretically coincide (0 by default).

    The output `energy` and `geometry` correspond to `sample_position`.

    The units of `positions`, `sample_position` and `reference_position` are defined by `positionunits_in_meter`
    (1e-3 by default which means the unit is in millimeter).

    The parametrization allow deriving energy+geometry from the detector position.

    .. code-block:: python

        energy, geometry = parametrization(parameters, position)
    """

    def run(self):
        if len(self.inputs.images) != len(self.inputs.positions):
            raise ValueError("number of 'images' and 'positions' must be the same")
        detector = data_utils.data_from_storage(self.inputs.detector)
        detector = pyFAI.detectors.detector_factory(detector)
        calibrant = data_utils.data_from_storage(self.inputs.calibrant)
        calibrant = pyFAI.calibrant.get_calibrant(calibrant)
        wavelength0 = xrpd_utils.energy_wavelength(self.inputs.energy)
        geometry0 = data_utils.data_from_storage(self.inputs.geometry)
        xrpd_utils.validate_geometry(geometry0)

        # Parameterize the detector geometry
        trans_function, initial_guess = self._reparametrization()

        # Define setup
        setup = pyFAI.goniometer.GoniometerRefinement(
            initial_guess,
            pos_function=lambda x: x,
            trans_function=trans_function,
            detector=detector,
            wavelength=wavelength0,
        )
        for i, (image, xi) in enumerate(zip(self.inputs.images, self.inputs.positions)):
            label = f"position{i}"
            image = bliss.get_image(image)
            xi = bliss.get_data(xi)
            setup.new_geometry(label, image=image, metadata=xi, calibrant=calibrant)

        # Find diffraction rings and fit
        self._refine(setup)

        # Parse results
        geometry, energy = self._get_fit_results(setup)
        paramerization = self._get_parameterization(setup)
        parameters = self._get_parameters(setup)
        rings = self._get_rings(setup, calibrant)
        chi2 = setup.chi2()

        self.outputs.geometry = geometry
        self.outputs.energy = energy
        self.outputs.detector = self.inputs.detector
        self.outputs.rings = rings
        self.outputs.chi2 = chi2
        self.outputs.parametrization = paramerization
        self.outputs.parameters = parameters

    def _reparametrization(
        self,
    ) -> Tuple[pyFAI.goniometer.ExtendedTransformation, List[Number]]:
        # xunits are the position units
        # dunits are the distance units of the fit parameters
        # aunits are the angular units of the fit parameters
        dunits_in_m = 100  # dunits/m
        aunits_in_rad = 10  # aunits/rad
        xunits_in_m = self._get_position_units()  # xunits/m

        trans_function = pyFAI.goniometer.ExtendedTransformation(
            param_names=[
                "dist_offset",  # dunits
                "dist_scale",  # dunits/xunits
                "poni1_offset",  # dunits
                "poni1_scale",  # dunits/xunits
                "poni2_offset",  # dunits
                "poni2_scale",  # dunits/xunits
                "arot1",  # aunits
                "arot2",  # aunits
                "arot3",  # aunits
                "energy",  # keV
            ],
            pos_names=["x"],  # xunits
            dist_expr=f"dist_scale / {dunits_in_m} * x + dist_offset / {dunits_in_m}",
            poni1_expr=f"poni1_scale / {dunits_in_m} * x + poni1_offset / {dunits_in_m}",
            poni2_expr=f"poni2_scale / {dunits_in_m} * x + poni2_offset / {dunits_in_m}",
            rot1_expr=f"arot1 / {aunits_in_rad}",
            rot2_expr=f"arot2 / {aunits_in_rad}",
            rot3_expr=f"arot3 / {aunits_in_rad}",
            wavelength_expr="hc*1e-10/energy",
        )

        geometry0 = self.inputs.geometry
        xref = self._get_reference_position()  # xunits
        dist_offset = self._get_sample_position() * xunits_in_m  # m
        dist_scale = (geometry0["dist"] - dist_offset) / xref  # m/xunits

        poni1_scale = 0.0  # m/xunits
        poni1_offset = geometry0["poni1"]  # m
        poni2_scale = 0.0  # m/xunits
        poni2_offset = geometry0["poni2"]  # m

        energy0 = self.inputs.energy
        initial_guess = [
            dist_offset * dunits_in_m,
            dist_scale * dunits_in_m,
            poni1_offset * dunits_in_m,
            poni1_scale * dunits_in_m,
            poni2_offset * dunits_in_m,
            poni2_scale * dunits_in_m,
            geometry0["rot1"] * aunits_in_rad,
            geometry0["rot2"] * aunits_in_rad,
            geometry0["rot3"] * aunits_in_rad,
            energy0,
        ]
        return trans_function, initial_guess

    def _refine(self, setup: pyFAI.goniometer.GoniometerRefinement) -> None:
        """Find diffraction rings and fit"""
        parametrization = {
            "dist": ["dist_offset", "dist_scale"],
            "poni1": ["poni1_offset", "poni1_scale"],
            "poni2": ["poni2_offset", "poni2_scale"],
            "rot1": ["arot1"],
            "rot2": ["arot2"],
            "rot3": ["arot3"],
        }
        force_fixed = parse_fixed(self.inputs.fixed, parametrization)
        fixed = fixed_prev = set(setup.trans_function.param_names)  # all fixed

        max_rings = self.inputs.max_rings
        if max_rings:
            if max_rings < 0:
                max_rings = None
        else:
            max_rings = None

        def fit(*release):
            nonlocal fixed, fixed_prev
            set_free = set(release) - force_fixed
            if not set_free:
                return
            fixed -= set_free
            for setup_single_dist in setup.single_geometries.values():
                setup_single_dist.extract_cp(max_rings=max_rings)
            setup.refine3(fix=fixed)  # method="slsqp"
            fixed_prev = fixed

        if self.inputs.robust:
            releases = [
                ["dist_offset", "dist_scale"],
                ["poni1_offset", "poni2_offset"],
                ["arot1", "arot2", "arot3"],
                ["poni1_scale", "poni2_scale"],
                ["energy"],
            ]
        else:
            releases = [
                [
                    "dist_offset",
                    "dist_scale",
                    "poni1_offset",
                    "poni2_offset",
                    "arot1",
                    "arot2",
                    "arot3",
                    "poni1_scale",
                    "poni2_scale",
                    "energy",
                ]
            ]
        n = len(releases)
        for i, release in enumerate(releases, 1):
            fit(*release)
            self.progress = i / n * 100

    def _get_rings(
        self,
        setup: pyFAI.goniometer.GoniometerRefinement,
        calibrant: pyFAI.calibrant.Calibrant,
    ) -> Dict[str, dict]:
        rings = dict()
        for i, setup_single_dist in enumerate(setup.single_geometries.values()):
            points = setup_single_dist.geometry_refinement.data
            rings[str(i)] = xrpd_utils.points_to_rings(points, calibrant)
        return rings

    def _get_fit_results(
        self, setup: pyFAI.goniometer.GoniometerRefinement
    ) -> Tuple[dict, Number]:
        parameters = setup.param
        xref = self._get_reference_position()
        results = setup.trans_function(parameters, xref)
        geometry = {k: getattr(results, k) for k in xrpd_utils.GEOMETRY_PARAMETERS}
        energy = xrpd_utils.energy_wavelength(results.wavelength)
        return geometry, energy

    def _get_parameterization(
        self, setup: pyFAI.goniometer.GoniometerRefinement
    ) -> dict:
        parametrization = dict(setup.trans_function.to_dict())
        parametrization.pop("constants")
        parametrization.pop("content")
        return parametrization

    def _get_parameters(self, setup: pyFAI.goniometer.GoniometerRefinement) -> dict:
        parameters = setup.param
        names = setup.trans_function.param_names
        return dict(zip(names, parameters))

    def _get_reference_position(self):
        """first image position by default (xunits)"""
        if self.missing_inputs.reference_position:
            return bliss.get_data(self.inputs.positions[0])
        else:
            return bliss.get_data(self.inputs.reference_position)

    def _get_sample_position(self):
        """0 by default (xunits)"""
        if self.missing_inputs.sample_position:
            return 0
        else:
            return bliss.get_data(self.inputs.sample_position)

    def _get_position_units(self):
        """millimeter by default"""
        if self.inputs.positionunits_in_meter:
            return self.inputs.positionunits_in_meter  # xunits/m
        else:
            return 1e-3  # xunits/m


def calculate_geometry(
    parametrization: dict, parameters: dict, position: Number
) -> Tuple[dict, Number]:
    trans_function = pyFAI.goniometer.ExtendedTransformation(**parametrization)
    parameters = [parameters[name] for name in trans_function.param_names]
    trans_function(parameters, position)
    results = trans_function(parameters, position)
    geometry = {k: getattr(results, k) for k in xrpd_utils.GEOMETRY_PARAMETERS}
    energy = xrpd_utils.energy_wavelength(results.wavelength)
    return geometry, energy


class CalculateGeometry(
    Task,
    input_names=["parametrization", "parameters", "position"],
    output_names=["geometry", "energy"],
):
    def run(self):
        parametrization = data_utils.data_from_storage(self.inputs.parametrization)
        geometry, energy = calculate_geometry(
            parametrization,
            self.inputs.parameters,
            bliss.get_data(self.inputs.position),
        )
        self.outputs.geometry = geometry
        self.outputs.energy = energy
