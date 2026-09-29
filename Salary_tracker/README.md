# Salary Tracker - Employee Management System

## Overview

`script.py` implements an **Employee management system** that tracks and manages employee information, including name, job level, and salary. The system enforces business logic rules through Python properties to ensure data integrity and prevent invalid salary/promotion operations.

## Purpose

This script provides a structured way to:
- Create and manage employee records with different job levels
- Track employee salaries based on predefined salary tiers
- Handle employee promotions with automatic salary updates
- Validate all changes to ensure business rules are followed
- Prevent downward demotions and invalid data entries

## Key Features

### 1. **Employee Class**
The core class that represents an employee with the following attributes:

#### Base Salary Structure
The system defines standard base salaries for different job levels:
- **Trainee**: $1,000
- **Junior**: $2,000
- **Mid-level**: $3,000
- **Senior**: $4,000

### 2. **Properties with Validation**

#### Name Property
- **Type**: String
- **Validation**: Ensures the name is always a string
- **Error Handling**: Raises `TypeError` if a non-string value is provided
- **Behavior**: Updates name and prints confirmation message

```python
charlie_brown.name = "Charlie Brown"  # ✓ Valid
charlie_brown.name = 123              # ✗ TypeError
```

#### Level Property
- **Type**: String (must be one of: 'trainee', 'junior', 'mid-level', 'senior')
- **Validations**:
  - Must be a valid level in the salary dictionary
  - Cannot be set to the same level twice
  - Cannot be demoted (lowered) to a lower level
  - Automatically updates the employee's salary when promoted
- **Error Handling**: Raises appropriate `TypeError` or `ValueError` exceptions
- **Behavior**: Prints promotion confirmation message

```python
charlie_brown.level = 'junior'     # ✓ Valid (promotion)
charlie_brown.level = 'trainee'    # ✗ ValueError: Cannot demote
charlie_brown.level = 'invalid'    # ✗ ValueError: Invalid level
```

#### Salary Property
- **Type**: Numeric (int or float)
- **Validations**:
  - Must be a number (int or float)
  - Cannot be set below the minimum salary for the employee's current level
- **Error Handling**: Raises `TypeError` for non-numeric values or `ValueError` for insufficient salary
- **Behavior**: Prints salary update confirmation message

```python
charlie_brown.salary = 2500        # ✓ Valid (above minimum)
charlie_brown.salary = 500         # ✗ ValueError: Below minimum
charlie_brown.salary = "invalid"   # ✗ TypeError
```

### 3. **String Representations**

#### `__str__()` Method
Returns a user-friendly string representation:
```python
print(charlie_brown)  # Output: Charlie Brown: trainee
```

#### `__repr__()` Method
Returns a developer-friendly representation that shows the constructor format:
```python
repr(charlie_brown)  # Output: Employee('Charlie Brown', 'trainee')
```

## Usage Example

The script includes a working example at the bottom:

```python
# Create a new employee at trainee level
charlie_brown = Employee('Charlie Brown', 'trainee')

# Display employee information
print(charlie_brown)                    # Charlie Brown: trainee
print(f'Base salary: ${charlie_brown.salary}')  # Base salary: $1000

# Promote employee to junior level
charlie_brown.level = 'junior'  # Output: 'Charlie Brown' promoted to 'junior'.
                                # Salary automatically updates to $2000
```

## Error Handling

The script implements robust error handling:

| Error Type | Scenario | Example |
|-----------|----------|---------|
| `TypeError` | Invalid name type | Setting `name` to a number |
| `TypeError` | Invalid level type | Setting `level` to a number |
| `TypeError` | Invalid salary type | Setting `salary` to a string |
| `ValueError` | Invalid job level | Setting `level` to 'boss' (not in dictionary) |
| `ValueError` | Duplicate level | Setting same level twice |
| `ValueError` | Demotion attempt | Promoting from 'senior' to 'junior' |
| `ValueError` | Insufficient salary | Salary below minimum for current level |

## Technical Highlights

### Design Patterns Used
- **Property Decorators**: Uses `@property` and `@<property>.setter` for encapsulation and validation
- **Class Variables**: Uses `_base_salaries` as a shared dictionary across all employees
- **Private Attributes**: Uses underscore prefix (`_name`, `_level`, `_salary`) for internal storage
- **Data Validation**: Implements validation at the setter level to ensure data integrity

### Why This Design?
1. **Encapsulation**: Properties provide controlled access to attributes
2. **Validation**: Business logic is enforced at the point of assignment
3. **Maintainability**: Changing salary tiers only requires updating one dictionary
4. **Scalability**: Easy to add new job levels or modify salary rules

## Potential Enhancements

- Add date tracking for promotion history
- Implement bonus/benefits system
- Add methods to calculate raises
- Export employee data to CSV/database
- Add department or team management
- Implement role-based salary adjustments
- Add performance rating system linked to salary





