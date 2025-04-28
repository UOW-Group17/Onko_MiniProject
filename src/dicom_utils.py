"""
This file is intended to be the utility file that converts the Images to be displayed
and extract the patients data into the GUI
"""

import numpy as np
import pydicom
from datetime import datetime
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
    birth_date: datetime.date
    modality: str

def extract_patient_info(ds) -> PatientInfo:
    """
        Extracts patient information from a DICOM dataset and returns a PatientInfo
         object.

        Handles anonymization if the patient name is missing or too long,
        and parses the birth date.

        :param ds: DICOM dataset.
        :return: A PatientInfo object with the extracted data.
        """

    patient_name = ds.get("PatientName", None)

    #TODO Need to optimise the below better!
    given = "Anonymous"
    family = "Anonymous"
    patient_id = "Anonymous"
    sex = "Anonymous"

    # If statement to return data - Correct the condition here
    if not patient_name or len(str(patient_name)) <= 20:
        given = getattr(patient_name, "given_name", "Unknown")
        family = getattr(patient_name, "family_name", "Unknown")
        patient_id = str(ds.get("PatientID", "Unknown"))
        sex = str(ds.get("PatientSex", "Unknown"))

    birth_date_str = ds.get("PatientBirthDate", "Unknown")

    if birth_date_str is not None:
        try:
            birth_date = datetime.strptime(birth_date_str, "%Y%m%d").date()
        except ValueError:
            birth_date = None
    else:
        birth_date = None

    return PatientInfo(
        given_name = given,
        family_name = family,
        patient_id=patient_id,
        sex=sex,
        birth_date=birth_date,
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

    image_type = getattr(ds, "ImageType", None)

    if isinstance(image_type, str):
        image_type_list = [image_type.strip().upper()]
    elif isinstance(image_type, (pydicom.multival.MultiValue, list)):
        image_type_list = [str(val).strip().upper() for val in image_type]
    else:
        raise ValueError(f"Unexpected ImageType format: {type(image_type)}")

    #checking to see if there are any Localizer images
    if "LOCALIZER" in image_type_list:
        raise ValueError("Skipping LOCALIZER image.")

    # for CT images: only keep AXIAL images
    modality = ds.get("Modality", "").upper()
    if modality == "CT" and "AXIAL" not in image_type_list:
        raise ValueError("Skipping non-AXIAL CT image.")

    #all tests passed
    return True
