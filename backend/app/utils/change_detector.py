from typing import List, Dict, Any

def detect_changes(db_obj: Any, new_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Compare existing SQLAlchemy object with new update data.
    Return list of dicts: {field_name, old_value, new_value}
    """
    changes = []

    for field, new_value in new_data.items():
        old_value = getattr(db_obj, field)

        # SQLAlchemy Date objects → str
        if hasattr(old_value, "isoformat"):
            old_value = old_value.isoformat()
        if hasattr(new_value, "isoformat"):
            new_value = new_value.isoformat()

        if old_value != new_value:
            changes.append({
                "field_name": field,
                "old_value": str(old_value) if old_value is not None else None,
                "new_value": str(new_value) if new_value is not None else None
            })

    return changes
