import numpy
from silx.io.dictdump import nxtodict
from ..tasks import SaveNexusPattern1D
from orangecontrib.ewoksxrpd.nexus import OWSaveNexusPattern1D
from .utils import execute_task


def test_save_nexus_task(tmpdir, setup1):
    assert_save_nexus(tmpdir, setup1, None)


def test_save_nexus_widget(tmpdir, setup1, qtapp):
    assert_save_nexus(tmpdir, setup1, qtapp)


def assert_save_nexus(tmpdir, setup1, qtapp):
    inputs = {
        "url": str(tmpdir / "result.h5"),
        "x": numpy.linspace(1, 60, 60),
        "y": numpy.random.random(60),
        "xunits": "2th_deg",
        "header": {
            "energy": 10.2,
            "detector": setup1.detector,
            "geometry": setup1.geometry,
        },
        "metadata": {"sample": {"@NX_class": "NXSample", "name": "mysample"}},
    }

    execute_task(
        SaveNexusPattern1D,
        OWSaveNexusPattern1D,
        inputs=inputs,
        widget=qtapp is not None,
    )

    adict = nxtodict(str(tmpdir / "result.h5"))

    numpy.testing.assert_array_equal(
        adict["results"]["diffractogram"]["2th"], inputs["x"]
    )
    numpy.testing.assert_array_equal(
        adict["results"]["diffractogram"]["data"], inputs["y"]
    )
    numpy.testing.assert_array_equal(
        adict["results"]["process"]["configuration"]["energy"],
        inputs["header"]["energy"],
    )
    numpy.testing.assert_array_equal(
        adict["results"]["process"]["configuration"]["energy@units"], "keV"
    )
    assert adict["results"]["sample"]["name"] == "mysample"
