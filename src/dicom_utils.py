"""
This file is intended to be the utility file that concerts the Images to be displayed
and extract the patients data into the GUI
"""

import numpy as np
from PySide6.QtGui import QImage

def numpy_to_qimage(array):
    """
    This function converts a NumPy array representing a grayscale image to a QImage, suitable for display in Qt-based GUIs.
    It normalizes the array to 0-255, then creates a QImage with the grayscale format.
    :param array:
    :return: QImage || error || nothing
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

def extract_dicom_metadata(ds):
    """
    This function extracts the patients data from the DICOM file
    As we are using test data I have made an if statement to say the data is Anonymous
    if the raw data comes back as a UUID and say everything is Anonymous
    If not it will grab the name and split it then add it to the GUI
    :param ds: dicom dataset
    :return: an array with the data in it for the main to read
    """

    raw_name = str(ds.get("PatientName", "")).strip()

    if not raw_name or len(raw_name) > 20:
        #If raw name = UUID
        given = "Anonymous"
        family = "Anonymous"
        patient_id = "Anonymous"
        patient_sex = "Unknown"
        birth_date = "Unknown"
    elif "^" in raw_name:
        #If it is not an Anonymous patient
        family, given = raw_name.split("^", 1)
        patient_id = str(ds.get("PatientID", "Unknown"))
        patient_sex = str(ds.get("PatientSex", "Unknown"))
        birth_date = str(ds.get("PatientBirthDate", "Unknown"))
    else:
        #Patient has no last name
        given = raw_name
        family = "No Last Name"
        patient_id = str(ds.get("PatientID", "Unknown"))
        patient_sex = str(ds.get("PatientSex", "Unknown"))
        birth_date = str(ds.get("PatientBirthDate", "Unknown"))

    return {
        "GivenName": given,
        "FamilyName": family,
        "PatientID": patient_id,
        "PatientSex": patient_sex,
        "PatientBirthDate": birth_date,
        "Modality": str(ds.get("Modality", "Unknown")),
    }
