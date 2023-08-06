import os
import numpy
import pyFAI

import ewoks
from ewokscore import Task

from .utils.xrpd_utils import energy_wavelength
from .utils.data_utils import is_data

__all__ = ["SaveAsciiPattern1D"]


class SaveAsciiPattern1D(
    Task,
    input_names=[
        "filename",
        "x",
        "y",
        "xunits",
    ],
    optional_input_names=["header", "yerror", "metadata"],
    output_names=["saved"],
):
    def run(self):
        if is_data(self.inputs.yerror):
            data = [self.inputs.x, self.inputs.y, self.inputs.yerror]
        else:
            data = [self.inputs.x, self.inputs.y]
        data = numpy.stack(data, axis=1)

        header = {
            "pyFAI": pyFAI.version,
            "ewoks": ewoks.__version__,
            "xunits": self.inputs.xunits,
        }
        if self.inputs.header:
            info = dict(self.inputs.header)

            if info.get("energy"):
                energy = info.pop("energy")
                info.pop("wavelength", None)
                header["energy"] = "{:.18e} keV".format(energy)
                wavelength = energy_wavelength(energy)
                header["wavelength"] = "{:.18e} Angstrom".format(wavelength)

            if info.get("detector"):
                header["detector"] = str(info.pop("detector"))

            if info.get("geometry"):
                geometry = info.pop("geometry")
                for k, v in geometry.items():
                    if k == "dist":
                        header["distance"] = "{:.18e} m".format(v)
                    elif k == "poni1":
                        header["center dim0"] = "{:.18e} m".format(v)
                    elif k == "poni2":
                        header["center dim1"] = "{:.18e} m".format(v)
                    elif k == "rot1":
                        header["rot1"] = "{:.18e} deg".format(numpy.degrees(v))
                    elif k == "rot2":
                        header["rot2"] = "{:.18e} deg".format(numpy.degrees(v))
                    elif k == "rot3":
                        header["rot3"] = "{:.18e} deg".format(numpy.degrees(v))

            header.update({k: str(v) for k, v in info.items()})

        lst = [f"{k} = {v}" for k, v in header.items()]
        metadata = self.inputs.metadata
        if metadata:
            lst.extend(f"{k} = {v}" for k, v in metadata.items())
        header = "\n".join(lst)

        dirname = os.path.dirname(self.inputs.filename)
        if dirname:
            os.makedirs(dirname, exist_ok=True)
        numpy.savetxt(self.inputs.filename, data, header=header)
        self.outputs.saved = True
