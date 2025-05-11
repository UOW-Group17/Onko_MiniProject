import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime
from pydicom.dataset import Dataset
from pydicom.multival import MultiValue
from src import dicom_utils

#dummy class
class DummyPatient:
    def __init__(self, given_name=None, family_name=None):
        self.given_name = given_name
        self.family_name = family_name

#tests for extracting patient information
def test_extract_patient_info_anonymous():
    """THis method is for a dummy patient that has a UUID for a name"""
    ds = {
        "PatientName": "123e4567-e89b-12d3-a456-426614174000",  # Simulate UUID
        "PatientBirthDate": None,
        "Modality": "CT"
    }
    with patch("src.dicom_utils._is_uuid", return_value=True):
        info = dicom_utils.extract_patient_info(ds)
    assert info.given_name == "Anonymous"
    assert info.family_name == "Anonymous"
    assert info.patient_id == "Anonymous"
    assert info.sex == "Anonymous"
    assert info.birth_date is None
    assert info.modality == "CT"


def test_extract_patient_info_with_details():
    """This method is for a dummy patient with valid inputs"""
    ds = {
        "PatientName": DummyPatient(given_name="John", family_name="Doe"),
        "PatientID": "P123",
        "PatientSex": "M",
        "PatientBirthDate": "19800101",
        "Modality": "MR"
    }
    with patch("src.dicom_utils._is_uuid", return_value=False):
        info = dicom_utils.extract_patient_info(ds)
    assert info.given_name == "John"
    assert info.family_name == "Doe"
    assert info.patient_id == "P123"
    assert info.sex == "M"
    assert info.birth_date == datetime.strptime("19800101", "%Y%m%d").date()
    assert info.modality == "MR"

def test_extract_patient_info_invalid_birthdate():
    """This method is for a dummy patient with invalid inputs"""
    ds = {
        "PatientName": DummyPatient(given_name="Jane", family_name="Smith"),
        "PatientID": "P456",
        "PatientSex": "F",
        "PatientBirthDate": "notadate",
        "Modality": "CT"
    }
    with patch("src.dicom_utils._is_uuid", return_value=False):
        info = dicom_utils.extract_patient_info(ds)
    assert info.birth_date is None

def test_extract_patient_info_missing_fields():
    """This method is for a dummy patient with missing fields
    Namely the birthdate, also name is forced to not be a UUID"""
    ds = {}
    with patch("src.dicom_utils._is_uuid", return_value=True):
        info = dicom_utils.extract_patient_info(ds)
    assert info.given_name == "Anonymous"
    assert info.family_name == "Anonymous"
    assert info.patient_id == "Anonymous"
    assert info.sex == "Anonymous"
    assert info.birth_date is None
    assert info.modality == "Unknown"

def test_extract_patient_info_non_uuid_name():
    """Test extract_patient_info with a non-UUID PatientName"""
    ds = {
    "PatientName": MagicMock(given_name="John", family_name="Doe"),
    "PatientBirthDate": "19801001",
    "Modality": "CT",
    "PatientID": "JD123",
    "PatientSex": "M"
    }
    #No patching _is_uuid, needs to be treated as normal name
    info = dicom_utils.extract_patient_info(ds)
    assert info.given_name == "John"
    assert info.family_name == "Doe"
    assert info.patient_id == "JD123"
    assert info.sex == "M"
    assert info.birth_date == datetime.strptime("19801001", "%Y%m%d").date()
    assert info.modality == "CT"

#Anything below is tests for validate_dicom method

@pytest.mark.parametrize(
    #bunch of data that should pass as they have AXIAL, no localiser or CT
    "study_id, study_desc, image_type, modality, expected",
    [
        # Happy path: string ImageType, not LOCALIZER, not CT
        ("123", "desc", "SAGITTAL", "MR", True),
        # Happy path: MultiValue ImageType, not LOCALIZER, not CT
        ("456", "desc2", MultiValue(str, ["AXIAL", "SOMETHING"]), "MR", True),
        # Happy path: list ImageType, not LOCALIZER, not CT
        ("789", "desc3", ["AXIAL", "SOMETHING"], "MR", True),
        # Happy path: CT, AXIAL present
        ("321", "desc4", ["AXIAL", "SOMETHING"], "CT", True),
        # Happy path: CT, AXIAL present (case-insensitive)
        ("654", "desc5", ["axial", "other"], "ct", True),
    ],
    ids=[
        "string_ImageType_MR",
        "MultiValue_ImageType_MR",
        "list_ImageType_MR",
        "CT_AXIAL_present",
        "CT_AXIAL_present_case_insensitive",
    ]
)

def test_validate_dicom_happy_paths(study_id, study_desc, image_type, modality, expected):
    """Pytest function that verifies that dicom happy paths work, and will return
    true for a variety of valid dicom dataset senerios"""
    # Arrange
    ds = Dataset()
    ds.StudyID = study_id
    ds.StudyDescription = study_desc
    ds.ImageType = image_type
    ds.Modality = modality

    # Act
    result = dicom_utils.validate_dicom(ds)

    # Assert
    assert result is expected
    
