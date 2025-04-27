"""
provides a read_dicom_file() function that takes a file path to a dicom file, checks if the
file is valid, and returns the FileDataset object. If the file is not valid it will return None.
"""

import logging
import pydicom
from pydicom.errors import InvalidDicomError

logger = logging.getLogger(__name__)  # Start logger


def read_dicom_file(file_path):
    """Read a dicom file in a fault tolerant way and return the FileDataset"""
    try:
        # Try standard dcm read
        dicom_file = pydicom.dcmread(file_path)
        logging.info("Successfully read DICOM file: %s", file_path)
        return dicom_file

    except FileNotFoundError as e:
        logger.error("File not found: %s - %s", file_path, str(e))
        return None

    except InvalidDicomError as e:
        logger.warning("File %s is not a valid DICOM file: %s",
                       file_path, str(e))
        try:
            # Try force reading file in case it is a DICOM file without a header
            dicom_file = pydicom.dcmread(file_path, force=True)
            logging.warning(
                "Successfully force-read DICOM file %s", file_path)
            return dicom_file
        except Exception as force_e:
            logging.error(
                "Failed to read %s (even with force): %s", file_path, str(force_e))
            return None

    except Exception as e:
        logging.error("Unexpected Error reading %s: %s", file_path, str(e))
        return None


dicom_file = read_dicom_file("Data/Sample_Dicom_File/0002.DCM")
print(dicom_file)
