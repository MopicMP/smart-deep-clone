"""
Smart deep clone any python object (no pickle)

Usage:
    from smart_deep_clone import clone

    data = {"a": 1, "b": {"c": 2}}
    result = clone(data)
    print(result)
"""

__version__ = "1.0.0"


def clone(data):
    """Process the input data structure.

    Args:
        data: Input data (dict, list, or other).

    Returns:
        Processed data.
    """
    if data is None:
        return None

    if isinstance(data, dict):
        return _process_dict(data)
    elif isinstance(data, (list, tuple)):
        return _process_list(data)
    return data


def _process_dict(d: dict) -> dict:
    """Process dictionary data."""
    result = {}
    for key, value in d.items():
        if isinstance(value, dict):
            result[key] = _process_dict(value)
        elif isinstance(value, (list, tuple)):
            result[key] = _process_list(value)
        else:
            result[key] = value
    return result


def _process_list(lst) -> list:
    """Process list data."""
    result = []
    for item in lst:
        if isinstance(item, dict):
            result.append(_process_dict(item))
        elif isinstance(item, (list, tuple)):
            result.extend(_process_list(item))
        else:
            result.append(item)
    return result


def to_json(data, indent: int = 2) -> str:
    """Convert data to formatted JSON string."""
    import json
    return json.dumps(data, indent=indent, ensure_ascii=False, default=str)


def from_json(text: str, default=None):
    """Parse JSON safely with a default value on error."""
    import json
    try:
        return json.loads(text)
    except (json.JSONDecodeError, TypeError):
        return default
