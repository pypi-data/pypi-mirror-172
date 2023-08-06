"""Helpers for preparing data by the receivers."""

import json
from collections.abc import MutableMapping
from typing import Any, Dict, Optional

import attr
from openedx_events.data import EventsMetadata


def _flatten(dictionary: MutableMapping, parent_key: str = "", sep: str = "_") -> Dict:
    """
    Generate a flat dictionary.

    Source: https://stackoverflow.com/a/6027615
    """
    items = []
    for key, value in dictionary.items():
        new_key = parent_key + sep + key if parent_key else key
        if isinstance(value, MutableMapping):
            items.extend(_flatten(value, new_key, sep=sep).items())
        else:
            items.append((new_key, value))
    return dict(items)


def prepare_data(data: Any, metadata: EventsMetadata, field_mapping: Optional[Dict] = None) -> Dict:
    """
    Convert data into the format expected by the Celery task.

    This performs the following operations:
    1. "Flatten" data to avoid nested structures.
    2. Apply an optional custom mapping.
    3. Parse data into JSON-serializable format.
    """
    flattened_data = _flatten(attr.asdict(data))
    if field_mapping is not None:
        flattened_metadata = _flatten(attr.asdict(metadata), "metadata")
        flattened_metadata = {
            field_mapping[key]: value for key, value in flattened_metadata.items() if key in field_mapping
        }
        flattened_data = {field_mapping[key]: value for key, value in flattened_data.items() if key in field_mapping}
        flattened_data = {**flattened_metadata, **flattened_data}
    else:
        # Include event name by default.
        flattened_data["event"] = metadata.event_type
    serialized_data = json.loads(json.dumps(flattened_data, default=str))

    return serialized_data
