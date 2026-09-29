# Employee Class Documentation

## Overview

The `Employee` class is a Python implementation that manages employee information including name, job level, and salary. It demonstrates the use of **properties with custom setters** for validation and encapsulation, ensuring data integrity through defined business rules.

## Features

- **Encapsulation**: Uses private attributes (`_name`, `_level`, `_salary`) with property decorators for controlled access
- **Validation**: Custom setters validate input types and enforce business logic
- **Level-based Salaries**: Maintains predefined minimum salaries for different job levels
- **Error Handling**: Raises appropriate exceptions (`TypeError`, `ValueError`) with descriptive messages
- **User Feedback**: Prints confirmation messages when attributes are successfully updated

## Class Attributes

### `_base_salaries` (Dictionary)

A class-level dictionary defining the minimum salary for each job level:

```python
_base_salaries = {
    'trainee': 1000,
    'junior': 2000,
    'mid-level': 3000,
    'senior': 4000,
}
```

These values serve as the baseline salaries and validation thresholds for each level.

## Instance Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `_name` | str | The employee's name (private) |
| `_level` | str | The employee's job level (private) |
| `_salary` | int/float | The employee's salary (private) |

## Methods and Properties

### `__init__(name, level)`

**Constructor** - Initializes a new Employee instance.

**Parameters:**
- `name` (str): The employee's name
- `level` (str): The employee's initial job level (must be a key in `_base_salaries`)

**Example:**
```python
charlie_brown = Employee('Charlie Brown', 'trainee')
```

**Behavior:**
- Sets the name using the `name` property setter (triggers validation)
- Sets the level using the `level` property setter (triggers validation)
- Automatically assigns the base salary for the given level

### `__str__()`

Returns a string representation of the employee.

**Returns:** `"{name}: {level}"` (e.g., `"Charlie Brown: trainee"`)

### `__repr__()`

Returns a formal string representation suitable for debugging.

**Returns:** `"Employee('{name}', '{level}'"` (e.g., `"Employee('Charlie Brown', 'trainee')"`)

### `name` Property

**Getter:**
```python
@property
def name(self):
    return self._name
```
Returns the employee's name.

**Setter:**
```python
@name.setter
def name(self, new_name):
```

Validates and updates the employee's name.

**Validation Rules:**
- `new_name` must be a string
- Raises `TypeError` if not a string with message: `"'name' must be a string."`

**Side Effects:**
- Prints confirmation message: `"'name' updated to '{self.name}'."`

**Example:**
```python
charlie_brown.name = 'Charlie'  # Valid
charlie_brown.name = 123        # Raises TypeError
```

### `level` Property

**Getter:**
```python
@property
def level(self):
    return self._level
```
Returns the employee's current job level.

**Setter:**
```python
@level.setter
def level(self, new_level):
```

Validates and updates the employee's job level (promoting the employee).

**Validation Rules:**
1. `new_level` must be a string
   - Raises `TypeError`: `"'level' must be a string."`

2. `new_level` must be a valid key in `_base_salaries`
   - Raises `ValueError`: `"Invalid value '{new_level}' for 'level' attribute."`

3. `new_level` cannot be the same as the current level (uses `hasattr()` to check if `_level` exists)
   - Raises `ValueError`: `"'{self._level}' is already the selected level."`

4. `new_level` cannot be a lower level than the current level (uses `hasattr()` to check if `_level` exists)
   - Raises `ValueError`: `"Cannot change to lower level."`

**Side Effects:**
- Prints promotion message: `"'{self.name}' promoted to '{new_level}'."`
- Automatically updates the salary to the new level's base salary

**Example:**
```python
charlie_brown.level = 'junior'     # Valid promotion
charlie_brown.level = 'trainee'    # Raises ValueError (lower level)
charlie_brown.level = 'junior'     # Raises ValueError (already junior)
```

### `salary` Property

**Getter:**
```python
@property
def salary(self):
    return self._salary
```
Returns the employee's current salary.

**Setter:**
```python
@salary.setter
def salary(self, new_salary):
```

Validates and updates the employee's salary with a minimum threshold.

**Validation Rules:**
1. `new_salary` must be a number (int or float)
   - Raises `TypeError`: `"'salary' must be a number."`

2. `new_salary` must be at least the base salary for the current level (uses `hasattr()` to check if `_level` exists, avoiding `AttributeError` during initialization)
   - Raises `ValueError`: `"Salary must be higher than minimum salary ${base_salary}."`

**Side Effects:**
- Prints confirmation message: `"Salary updated to ${new_salary}."`

**Example:**
```python
charlie_brown.salary = 1500   # Valid (above trainee minimum of 1000)
charlie_brown.salary = 500    # Raises ValueError (below minimum)
charlie_brown.salary = "high" # Raises TypeError
```

## Important Design Pattern: `hasattr()` Usage

The class uses `hasattr(self, '_level')` checks in the `level` and `salary` setters to prevent `AttributeError` during initialization. This is crucial because:

- During `__init__`, when the first assignment occurs (`self.name = name`), the `_level` attribute doesn't exist yet
- Using `hasattr()` allows setters to skip validation that depends on existing attributes during the initialization phase
- After `__init__` completes, all attributes exist and full validation applies

## Usage Example

```python
# Create a new employee at trainee level
charlie_brown = Employee('Charlie Brown', 'trainee')
print(charlie_brown)                    # Output: Charlie Brown: trainee
print(f'Base salary: ${charlie_brown.salary}')  # Output: Base salary: $1000

# Promote to junior level
charlie_brown.level = 'junior'
# Output: 'Charlie Brown' promoted to 'junior'.
#         Salary updated to $2000.

# Update salary within valid range
charlie_brown.salary = 2500
# Output: Salary updated to $2500.

# Attempt invalid operations
charlie_brown.level = 'trainee'  # Raises ValueError: Cannot change to lower level.
charlie_brown.salary = 1000      # Raises ValueError: Salary must be higher than minimum salary $2000.
```

## Error Handling Summary

| Error Type | Condition | Message |
|------------|-----------|---------|
| `TypeError` | Non-string name | `"'name' must be a string."` |
| `TypeError` | Non-string level | `"'level' must be a string."` |
| `TypeError` | Non-numeric salary | `"'salary' must be a number."` |
| `ValueError` | Invalid level | `"Invalid value '{level}' for 'level' attribute."` |
| `ValueError` | Same level promotion | `"'{level}' is already the selected level."` |
| `ValueError` | Demotion attempt | `"Cannot change to lower level."` |
| `ValueError` | Salary below minimum | `"Salary must be higher than minimum salary ${minimum}."` |

## Best Practices Demonstrated

1. **Encapsulation**: Private attributes with property decorators protect internal state
2. **Validation**: Input validation occurs at the setter level, not the user level
3. **Immutability Patterns**: Properties allow read-only or controlled-write access
4. **Defensive Programming**: Using `hasattr()` to check attribute existence before using them
5. **Clear Error Messages**: Exceptions include context to help users understand what went wrong
6. **User Feedback**: Print statements confirm successful operations
7. **Type Safety**: Explicit type checking for critical attributes
8. **Business Logic**: Enforces real-world constraints (no demotions, salary minimums, etc.)

## Common Pitfalls

- **Attempting to demote**: The class prevents level downgrades
- **Setting salary below minimum**: Each level has a required minimum salary
- **Direct attribute access**: Avoid using `employee._name` directly; use properties instead
- **Passing wrong types**: Always pass strings for `name` and `level`, numbers for `salary`
