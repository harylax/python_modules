from datetime import datetime
from enum import Enum
import json
from pathlib import Path


try:
    from pydantic import BaseModel, Field, ValidationError, model_validator
except ImportError:
    print("Pydantic not installed\n")
    print("Usage:")
    print("\tpython3 -m venv venv")
    print("\tsource venv/bin/activate")
    print("\tpip install pydantic")
    exit(1)


class ContactType(str, Enum):
    radio = "radio"
    visual = "visual"
    physical = "physical"
    telepathic = "telepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(..., min_length=5, max_length=15)
    timestamp: datetime = Field(...)
    location: str = Field(..., min_length=3, max_length=100)
    contact_type: ContactType = Field(...)
    signal_strength: float = Field(..., ge=0.0, le=10.0)
    duration_minutes: int = Field(..., ge=1, le=1440)
    witness_count: int = Field(..., ge=1, le=100)
    message_received: str | None = Field(default=None, max_length=500)
    is_verified: bool = Field(default=False)

    @model_validator(mode='after')
    def validate_rules(self) -> 'AlienContact':
        if not self.contact_id.startswith('AC'):
            raise ValueError("Contact ID must start with \"AC\"")
        if self.contact_type == ContactType.physical and not self.is_verified:
            raise ValueError("Physical contact reports must be verified")
        if self.contact_type == ContactType.telepathic \
                and self.witness_count < 3:
            raise ValueError(
                "Telepathic contact requires at least 3 witnesses"
                )
        if self.signal_strength > 7.0:
            if self.message_received is None:
                raise ValueError(
                    "Strong signals (> 7.0) should include received messages"
                    )
        return self


def main() -> None:
    print("Alien Contact Log Validation")
    print("======================================")
    contact = AlienContact(
        contact_id="AC_2024_001",
        timestamp=datetime.fromisoformat("2024-01-21T07:10:00"),
        contact_type=ContactType.radio,
        location="Area 51, Nevada",
        signal_strength=8.5,
        duration_minutes=45,
        witness_count=5,
        message_received='Greetings from Zeta Reticuli'
    )
    print("Valid contact report:")
    print(f"ID: {contact.contact_id}")
    print(f"Type: {contact.contact_type.value}")
    print(f"Location: {contact.location}")
    print(f"Signal: {contact.signal_strength}/10")
    print(f"Duration: {contact.duration_minutes} minutes")
    print(f"Witnesses: {contact.witness_count}")
    print(f"Message: {contact.message_received}")
    print("\n======================================")
    try:
        AlienContact(
            contact_id="AC_2024_002",
            timestamp=datetime.fromisoformat("2024-02-21T07:10:00"),
            contact_type=ContactType.telepathic,
            location="Area 51, Nevada",
            signal_strength=7.5,
            duration_minutes=55,
            witness_count=2,
            message_received='Hello world'
        )
    except ValidationError as err:
        print("Expected validation error:")
        for error in err.errors():
            print(f"{error['msg']}")
    try:
        json_path = Path("generated_data/alien_contacts.json")
        with open(json_path) as f:
            data_dict: dict = json.load(f)
    except OSError as err:
        print("\n========================================")
        print(f"Could not load generated data: {err}")
        print("Usage: from the root")
        print("\tpython3 data_exporter.py")
        print("\tpython3 ex0/space_station.py")
        return
    print("Validation of generated data")
    print("\n========================================")
    for data in data_dict:
        try:
            c = AlienContact(**data)
            print(f"\t[OK] ID:\t\t{c.contact_id}")
            print(f"\t[OK] Timestamp:\t\t{c.timestamp}")
            print(f"\t[OK] Type:\t\t{c.contact_type.value}")
            print(f"\t[OK] Location:\t\t{c.location}")
            print(f"\t[OK] Signal:\t\t{c.signal_strength}")
            print(f"\t[OK] Duration:\t\t{c.duration_minutes}")
            print(f"\t[OK] Witnesses:\t\t{c.witness_count}")
            print(f"\t[OK] Message:\t\t{c.message_received}")
            print()
        except ValidationError as err:
            for error in err.errors():
                print(f"{data} validation error: {error['msg']}")


if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        print(f"Unexpected error: {err}")
