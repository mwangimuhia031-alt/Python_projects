# User Configuration Manager

A small Python project for managing user preferences such as theme, language, notifications, and volume.

## Features

- Add a new setting
- Update an existing setting
- Delete a setting
- View all current settings
- Normalize setting keys and values to lowercase
- Return clear success and error messages

## Functions

### `add_setting(settings, item)`

Adds a key-value pair to the settings dictionary. The key and value are converted to lowercase. Existing keys are not overwritten.

### `update_setting(settings, item)`

Updates the value of an existing setting. The key and value are converted to lowercase. Missing settings are reported without changing the dictionary.

### `delete_setting(settings, key)`

Deletes a setting by key. The key is converted to lowercase before lookup.

### `view_settings(settings)`

Displays all settings with capitalized keys. Empty dictionaries return `No settings available.`

## Example

```python
test_settings = {
    "theme": "dark",
    "language": "english"
}

add_setting(test_settings, ("NOTIFICATIONS", "ENABLED"))
# "Setting 'notifications' added with value 'enabled' successfully!"

update_setting(test_settings, ("THEME", "LIGHT"))
# "Setting 'theme' updated to 'light' successfully!"

print(view_settings(test_settings))
```

Output:

```text
Current User Settings:
Theme: light
Language: english
Notifications: enabled
```

## Running the Project

Open `User_configuration_manager.ipynb` in VS Code or Jupyter and run the Python code cell. The notebook contains the implementation and the `test_settings` dictionary used for testing.

## Requirements

- Python 3.x
- Jupyter Notebook or VS Code with the Jupyter extension
