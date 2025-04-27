"""
This file is intended to be the utility file that concerts the Images to be displayed
and extract the patients data into the GUI
"""

import numpy as np
from PySide6.QtGui import QImage
from dataclasses import dataclass

def numpy_to_qimage(array):
    """
    This function converts a NumPy array representing a grayscale image to a QImage,
    suitable for display in Qt-based GUIs.
    It normalizes the array to 0-255, then creates a QImage with the grayscale format.
    :param array: 2D NumPy array
    :return: QImage object in grayscale format using the normalized array data and dimensions.
    """
    if array is None:
        raise TypeError("Input array cannot be None")

    if array.ndim != 2:
        raise ValueError("Array must be 2D")

    norm_array = (255 * array).clip(0, 255).astype(np.uint8)
    height, width = norm_array.shape
    bytes_per_line = width * norm_array.itemsize

    return QImage(
        norm_array.data,
        width,
        height,
        bytes_per_line,
        QImage.Format_Grayscale8,
    )

@dataclass
class PatientInfo:
    """
    This class stores patient information extracted from a DICOM file.
    It includes the patient's name, ID, sex, birth date, and modality.
    """
    given_name: str
    family_name: str
    patient_id: str
    sex: str
    birth_date: str
    modality: str

def extract_dicom_metadata(ds):
    """
    This function extracts the patients data from the DICOM file
    As we are using test data I have made an if statement to say the data is Anonymous
    if the raw data comes back as a UUID and say everything is Anonymous
    If not it will grab the name and split it then add it to the GUI
    :param ds: dicom dataset
    :return: an array with the data in it for the main to read
    """

    patient_name = ds.get("PatientName", None)

    # Prepare common metadata
    common = {
        "PatientID": str(ds.get("PatientID", "Unknown")),
        "PatientSex": str(ds.get("PatientSex", "Unknown")),
        "PatientBirthDate": str(ds.get("PatientBirthDate", "Unknown")),
        "Modality": str(ds.get("Modality", "Unknown")),
    }

    #If statement to return data
    if not patient_name or len(str(patient_name)) > 20:  # Anonymized (UUID)
        given = "Anonymous"
        family = "Anonymous"
    else:
        given = getattr(patient_name, "given_name", "Unknown")
        family = getattr(patient_name, "family_name", "Unknown")

    return {
        "GivenName": given,
        "FamilyName": family,
        **common,
    }
