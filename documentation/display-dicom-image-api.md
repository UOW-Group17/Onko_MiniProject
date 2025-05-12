# Displaying DICOM image on Screen API Documentation

## 1. Overview

A number of functions that take raw DICOM image data and convert it into a usable QImage for display in QT GUI sytems.

## 2. Components

### 2.1 dicom_utils.py

**Purpose:** To convert a normalized pixel array into a QImage for use in QT GUI systems.

**Key Method(s)**

```python
numpy_to_qimage(numpy_array) -> QImage
```

- Takes a normalized numpy array (in range [0, 1]), checks the validity of this array, and converts it into a QImage.

### 2.2 inputs_and_outputs.py

**Purpose:** To extract and normalize a DICOM image to a pixel array, then call numpy_to_qimage to generate a useable QImage.

**Key Method(s)**

```python
get_normalized_pixel_array(dicom_dataset) -> np.float32  # This is the type of the normalized pixel array
```

- This function will check if the dicom image data is a pixel array, and if so will normalize it's values to the range [0, 1] then return the array.

```python
def get_qimage_from_dicom_file(dicom_dataset) -> QImage
```

- This function is the main controller function for displaying images. It calls get_normalized_pixel_array and numpy_to_qimage, checks for common erros and returns the validated QImage.

## 3. Usage Guide

- The following example is part of a Pyside6 QtWidget class.

**Basic Operations**

```python
image = get_qimage_from_dicom_file(ds)
pixmap = QPixmap.fromImage(image)
self.image_label.setPixmap(pixmap)
self.image_label.setScaledContents(True)
```