@pytest.mark.parametrize(
    #Examples that are missing studyID || studyDescription
    "missing_field, expected_exc, expected_msg",
    [
        ("StudyID", ValueError, "Missing required DICOM fields: StudyID"),
        ("StudyDescription", ValueError, "Missing required DICOM fields: StudyDescription"),
    ],
    ids=["missing_StudyID", "missing_StudyDescription"]
)

def test_validate_dicom_missing_required_fields(missing_field, expected_exc, expected_msg):
    """This method raises an exception when required fields are missing"""
    # Arrange
    ds = Dataset()
    # sourcery skip: no-conditionals-in-tests
    if missing_field != "StudyID":
        ds.StudyID = "123"
    if missing_field != "StudyDescription":
        ds.StudyDescription = "desc"
    ds.ImageType = "AXIAL"
    ds.Modality = "MR"

    # Act & Assert
    with pytest.raises(expected_exc) as excinfo:
        dicom_utils.validate_dicom(ds)
    assert expected_msg in str(excinfo.value)

@pytest.mark.parametrize(
    "image_type, expected_exc, expected_msg",
    [
        ("LOCALIZER", ValueError, "Skipping LOCALIZER image."),
        (["LOCALIZER", "AXIAL"], ValueError, "Skipping LOCALIZER image."),
        (MultiValue(str, ["localizer", "axial"]), ValueError, "Skipping LOCALIZER image."),
    ],
    ids=["string_LOCALIZER", "list_LOCALIZER", "MultiValue_LOCALIZER"]
)

def test_validate_dicom_localizer_image(image_type, expected_exc, expected_msg):
    """This method raises an exception when image type is invalid"""
    # Arrange
    ds = Dataset()
    ds.StudyID = "123"
    ds.StudyDescription = "desc"
    ds.ImageType = image_type
    ds.Modality = "MR"

    # Act & Assert
    with pytest.raises(expected_exc) as excinfo:
        dicom_utils.validate_dicom(ds)
    assert expected_msg in str(excinfo.value)

@pytest.mark.parametrize(
   "image_type, modality, expected_exc, expected_msg",
    [
        (["SOMETHING"], "CT", ValueError, "Skipping non-AXIAL CT image."),
        (["CORONAL", "SOMETHING"], "CT", ValueError, "Skipping non-AXIAL CT image."),
        ("CORONAL", "CT", ValueError, "Skipping non-AXIAL CT image."),
        (MultiValue(str, ["CORONAL", "SOMETHING"]), "CT", ValueError, "Skipping non-AXIAL CT image."),
    ],
    ids=[
        "list_non_AXIAL_CT",
        "list_CORONAL_CT",
        "string_CORONAL_CT",
        "MultiValue_CORONAL_CT"
    ]
)

def test_validate_dicom_non_axial_ct(image_type, modality, expected_exc, expected_msg):
    """This test is testing the Skipping non-AXIAL CT image by putting something that is not AXIAL
    Also putting in multiple options per one"""
    # Arrange
    ds = Dataset()
    ds.StudyID = "123"
    ds.StudyDescription = "desc"
    ds.ImageType = image_type
    ds.Modality = modality

    # Act & Assert
    with pytest.raises(expected_exc) as excinfo:
        dicom_utils.validate_dicom(ds)
    assert expected_msg in str(excinfo.value)

@pytest.mark.parametrize(
    "image_type, expected_exc, expected_msg",
    [
        (123, ValueError, "Unexpected ImageType format: <class 'int'>"),
        (None, ValueError, "Unexpected ImageType format: <class 'NoneType'>"),
        (object(), ValueError, "Unexpected ImageType format: <class 'object'>"),
    ],
    ids=["int_ImageType", "None_ImageType", "object_ImageType"]
)

def test_validate_dicom_unexpected_image_type(image_type, expected_exc, expected_msg):
    """THis method tests to see if the image type is unexpected"""
    # Arrange
    ds = Dataset()
    ds.StudyID = "123"
    ds.StudyDescription = "desc"
    ds.ImageType = image_type
    ds.Modality = "CT"

    # Act & Assert
    with pytest.raises(expected_exc) as excinfo:
        dicom_utils.validate_dicom(ds)
    assert expected_msg in str(excinfo.value)

@pytest.mark.parametrize(
    "modality_value, expected",
    [
        ("", True),
        ("None", True),
        ("MR", True),
        ("ct", True),
    ],
    ids=["empty_modality", "none_modality", "MR_modality", "ct_modality"]
)
def test_validate_dicom_modality_edge_cases(modality_value, expected):
    """This test is testing the Modality fields, like empty strings, None and different case variation"""
    #Arrange
    ds = Dataset()
    ds.StudyID = "123"
    ds.StudyDescription = "desc"
    ds.ImageType = "AXIAL"
    ds.Modality = modality_value

    #Act
    result = dicom_utils.validate_dicom(ds)

    #Assert
    assert result == expected
