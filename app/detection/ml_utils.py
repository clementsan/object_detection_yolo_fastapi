"""
Utility functions for detection module
"""

import json
from typing import Dict, Any

def convert_dict_to_json(object_dict: Dict[str, Any]) -> str:
    """Convert a dictionary to a JSON-formatted string"""

    # Convert to JSON string
    json_str = json.dumps(object_dict)

    return json_str
