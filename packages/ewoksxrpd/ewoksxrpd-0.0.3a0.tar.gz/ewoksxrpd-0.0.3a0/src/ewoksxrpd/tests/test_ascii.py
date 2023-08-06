import re
import numpy
from ..tasks import SaveAsciiPattern1D
from orangecontrib.ewoksxrpd.ascii import OWSaveAsciiPattern1D
from .utils import execute_task


def test_save_ascii_task(tmpdir, setup1):
    assert_save_ascii(tmpdir, setup1, None)


def test_save_ascii_widget(tmpdir, setup1, qtapp):
    assert_save_ascii(tmpdir, setup1, qtapp)


def assert_save_ascii(tmpdir, setup1, qtapp):
    inputs = {
        "filename": str(tmpdir / "result.dat"),
        "x": numpy.linspace(1, 60, 60),
        "y": numpy.random.random(60),
        "xunits": "2th_deg",
        "header": {
            "energy": 10.2,
            "detector": setup1.detector,
            "geometry": setup1.geometry,
        },
        "metadata": {"name": "mysample"},
    }

    execute_task(
        SaveAsciiPattern1D,
        OWSaveAsciiPattern1D,
        inputs=inputs,
        widget=qtapp is not None,
    )

    x, y = numpy.loadtxt(str(tmpdir / "result.dat")).T
    numpy.testing.assert_array_equal(x, inputs["x"])
    numpy.testing.assert_array_equal(y, inputs["y"])

    with open(tmpdir / "result.dat") as f:
        lines = list()
        for line in f:
            if not line.startswith("#"):
                break
            lines.append(line)

    lines = "".join(lines)
    m = re.findall("energy = (.+) keV", lines)
    assert len(m) == 1
    assert float(m[0]) == inputs["header"]["energy"]
    assert "name = mysample"
