from dataclasses import dataclass
from typing import Dict


@dataclass
class Device:
    id: str
    name: str
    brand: str
    model: str
    os: str
    location: Dict[str, float]


