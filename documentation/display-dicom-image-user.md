# Displaying DICOM images in a PySide6 GUI (inputs_and_outputs.py, dicom_utils.py)

The DICOM image display system provides conversion of raw DICOM pixel data into displayable QImage format for use in QT GUI applications. These components work together to handle DICOM file processing, pixel array normalization, and image format conversion.

## Common Issues and Troubleshooting

**Invalid DICOM Format:** The system may fail to process files that don't contain valid pixel data. This typically occurs with non-image DICOM files or corrupted datasets. Troubleshooting involves verifying the DICOM contains 'PixelData' attribute.

**Dimension Errors:** The system requires 2D image arrays. Multi-frame DICOMs will be rejected. Troubleshooting requires pre-processing 3D datasets into individual slices before display.

## System Behaviour and Error Handling

**Normalization Failures:** When pixel array normalization fails, the system raises specific ValueErrors with detailed messages about the nature of the failure (missing data, invalid ranges, etc.). The system includes automatic scaling to [0, 1] range but will fail explicitly if the maximum pixel value is zero.

**QImage Conversion Errors:** Failed conversions to QImage format generate clear exceptions about array dimensions or type mismatches. The system validates array shape (must be 2D) and data type (must be convertible to uint8) before conversion attempts.

## Limitations

The current implementation only supports grayscale single-frame DICOM images. Color images and multi-frame DICOMs require pre-processing. The normalization process assumes typical medical imaging value ranges - specialized modalities with unusual ranges may not be supported. The system has a hard requirement for 2D arrays which limits direct display of volumetric data.

## Architectural Considerations

The display system follows a pipeline architecture with clear separation between extraction, normalization, and conversion stages. This design allows for modular enhancement of individual processing steps.

The extraction layer handles all DICOM-specific operations including pixel array validation. The normalization layer manages value scaling and range validation. The conversion layer transforms the processed array into Qt-compatible image format. The system is designed to be called from GUI components requiring DICOM display, returning either a ready-to-use QImage or detailed error information when processing fails. The strict separation between DICOM operations and display conversion allows for future support of additional image formats without affecting the core display functionality.
