import numpy
import h5py
import pytest
from ..tasks import IntegrateBlissScan
from orangecontrib.ewoksxrpd.batchintegrate import OWIntegrateBlissScan
from . import xrpd_theory
from .utils import execute_task


@pytest.mark.parametrize("ndims", [1, 2])
def test_batch_integrate(ndims, bliss_lab6_scan, setup1: xrpd_theory.Setup, tmpdir):
    assert_batch_integrate(ndims, bliss_lab6_scan, setup1, tmpdir)


@pytest.mark.parametrize("ndims", [1, 2])
def test_batch_integrate_qt(
    ndims, bliss_lab6_scan, setup1: xrpd_theory.Setup, tmpdir, qtapp
):
    assert_batch_integrate(ndims, bliss_lab6_scan, setup1, tmpdir, qtapp=qtapp)


def assert_batch_integrate(
    ndims, bliss_lab6_scan, setup1: xrpd_theory.Setup, tmpdir, qtapp=None
):
    output_filename = str(tmpdir / "result.h5")
    inputs = {
        "filename": bliss_lab6_scan,
        "scan": 2,
        "detector": setup1.detector,
        "energy": setup1.energy,
        "geometry": setup1.geometry,
        "detector_name": "p3",
        "monitor_name": "monitor",
        "reference": 1.0,
        "output_filename": output_filename,
        "retry_timeout": 2,
    }

    if ndims == 2:
        inputs["integration_options"] = {
            "method": "no_csr_cython",
            "nbpt_azim": 100,
            "error_model": "poisson",
        }
        inputs["worker_options"] = {"integrator_name": "integrate2d_ng"}
    else:
        inputs["integration_options"] = {
            "method": "no_csr_cython",
            "error_model": "azimuthal",
        }
        inputs["worker_options"] = {
            "integrator_name": "sigma_clip_ng",
            "extra_options": {"max_iter": 3, "thres": 0},
        }

    execute_task(
        IntegrateBlissScan,
        OWIntegrateBlissScan,
        inputs=inputs,
        widget=qtapp is not None,
    )

    with h5py.File(output_filename) as root:
        data = root["2.1/measurement/p3_integrated"][()]
        if ndims == 2:
            axes = ["points", "azimuth", "2th_deg"]
        else:
            axes = ["points", "2th_deg"]
        assert root["2.1/p3_integrated/integrated"].attrs["axes"].tolist() == axes
        spectrum0 = data[0]
        for spectrum in data:
            numpy.testing.assert_allclose(spectrum, spectrum0, atol=1)

        # Check links to raw data
        root["2.1/measurement/monitor"][()]
        list(root["2.1/instrument"].keys())
