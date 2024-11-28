from dataclasses import dataclass


@dataclass
class Device:
    device_id: str
    brand: str
    model: str
    os: str
    location: Dict[str, float]



