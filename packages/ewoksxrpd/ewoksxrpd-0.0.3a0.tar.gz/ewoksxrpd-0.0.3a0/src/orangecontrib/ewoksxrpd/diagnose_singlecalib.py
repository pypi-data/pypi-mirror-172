import os
from AnyQt import QtWidgets
from AnyQt import QtGui

# from AnyQt.QtCore import Qt
from ewoksxrpd.tasks import DiagnoseCalibrateSingleResults
from ewoksxrpd.gui.trigger_widget import OWTriggerWidget
from ewoksxrpd.gui.forms import input_parameters_diagnose_singlecalib


__all__ = ["OWDiagnoseCalibrateSingleResults"]


class OWDiagnoseCalibrateSingleResults(
    OWTriggerWidget, ewokstaskclass=DiagnoseCalibrateSingleResults
):
    name = "DiagnoseCalibrateSingleResults"
    description = "Diagnose single-distance calibration"
    icon = "icons/widget.png"
    want_main_area = True

    def _init_forms(self):
        parameter_info = input_parameters_diagnose_singlecalib(
            self.get_default_input_values()
        )
        self._create_input_form(parameter_info)

    def _init_main_area(self):
        layout = self._get_main_layout()
        self._label = QtWidgets.QLabel()
        layout.addWidget(self._label)
        super()._init_main_area()

    def _refresh_non_form_output_widgets(self):
        with self._capture_errors():
            super()._refresh_non_form_output_widgets()
            self._update_output_file()

    def _update_output_file(self):
        inputs = self.get_task_input_values()
        filename = inputs.get("filename")
        if not filename or not os.path.isfile(filename):
            self._label.clear()
            return

        pixmap = QtGui.QPixmap(filename)
        # pixmap = pixmap.scaled(10,5,Qt.KeepAspectRatio)
        self._label.setPixmap(pixmap)
