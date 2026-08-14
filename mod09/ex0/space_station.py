from datetime import datetime

try:
    from pydantic import BaseModel, Field, ValidationError
except ImportError as err:
    print(f"Import error: {err}")
    print(
        "\n[Warning] Make sure venv is activated and pydantic is installed in"
        "before running the program"
        )
    print(
        "\nUsage:\npython3 -m venv venv\nsource venv/bin/activate"
        "\npip install pydantic\npip install mypy\npython3 space_station.py"
        "\npython -m mypy space_station.py"
        )
    exit(1)


class SpaceStation(BaseModel):
    station_id: str = Field(..., min_length=3, max_length=10)
    name: str = Field(..., min_length=1, max_length=50)
    crew_size: int = Field(..., ge=1, le=20)
    power_level: float = Field(..., ge=0.0, le=100.0)
    oxygen_level: float = Field(..., ge=0.0, le=100.0)
    last_maintenance: datetime = Field(...)
    is_operational: bool = Field(default=True)
    notes: str | None = Field(default=None, max_length=200)

    def show_info(self) -> None:
        print(f"ID: {self.station_id}")
        print(f"Name: {self.name}")
        print(f"Crew: {self.crew_size} people")
        print(f"Power: {self.power_level}%")
        print(f"Oxygen: {self.oxygen_level}%")
        status: str = (
            'Operational'
            if self.is_operational
            else 'Unoperational'
            )
        print(f"Status: {status}")


def main() -> None:
    print("Space Station Data Validation")
    print("========================================")

    try:
        valid_space_station: SpaceStation = SpaceStation(
            station_id='ISS001',
            name='International Space Station',
            crew_size=6,
            power_level=85.5,
            oxygen_level=92.3,
            last_maintenance=datetime.fromisoformat("2026-07-01T09:29:00"),
            is_operational=True,
            notes="N/A"
        )

        print("Valid station created:")
        valid_space_station.show_info()

    except ValidationError as err:
        print("Expected validation error:")
        for error in err.errors():
            print(f"{error['msg']}")

    print("\n========================================")

    try:
        invalid_space_station: SpaceStation = SpaceStation(
            station_id='ISS001',
            name='International Space Station',
            crew_size=22,
            power_level=85.5,
            oxygen_level=92.3,
            last_maintenance=datetime.fromisoformat("2026-07-01T09:29:00"),
            is_operational=True,
            notes="N/A"
        )

        print("Invalid station created:")
        invalid_space_station.show_info()

    except ValidationError as err:
        print("Expected validation error:")
        for error in err.errors():
            print(f"{error['msg']}")


if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        print(f"Unexpected error: {err}")
