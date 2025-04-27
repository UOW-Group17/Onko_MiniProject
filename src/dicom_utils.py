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

    # Prepare common metadata
    common = {
        "PatientID": str(ds.get("PatientID", "Unknown")),
        "PatientSex": str(ds.get("PatientSex", "Unknown")),
        "PatientBirthDate": str(ds.get("PatientBirthDate", "Unknown")),
        "Modality": str(ds.get("Modality", "Unknown")),
    }

    #If statement to return data
    if not raw_name or len(raw_name) > 20:
        given, family = "Anonymous", "Anonymous"
    elif "^" in raw_name:
        family, given = raw_name.split("^", 1)
    else:
        given, family = raw_name, "No Last Name"

    return {
        "GivenName": given,
        "FamilyName": family,
        **common,
    }
