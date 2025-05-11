# Saving and reading user-preferences (user_pref_controller.py, user_pref_interface.py, user_pref_model.py)

The user preferences system provides persistant storage of applcation settings through a dedicated database utility. These componenets work together to create an maintain a SQLite database that securely stores user preferences in a hidden directory within the user's home folder, with cross platform support for Windows, macOS, and Linux systems.

## Common Issues and Troubleshooting

**Database Initialization Failure:** The system may fail to create the required database files during first-time setup. This typically occurs due to insufficient permissions in the home directory or conflicts with existing files. Troubleshoting involves verifying write permissions in the home directory and esuring no existing '.onko' directory is present that might cause conflicts. (Remember that you need to set hidden files to visible to check this).

**Path Validation Errors:** When saving preferences, the system calidates directory paths for existence and proper formatting. Invalid paths may be rejected if they exceed maximum length limitations (200 characters) or contain unsupported characters. Troubleshooting requires checking the path for special characters and ensuring it points to an existing, acessible location.

## System Behavior and Error Handling

**Database Connection Errors:** When database connections fail, the system logs detailed error information and raises appropriate exceptions. Failed connections typically result from filesystem permissions or database corruption. The system implements automatic retry logic for transient errors while providing clear feedback for persistent issues.

**Unexpected Errors:** The system includes comprehensive exception handling at all levels, from database operations to filesystem interactions. Unexpected errors are captured and logged.

## Limitations

The current implementation focuses on storing a single default directory preference per user. More complex preference structure would require database schema modifications. Some edge case errors may require manual intervention. For example, database corruption would require deleting and recreating the preferences database. The hidden nature of the storage directory would prevent accidental modifications but may complicate troubleshooting for less technical users.

## Architectural Considerations

The preference system follows a MVC architecture, with separation between the model (database operations), controller (business logic), and interface (API contracts). This design allows for much easier extension and maintnenance.

The model layer handles all direct database interactions, including table creation, data validation, and transaction management. The controller coordinates between the model and other application components, implementing business logic for preference management. The interface layer defines the public API contract, esuring consistent access to preference functionality throughout the application. This abstraction allows for potential future changes to the storage mechanism without affecting dependant code. The system is designed to be called from the main application or other components requiring access to user preferences, returning either the requested preference data or appropriate error indicators when operations fail.
