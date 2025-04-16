Team project to introduce students to the foundations for OnkoDICOM.

This is a PySide6 programme which starts and 
- determines if there is a preferences-configuration record, 
- if there is then it will read the configuration and continue. The kind of information stored is what is the default directory for the DICOM files to be found, etc. 
- The storage is held in a SQLite database.
- The programme is then to proceed to opening a DICOM Image file (e.g. a CT slice) in a fault tolerant way.
- And display the image
