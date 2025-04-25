"""
This file is used to open the dicom image, if it cant be opened it will throw errors
"""

import numpy as np
from dicom_utils import numpy_to_qimage

def dicom_image_opener(ds):
    """
    this method attempts to open a dicom image and convert it to a QImage.
    It uses the get_normalized_pixel_array function to extract and normalize the pixel data,
    and then numpy_to_qimage to convert it to a QImage
    if it doesn't work it throws errors
    :param ds: dicom set
    :return: either the image or nothing
    """
    try:
        pixels = get_normalized_pixel_array(ds)

        if pixels is None:
            raise ValueError("Failed to normalize pixel array")

        if qimage := numpy_to_qimage(pixels):
            return qimage
        raise ValueError("Failed to convert image to QImage")

    except AttributeError as e:
        raise ValueError("DICOM file is missing pixel data") from e
    except ValueError:
        raise  # Re-raise ValueError
    except Exception as e:
        raise RuntimeError("Error loading DICOM image") from e

# TODO Rename this here and in `dicom_image_opener`
def get_normalized_pixel_array(ds):
    """
    This function takes a DICOM dataset (ds) and extracts its pixel array.
    It then normalizes the pixel data to the range [0, 1] by dividing by the maximum pixel value,
    if that maximum value is not zero.
    The function returns the normalized pixel array as a NumPy array of float32.
    :param ds: Dicom dataset
    :return: the normalised pixel array
    """
    pixels = ds.pixel_array
    if not isinstance(pixels, np.ndarray):
        raise TypeError("Pixel array is not a numpy array")

    pixels = pixels.astype(np.float32)
    max_val = pixels.max()
    if max_val >= 1e-6:
        pixels /= max_val

    return pixels
