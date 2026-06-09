from datetime import datetime


try:
    from pydantic import BaseModel, Field, ValidationError
except ImportError:
    print("Pydantic not installed\n")
    print("Usage:")
    print("\tpython3 -m venv venv")
    print("\tsource venv/bin/activate")
    print("\tpip install pydantic")
    exit(1)


class SpaceStation(BaseModel):
    station_id: str = Field(..., min_length=3, max_length=10)
    name: str = Field(..., min_length=1, max_length=50)
    crew_size: int = Field(..., ge=1, le=20)
    power_level: float = Field(..., ge=0.0, le=100.0)
    oxygen_level: float = Field(..., ge=0.0, le=100.0)
    last_maintenance: datetime  # pydantic knows str with date format
    is_operational: bool = Field(default=True)
    notes: str | None = Field(default=None, max_length=200)


def main() -> None:
    print("Space Station Data Validation")
    print("========================================")
    station: SpaceStation = SpaceStation(
        station_id="ISS001",
        name="International Space Station",
        crew_size=6,
        power_level=85.5,
        oxygen_level=92.3,
        last_maintenance=datetime.fromisoformat("2026-06-09T20:47:02"),
        is_operational=True,
        notes="N/A"
    )
    print("Valid station created:")
    print(f"ID: {station.station_id}")
    print(f"Name: {station.name}")
    print(f"Crew: {station.crew_size} people")
    print(f"Power: {station.power_level}")
    print(f"Oxygen: {station.oxygen_level}")
    print("Status: ", end="")
    print(f"{'Operational' if station.is_operational else 'Out of service'}")
    print("\n========================================")
    try:
        SpaceStation(
            station_id="ISS001",
            name="International Space Station",
            crew_size=21,
            power_level=85.5,
            oxygen_level=92.3,
            last_maintenance=datetime.fromisoformat("2026-06-09T20:47:02"),
            is_operational=True,
            notes="N/A"
            )
    except ValidationError as err:
        print("Expected validation error:")
        for error in err.errors():
            print(error['msg'])


if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        print(f"Unexpected error: {err}")
