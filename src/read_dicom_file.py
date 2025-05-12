"""
provides a read_dicom_file() function that takes a file path to a dicom file, checks if the
file is valid, and returns the FileDataset object. If the file is not valid it will return None.
"""

import logging
import os
import pydicom
from pydicom.errors import InvalidDicomError

logger = logging.getLogger(__name__)  # Start logger

def read_dicom_file(file_path):
    """Read a DICOM file, return None if invalid or empty."""
    try:
        # Check for empty file first
        if os.path.getsize(file_path) == 0:
            logger.warning("Empty file: %s", file_path)
            return None
            
        # Try standard read
        dicom_file = pydicom.dcmread(file_path)

        logger.info("Successfully read DICOM file: %s", file_path)
        return dicom_file

    except FileNotFoundError as e:
        logger.error("File not found: %s - %s", file_path, str(e))
        return None

    except InvalidDicomError as e:
        logger.warning("File %s is not a valid DICOM part 10 file: %s", file_path, str(e))
        try:
            # Try force-reading
            dicom_file = pydicom.dcmread(file_path, force=True)

            # Check if file  has a required attribute
            if not hasattr(dicom_file, 'SOPClassUID'):
                logger.error("File lacks required DICOM fields: %s", file_path)
                return None

            logger.warning("Successfully force-read DICOM file %s", file_path)
            return dicom_file
        except Exception as force_e:
            logger.error("Failed to read %s (even with force): %s", file_path, str(force_e))
            return None

    except Exception as e:
        logger.error("Unexpected error reading %s: %s", file_path, str(e))
        return None

