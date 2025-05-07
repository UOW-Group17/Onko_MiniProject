"""Test file for the read_dicom_file.py functionality"""

import pytest
import logging
import os
import pydicom
from pydicom.dataset import Dataset, FileMetaDataset
from pydicom.uid import UID, ExplicitVRLittleEndian
from src.read_dicom_file import read_dicom_file


# Information about generating DICOM data can be found here;
# http://pydicom.github.io/pydicom/stable/auto_examples/input_output/plot_write_dicom.html#sphx-glr-auto-examples-input-output-plot-write-dicom-py

# Helper functions to create a simple test DICOM files
def create_valid_dicom(filename):
    """Create minimal valid DICOM file for testing"""
    file_meta = FileMetaDataset()
    file_meta.MediaStorageSOPClassUID = UID("1.2.840.10008.5.1.4.1.1.2")
    file_meta.MediaStorageSOPInstanceUID = UID("1.2.3")
    file_meta.ImplementationClassUID = UID("1.2.3.4")
    file_meta.TransferSyntaxUID = ExplicitVRLittleEndian

    ds = pydicom.dataset.FileDataset(
        filename, {}, file_meta=file_meta, preamble=b'\0'*128)
    ds.PatientName = "Test^Patient"
    ds.PatientID = "12345"

    # Transfer syntax
    ds.is_little_endian = True
    ds.is_implicit_VR = False

    ds.save_as(filename)



def create_headerless_dicom(filename):
    """Create a DICOM file without proper header metadata"""
    ds = pydicom.Dataset()
    
    # Patient information
    ds.PatientName = "HEADERLESS^TEST"
    ds.PatientID = "67890"
    
    # Study information
    ds.StudyInstanceUID = pydicom.uid.generate_uid()
    ds.SeriesInstanceUID = pydicom.uid.generate_uid()
    
    # SOP information
    ds.SOPClassUID = "1.2.840.10008.5.1.4.1.1.2"  # CT Image Storage
    ds.SOPInstanceUID = pydicom.uid.generate_uid()
    
    # Image information
    ds.Modality = "CT"
    ds.Rows = 10  # Must match your pixel data dimensions
    ds.Columns = 10  # Must match your pixel data dimensions
    ds.BitsAllocated = 8  # Important for pixel data interpretation
    ds.BitsStored = 8
    ds.HighBit = 7
    ds.PixelRepresentation = 0  # 0=unsigned, 1=signed
    ds.SamplesPerPixel = 1  # 1 for grayscale
    ds.PhotometricInterpretation = "MONOCHROME2"
    
    # Pixel data
    ds.PixelData = b"\x00" * 100  # 10x10 image with 8-bit pixels
    
    # Transfer syntax
    ds.is_little_endian = True
    ds.is_implicit_VR = False
    
    ds.save_as(filename)


class TestReadDicomFile:
    """ Test class for read_dicom_file"""

    @classmethod
    def setup_class(cls):
        """Create test files before all tests"""
        cls.valid_dcm = "valid_test.dcm"
        cls.headerless_dcm = "headerless_test.dcm"
        cls.invalid_dcm = "invalid_test.dcm"
        cls.empty_file = "empty_test.dcm"

        create_valid_dicom(cls.valid_dcm)
        create_headerless_dicom(cls.headerless_dcm)

        # Create an invalid DICOM file (just a text file)
        with open(cls.invalid_dcm, 'w') as f:
            f.write("This is not a DICOM file")

        # Create an empty file
        open(cls.empty_file, 'w').close()


    @classmethod
    def teardown_class(cls):
        """Clean up test files after all tests"""
        for f in [cls.valid_dcm, cls.headerless_dcm, cls.invalid_dcm, cls.empty_file]:
            if os.path.exists(f):
                os.remove(f)

    def test_read_valid_dicom(self):
        """Test reading a valid DICOM file"""
        result = read_dicom_file(self.valid_dcm)
        assert isinstance(result, Dataset)
        assert result.PatientName == "Test^Patient"
        assert result.PatientID == "12345"

    def test_read_headerless_dicom(self):
        """Test force-reading a headerless DICOM file"""
        result = read_dicom_file(self.headerless_dcm)
        assert isinstance(result, Dataset)
        assert result.PatientName == "HEADERLESS^TEST"
        assert result.PatientID == "67890"

    def test_invalid_dicom_file(self):
        """Test handling of invalid DICOM file"""
        result = read_dicom_file(self.invalid_dcm)
        assert result is None

    def test_empty_file(self):
        """Test handling of empty file"""
        result = read_dicom_file(self.empty_file)
        assert result is None

    def test_file_not_found(self):
        """Test handling of non existant file"""
        result = read_dicom_file("non_existant_file.dcm")
        assert result is None

if __name__ == '__main__':
    pytest.main()
