import pytest
from unittest.mock import patch, MagicMock

from ntsecuritycon import DS_NAME_NO_ERROR
from numba.core.callconv import excinfo_ptr_t

from src import inputs_and_outputs

@pytest.mark.parametrize(
    "pixels, qimage, expected",
    [
        # Happy path
        ("pixel_data", "QImage_object", "QImage_object"),
    ],
    ids=["happy_path"]
)

def test_get_qimage_from_dicom_file_success(pixels, qimage, expected):
    """This module is getting the correct return value from the dicom file"""
    ds = MagicMock()
    with patch("src.inputs_and_outputs.get_normalized_pixel_array", return_value=pixels), \
         patch("src.inputs_and_outputs.numpy_to_qimage", return_value=qimage):
        result = inputs_and_outputs.get_qimage_from_dicom_file(ds)
        assert result == expected

@pytest.mark.parametrize(
    "pixels, expected_exc, expected_msg",
    [
        (None, ValueError, "Failed to normalize pixel array"),
    ],
    ids=["normalise_returns_none"],
)

def test_get_qimage_from_dicom_file_failure(pixels, expected_exc, expected_msg):
    """This method tests what happens when the get normalized pixel array returns none or an error"""
    # Arrange
    ds = MagicMock()
    with patch("src.inputs_and_outputs.get_normalized_pixel_array", return_value=pixels):
        # Act & Assert
        with pytest.raises(expected_exc) as excinfo:
            inputs_and_outputs.get_qimage_from_dicom_file(ds)
        assert expected_msg in str(excinfo.value)

@pytest.mark.parametrize(
    "pixels, qimage, expected_exc, expected_msg",
    [
        # Edge case: numpy_to_qimage returns None
        ("pixels_array", None, ValueError, "Failed to convert image to QImage"),
    ],
    ids=["qimage_returns_none"]
)

def test_get_qimage_from_dicom_file_qimage_none(qimage, pixels, expected_exc, expected_msg):
    """This method is for checking rhe get_qimage_from_dicom_files returns an error when numpy_for qimage returns nothing is returned """
    # Arrange
    ds = MagicMock()
    with patch("src.inputs_and_outputs.get_normalized_pixel_array", return_value=pixels), \
         patch("src.inputs_and_outputs.numpy_to_qimage", return_value=qimage):

        # Act & Assert
        with pytest.raises(expected_exc) as excinfo:
            inputs_and_outputs.get_qimage_from_dicom_file(ds)
        assert expected_msg in str(excinfo.value)

def test_get_qimage_from_dicom_file_att_error():
    """This method checks that the get_qimage_from_dicom_file raises an error if there is no pixel data"""
    dis = MagicMock()
    with patch("src.inputs_and_outputs.get_normalized_pixel_array",
               side_effect=AttributeError("no pixel data")):
        with pytest.raises(ValueError) as excinfo:
            inputs_and_outputs.get_qimage_from_dicom_file(dis)
            assert "DICOM file is missing pixel data" in str(excinfo.value)

def test_get_qimage_from_dicom_files_value_error():
    """This method checks that get_qimage_from_dicom_file raises an error keeps the Value error raised by get_normalised_pixel_array
    and that the error message is kept"""
    #Arrange
    ds = MagicMock()
    with patch("src.inputs_and_outputs.get_normalized_pixel_array",side_effect=ValueError("bad value")):
        with pytest.raises(ValueError) as excinfo:
            inputs_and_outputs.get_qimage_from_dicom_file(ds)
            assert "bad value" in str(excinfo.value)

def test_get_qimage_from_dicom_file_unexpected_exception():

    # arrange
    ds = MagicMock()
    with patch("src.inputs_and_outputs.get_normalized_pixel_array",
               side_effect=RuntimeError("unexpected error")):
        with pytest.raises(RuntimeError) as excinfo:
            inputs_and_outputs.get_qimage_from_dicom_file(ds)
            assert "unexpected error" in str(excinfo.value)
            assert "Error loading DICOM file" in str(excinfo.value.__cause__)
