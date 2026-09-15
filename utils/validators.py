def non_empty(value, field="Value"):
    value = str(value).strip()
    if not value:
        raise ValueError(f"{field} cannot be empty.")
    return value

def positive_int(value, field="Value"):
    try:
        value = int(value)
    except ValueError:
        raise ValueError(f"{field} must be a whole number.")
    if value <= 0:
        raise ValueError(f"{field} must be greater than 0.")
    return value

def non_negative_int(value, field="Value"):
    try:
        value = int(value)
    except ValueError:
        raise ValueError(f"{field} must be a whole number.")
    if value < 0:
        raise ValueError(f"{field} cannot be negative.")
    return value

def positive_float(value, field="Value"):
    try:
        value = float(value)
    except ValueError:
        raise ValueError(f"{field} must be a number.")
    if value <= 0:
        raise ValueError(f"{field} must be greater than 0.")
    return value

def percentage(value):
    value = positive_float(value, "Percentage")
    if value > 100:
        raise ValueError("Percentage cannot exceed 100%.")
    return value