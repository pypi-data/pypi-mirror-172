from ewokscore import Task
from ewoksdata.data import bliss

__all__ = ["SubtractBackground"]


class SubtractBackground(
    Task,
    input_names=["image", "monitor", "background", "background_monitor"],
    output_names=["image", "monitor"],
):
    """The background will be normalized to the monitor:

    .. code:

        Icor = I  - B / Bmon * Imon
    """

    def run(self):
        monitor = bliss.get_data(self.inputs.monitor)
        norm = monitor / bliss.get_data(self.inputs.background_monitor)
        background = norm * bliss.get_image(self.inputs.background)
        self.outputs.image = bliss.get_image(self.inputs.image) - background
        self.outputs.monitor = monitor
