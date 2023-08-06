import numpy
from ..tasks import SubtractBackground
from orangecontrib.ewoksxrpd.background import OWSubtractBackground
from .xrpd_theory import Measurement
from .utils import execute_task


def test_background_subtraction_task(
    imageSetup1SampleA: Measurement,
    image1Setup1SampleB: Measurement,
    image2Setup1SampleB: Measurement,
):
    assert_background_subtraction(
        imageSetup1SampleA, image1Setup1SampleB, image2Setup1SampleB, None
    )


def test_background_subtraction_widget(
    imageSetup1SampleA: Measurement,
    image1Setup1SampleB: Measurement,
    image2Setup1SampleB: Measurement,
    qtapp,
):
    assert_background_subtraction(
        imageSetup1SampleA, image1Setup1SampleB, image2Setup1SampleB, qtapp
    )


def assert_background_subtraction(
    imageSetup1SampleA: Measurement,
    image1Setup1SampleB: Measurement,
    image2Setup1SampleB: Measurement,
    qtapp,
):
    image = imageSetup1SampleA.image + image1Setup1SampleB.image
    inputs = {
        "image": image,
        "monitor": imageSetup1SampleA.monitor,
        "background": image2Setup1SampleB.image,
        "background_monitor": image2Setup1SampleB.monitor,
    }
    results = execute_task(
        SubtractBackground,
        OWSubtractBackground,
        inputs=inputs,
        widget=qtapp is not None,
    )
    numpy.testing.assert_allclose(
        imageSetup1SampleA.image, results["image"], atol=1e-10
    )
