from datetime import datetime
from enum import Enum


try:
    from pydantic import (
        BaseModel,
        Field,
        ValidationError,
        model_validator
        )
except ImportError as err:
    print(f"Import error: {err}")
    print(
        "\n[Warning] Make sure venv is activated and pydantic is installed in "
        "before running the program"
        )
    print(
        "\nUsage:\npython3 -m venv venv\nsource venv/bin/activate"
        "\npip install pydantic\npip install mypy\npython3 alien_contact.py"
        "\npython -m mypy alien_contact.py"
        )
    exit(1)


class ContactType(Enum):
    radio = 'radio'
    visual = 'visual'
    physical = 'physical'
    telepathic = 'telepathic'


class AlienContact(BaseModel):
    contact_id: str = Field(..., min_length=5, max_length=15)
    timestamp: datetime = Field(...)
    location: str = Field(..., min_length=3, max_length=100)
    contact_type: ContactType = Field(...)
    signal_strength: float = Field(..., ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1140)
    witness_count: int = Field(ge=1, le=100)
    message_received: str | None = Field(default=None, max_length=500)
    is_verified: bool = Field(default=False)

    @model_validator(mode='after')
    def custom_validation(self) -> 'AlienContact':
        if not self.contact_id.startswith('AC'):
            raise ValueError(
                "Contact ID must start with \"AC\" (Alien Contact)"
                )
        if self.contact_type.value == 'physical':
            if not self.is_verified:
                raise ValueError("Physical contact reports must be verified")
        if self.contact_type.value == 'telepathic':
            if self.witness_count < 3:
                raise ValueError(
                    "Telepathic contact requires at least 3 witnesses"
                    )
        if self.signal_strength > 7.0:
            if self.message_received is None:
                raise ValueError(
                    "Strong signals (> 7.0) should include received messages"
                    )
        return self

    def show_info(self) -> None:
        print(f"ID: {self.contact_id}")
        print(f"Type: {self.contact_type.value}")
        print(f"Location: {self.location}")
        print(f"Signal: {self.signal_strength}/10")
        print(f"Duration: {self.duration_minutes} minutes")
        print(f"Witnesses: {self.witness_count}")
        print(f"Message: '{self.message_received}'")


def main() -> None:
    print("Alien Contact Log Validation")
    print("======================================")

    try:
        valid_contact_report: AlienContact = AlienContact(
            contact_id='AC_2024_001',
            timestamp=datetime.fromisoformat("2024-01-01T10:00:00"),
            location='Area 51, Nevada',
            contact_type=ContactType('radio'),
            signal_strength=8.5,
            duration_minutes=45,
            witness_count=5,
            message_received='Greetings from Zeta Reticuli'
        )

        print("Valid contact report:")
        valid_contact_report.show_info()

    except ValidationError as err:
        print("Expected validation error:")
        for error in err.errors():
            print(f"{error['msg'].replace('Value error, ', '')}")

    print("\n========================================")

    try:
        invalid_contact_report: AlienContact = AlienContact(
            contact_id='AC_2024_002',
            timestamp=datetime.fromisoformat("2024-01-02T10:00:00"),
            location='Area 51, Nevada',
            contact_type=ContactType('telepathic'),
            signal_strength=8.5,
            duration_minutes=45,
            witness_count=2,
            message_received='Greetings from Zeta Reticuli'
        )

        print("Invalid station created:")
        invalid_contact_report.show_info()

    except ValidationError as err:
        print("Expected validation error:")
        for error in err.errors():
            print(f"{error['msg'].replace('Value error, ', '')}")


if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        print(f"Unexpected error: {err}")
