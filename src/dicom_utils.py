"""
This file is intended to be the utility file that concerts the Images to be displayed
and extract the patients data into the GUI
"""

import numpy as np
import pydicom
from pydicom.multival import MultiValue
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
    It includes the patient's name, ID, sex, birthdate, and modality.
    """
    given_name: str
    family_name: str
    patient_id: str
    sex: str
    birth_date: str
    modality: str

def extract_dicom_metadata(ds) -> PatientInfo:
    """
    This function extracts the patients data from the DICOM file
    As we are using test data I have made an if statement to say the data is Anonymous
    if the raw data comes back as a UUID and say everything is Anonymous
    If not it will grab the name and split it then add it to the GUI
    :param ds: dicom dataset
    :return: an array with the data in it for the main to read
    """

    patient_name = ds.get("PatientName", None)

    #If statement to return data
    if not patient_name or len(str(patient_name)) > 20:  # Anonymized (UUID)
        given = "Anonymous"
        family = "Anonymous"
    else:
        given = getattr(patient_name, "given_name", "Unknown")
        family = getattr(patient_name, "family_name", "Unknown")

    return PatientInfo(
        given_name = given,
        family_name = family,
        patient_id=str(ds.get("PatientID", "Unknown")),
        sex=str(ds.get("PatientSex", "Unknown")),
        birth_date=str(ds.get("PatientBirthDate", "Unknown")),
        modality=str(ds.get("Modality", "Unknown"))
    )


def validate_dicom(ds):
    """
   Checks if the DICOM dataset contains required fields and handles specific image types.

    :param ds: The DICOM dataset.
    :raises ValueError: If required DICOM fields are missing.
    :raises TypeError: If ImageType is not a string or MultiValue.
    :return: True if the DICOM is valid, False otherwise.
    """

    #must have these fields in the file
    required_fields = ["StudyID", "StudyDescription"]
    if missing_fields := [
        field for field in required_fields if not getattr(ds, field, None)
    ]:
        raise ValueError(f"Missing required DICOM fields: {', '.join(missing_fields)}")

    #raises error for "LOCALISER" images & non-AXIAL images
    if image_type := ds.get("ImageType", None):
        if isinstance(image_type, pydicom.multival.MultiValue):
            image_type_list = [str(val).strip().upper() for val in image_type]
            if "LOCALIZER" in image_type_list:
                raise ValueError("Skipping LOCALIZER image.")
            if "AXIAL" not in image_type_list:
                raise ValueError("Skipping non-AXIAL image.")
        elif not isinstance(image_type, str):
            raise TypeError("ImageType must be a string or MultiValue")

    return True
