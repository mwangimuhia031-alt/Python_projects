# Medical Data Validator

This project validates the structure and basic content of a collection of medical records. The implementation is in [`script.py`](script.py).

## Purpose

A medical record is expected to be a dictionary with a fixed set of fields:

- `patient_id`
- `age`
- `gender`
- `diagnosis`
- `medications`
- `last_visit_id`

The validator checks both the outer collection and every individual record. It reports invalid records and returns a Boolean result:

- `True` when all records are valid
- `False` when the input format or any field value is invalid

This is a format and basic consistency validator. It does not verify whether a diagnosis is medically correct or whether a medication is appropriate for a patient.

## Validation Rules

| Field | Rule |
| --- | --- |
| `patient_id` | Must be a string matching `p` followed by one or more digits, such as `P1001`. Matching is case-insensitive. |
| `age` | Must be an integer greater than or equal to 18. |
| `gender` | Must be the string `male` or `female`, ignoring letter case. |
| `diagnosis` | Must be a string or `None`. |
| `medications` | Must be a list containing only strings. An empty list is allowed. |
| `last_visit_id` | Must be a string matching `v` followed by one or more digits, such as `V2301`. Matching is case-insensitive. |

The complete input must be a list or tuple. Every item in that collection must be a dictionary with exactly the six required keys. Extra keys and missing keys are rejected.

## How the Code Works

### 1. Store the sample data

`medical_records` contains example records. It demonstrates that identifiers may use either uppercase or lowercase letters while still following the same format.

### 2. Validate individual fields

`find_invalid_records()` receives one record through keyword arguments. It builds a `constraints` dictionary where each key is a field name and each value is the result of that field's validation rule.

For example:

```python
'age': isinstance(age, int) and age >= 18
```

The function returns the names of all fields whose constraints are false. Returning field names makes it possible for the caller to produce a useful error message instead of only returning a generic failure.

Regular expressions are used for the identifier fields:

- `r'p\d+'` validates patient IDs.
- `r'v\d+'` validates visit IDs.

The `re.IGNORECASE` flag permits either uppercase or lowercase prefixes.

### 3. Validate the outer collection

`validate()` first checks that the input is a list or tuple. It then loops through the records with `enumerate()` so error messages can identify the record position.

For each item it checks, in order:

1. The item is a dictionary.
2. Its keys exactly match the expected key set.
3. Its values pass `find_invalid_records()`.

The `is_invalid` flag records whether any problem has been found. The loop continues after an error so multiple invalid records can be reported in one run.

### 4. Return the final result

After all records have been examined:

- If `is_invalid` is `True`, the function returns `False`.
- Otherwise, it prints `Valid format.` and returns `True`.

A key part of the implementation is assigning field-level failures back to the overall result:

```python
if invalid_records:
    is_invalid = True
```

Without this step, invalid field values would be detected but ignored by `validate()`.

## Logical Development Steps

The code can be created and reasoned about in the following sequence:

1. Define the expected shape of one medical record.
2. Create representative sample records, including different capitalization styles.
3. Decide the validation rule for each field before writing the function.
4. Implement the field checks in one function so the rules are centralized.
5. Return invalid field names to make failures diagnosable.
6. Validate the outer collection type before iterating over it.
7. Check that every item is a dictionary.
8. Compare each dictionary's keys with one shared expected key set.
9. Pass validly shaped dictionaries to the field validator using `**dictionary`.
10. Mark the complete input invalid whenever any field check fails.
11. Continue checking the remaining records so the user receives all available errors.
12. Run the validator with both valid and deliberately invalid data.

This order moves from broad structural checks to specific value checks. It also prevents `find_invalid_records()` from receiving an unexpected set of keyword arguments when a record has missing or extra keys.

## Running the Validator

From the project directory, run:

```text
python script.py
```

The included sample data produces:

```text
Valid format.
```

To test a failure, call `validate()` with a record such as:

```python
invalid_records = [
    {
        'patient_id': 'bad-id',
        'age': 17,
        'gender': 'Female',
        'diagnosis': 'Asthma',
        'medications': ['Albuterol'],
        'last_visit_id': 'V2303',
    }
]

validate(invalid_records)
```

The result is `False`, and the validator reports `patient_id` and `age` as invalid.

## Possible Extensions

For a larger application, the validator could be extended to:

- Return structured errors instead of printing messages.
- Validate duplicate patient or visit identifiers.
- Add explicit upper and lower age limits.
- Validate that medication names are non-empty.
- Use a testing framework such as `unittest` or `pytest`.
- Load records from JSON or a database instead of hard-coded data.
- Add domain-specific checks without mixing them into the basic format checks.
