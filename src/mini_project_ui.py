
import numpy as np
import sys
import pydicom
import logging
from PySide6 import QtWidgets
from PySide6.QtWidgets import QMessageBox
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import QTimer
from src.inputs_and_outputs import get_qimage_from_dicom_file
from src.dicom_utils import extract_patient_info, validate_dicom
from src.read_dicom_file import read_dicom_file
from src.user_pref_controller import UserPrefController
from babel.dates import format_date
import pathlib
import os

class MiniProjectUI(QtWidgets.QDialog):
    """The class that contains the UI"""
    number_rows_for_dic_button = 2

    def __init__(self,data_base):
        super().__init__()
        self.setWindowTitle("Mini Project UI")
        self.path = ""
        self.data_base = data_base
        if self.data_base is not None:
            default_path = self.data_base.default_path()
            if default_path is not None:
                self.path = str(default_path)
        
        self.directory_button_box()
        main_layout = QtWidgets.QVBoxLayout()
        self.image_label = QtWidgets.QLabel("No Image to Display")

        main_layout.addWidget(self._grid_group_box)
        main_layout.addWidget(self.image_label)

        self.setLayout(main_layout)

        QTimer.singleShot(100,self.check_saved_dir)


    #popup to allow the user to open a diretory checks if the user want to open or close the program
    def please_select_directory(self): 
        """Popup to allow the user to select a directory"""
        pop_up = QtWidgets.QMessageBox()
        pop_up.setIcon(QtWidgets.QMessageBox.Question)
        pop_up.setText("Please Select A DICOM File to Open")
        pop_up.setStandardButtons(QtWidgets.QMessageBox.Close | QtWidgets.QMessageBox.Open)
        anw = pop_up.exec()

        if anw == QtWidgets.QMessageBox.Close:
            QtWidgets.QApplication.exit()
        elif anw == QtWidgets.QMessageBox.Open:
            self.add_directory()


    def file_cannot_be_opened_error(self):
        """Displays the file error open button"""
        error_message = QtWidgets.QMessageBox()
        error_message.setIcon(QtWidgets.QMessageBox.Warning)
        error_message.setText("File can not be opened because the file is missing format data or appropriate headers")
        error_message.exec()

    def show_database_message(self, success: bool):
        """Dislays a message to inform user if the value was saved"""
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information if success else QMessageBox.Warning)
        msg_box.setText("Database saved successfully." if success else "Database could not save the path")
        msg_box.exec()

    def directory_button_box(self):
        """Creates the grid layout for the button box"""
        self._grid_group_box = QtWidgets.QGroupBox("Patient Information")
        layout = QtWidgets.QGridLayout()
        button = QtWidgets.QPushButton("Open New File")
        path_label = QtWidgets.QLabel("Path: ")
        self.text = QtWidgets.QLabel()
        fname_label = QtWidgets.QLabel("First Name:")
        lname_label = QtWidgets.QLabel("Last Name:")
        self.fname = QtWidgets.QLabel("First Name")
        self.lname = QtWidgets.QLabel("Last Name")
        self.dob_label = QtWidgets.QLabel("Date Of Birth:")
        self.dob = QtWidgets.QLabel("Date Of Birth: ")
        self.patient_id_label = QtWidgets.QLabel("patient ID:")
        self.patient_id = QtWidgets.QLabel("Patient ID")
        self.sex_label = QtWidgets.QLabel("Sex:")
        self.sex =  QtWidgets.QLabel("M/F")
        self.modality_label = QtWidgets.QLabel("Modality:")
        self.modality = QtWidgets.QLabel("Modality")

        button.clicked.connect(self.add_directory)
        layout.addWidget(path_label, 0, 0)
        layout.addWidget(self.text, 0, 1, 1,4)
        layout.addWidget(fname_label, 1, 0)
        layout.addWidget(lname_label, 2, 0)
        layout.addWidget(self.dob_label, 3, 0)
        layout.addWidget(self.sex_label, 1, 3)
        layout.addWidget(self.patient_id_label, 2, 3)
        layout.addWidget(self.modality_label, 3, 3)
        layout.addWidget(self.fname, 1, 1)
        layout.addWidget(self.lname, 2, 1)
        layout.addWidget(self.dob, 3, 1)
        layout.addWidget(self.sex, 1, 4)
        layout.addWidget(self.patient_id, 2, 4)
        layout.addWidget(self.modality, 3, 4)
        layout.addWidget(button, 5, 4)
        layout.setColumnStretch(1, 20)
        self._grid_group_box.setLayout(layout)

    def add_directory(self):
        """Function for the button click"""
        if self.path is None: # To deal with if self.path is not initialized
            self.path = ""
        path_object = pathlib.Path(self.path).parent

        if ( # To ensure the paths given are valid paths
                not path_object.exists()
                or not path_object.is_dir()
                or self.path.strip() == ""
        ):
            # Sending to home directory if path doesn't exist
            path_object = pathlib.Path.home()

        dir_path, _ = QtWidgets.QFileDialog.getOpenFileName(self,
                                                            caption="Select DICOM File",
                                                            dir=str(path_object),
                                                            filter="DICOM Files (*.dcm)")
        # on cancel getOpenFileName returns an empty string need to skip
        if dir_path.strip() != "":
            self.path = dir_path
            self.open_dicom_file()

    #This also needs to be changed to reflect the MySQL
    def check_saved_dir(self):
        """Checks if the file in the directory has been created"""
        if self.path != "":
            self.open_dicom_file()
        else:
            self.text.setText("Please open a DICOM file")
            self.please_select_directory()

    def save_directory_path(self):
        """Saves the directory path the database""" 
        if self.data_base.save_default_path(self.path):
            self.show_database_message(success=True)
        else:
            self.show_database_message(success=False)

    #opens the dicom file and sets all of the data for the Patains like DOB Sex ect
    def set_label(self, ds, field, label, default):
        """Function to use to set the labels for PatientID, dob, ID, modality"""
        value = ds.get(field, None)
        label.setText(str(value) if value else default)

    def open_dicom_file(self):
        """Opens a DICOM file and displays the image linked to that file, if available"""
        try:
            ds = read_dicom_file(self.path)

            #Adds the validation needed for AXIAL files and "StudyID+StudyDescription"
            if ds is not None:
                validate_dicom(ds)
            else:
                logging.error("validate_dicom failed")
                # just returning to avoid raising exception as exception is handled by not overwriting self.path if an empty string is the path
                return
                # raise ValueError("Invalid DICOM file or failed to load the file.")

            if ds is not None:
                self.save_directory_path()
            else:
                logging.error("Could not open DICOM file")

        except pydicom.errors.InvalidDicomError:
            self.file_cannot_be_opened_error()

        self.text.setText(self.path)


        metadata = extract_patient_info(ds)

        # Check for pixel data, and display it if available
        if 'PixelData' in ds:
            try:
                image = get_qimage_from_dicom_file(ds)
                pixmap = QPixmap.fromImage(image)
                self.image_label.setPixmap(pixmap)
                self.image_label.setScaledContents(True)
            except Exception as e:
                logging.error(f"Error displaying image: {e}")
                self.image_label.setText("Error Displaying Image")
        else:
            self.image_label.setText("No Image Data Found")

        if metadata.birth_date:
            # Change the date variable to a string
            formatted_birth_date = format_date(metadata.birth_date, format='long', locale='en')
        else:
            formatted_birth_date = "Unknown"

        # A number of checks to see if there is data avalible to fill in
        self.fname.setText(metadata.given_name)
        self.lname.setText(metadata.family_name)
        self.patient_id.setText(metadata.patient_id)
        self.sex.setText(metadata.sex)
        self.dob.setText(formatted_birth_date)
        self.modality.setText(metadata.modality)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    database = UserPrefController(pathlib.Path("preferences.db"))
    widget = MiniProjectUI(database)
    widget.show()
    sys.exit(app.exec())
