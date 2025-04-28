# Opening a DICOM file (read_dicom_file.py)

This is handled by the **read_dicom_file.py** file that adds a utility function to the program that attempts to read and subsequently open the specified .dcm file while handling the potential errors thrown. If successful the ‘FileDataset’ is returned, otherwise None is returned. All error information is logged during file processing.

## Some issues and related troubleshooting for opening DICOM files:

**Invalid DICOM file:** The file attempting to be opened is not a .dcm file despite appearing as such. 
Troubleshooting: Verify the origin of the file, ensuring it’s from a reputable source. Check file size, as unusually small files may indicate corruption. If possible, use appropriate tool to examine the file header, as a valid DICOM file usually has a specific preamble and a "DICM" magic number at a certain offset.

**Corrupt DICOM file:** File damaged during processing/updating, storage or transfer.
Troubleshooting: If possible, try and get a new copy of the file from the source. If obtained via network access, ensure the file integrity and no packet loss or errors occurred during transfer.

**Incorrect or missing DICOM Tags:** DICOM files use a standardised set of tags to store information within the file such as image data, patient name, modality etc. If certain essential tags are missing or incorrect, the file may not be interpreted correctly and thus fail to open.
Troubleshooting: Use and appropriate to analyse the DICOM file and discover incorrect tags. Refer to the DICOM standard to cross check tags for the various Information Object Definitions (IODs), to help identify any issues.

## Utility Function Error Handling

**FileNotFound** - returns None and passes control back to the calling class or function, logging the error with the error type and file path that caused the error.

**InvalidDicomError** - initially logs a warning to the user that file is not a valid DICOM file. After which the function attempts to force read the DICOM file to circumvent missing file header information. If successful, a warning is logged stating the file was successfully read, and a ‘FileDataset’ object is returned. If unsuccessful, the error is logged stating the file was not read with None returned and control passed back to the calling class or function. 

**Exception** - logs error message stating that an unexpected error has occurred and simply returns None, passing control back to the calling class or function.

## Drawbacks

This utility function does not provide an alternative course of action for the user should the file fail to be read or opened. User options need to be handled by the calling class or function. As an example, if the ‘FileNotFound’ error is thrown the user may like to select another file or file path to open. However, this alternative action will need to be handled outside of read_dicom_file function as it only returns the None value to indicate failure.


## Architecture

This function should be called from the main program or other such class or function that utilises the ‘FileDataset’ object returned from the DICOM file to obtain and display the related information where and as required.
