from datetime import datetime
import json
from pathlib import Path


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
    last_maintenance: datetime = Field(...)
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
    try:
        json_path = Path("generated_data/space_stations.json")
        with open(json_path) as f:
            data_dict: dict = json.load(f)
    except OSError as err:
        print("\n========================================")
        print(f"Could not load generated data: {err}")
        print("Usage: from the root")
        print("\tpython3 data_exporter.py")
        print("\tpython3 ex0/space_station.py")
        return
    print("\n========================================")
    print("Validation of generated data")
    for data in data_dict:
        try:
            s = SpaceStation(**data)
            print(f"\t[OK] ID:\t\t{s.station_id}")
            print(f"\t[OK] Name:\t\t{s.name}")
            print(f"\t[OK] Crew:\t\t{s.crew_size}")
            print(f"\t[OK] Power:\t\t{s.power_level}")
            print(f"\t[OK] Oxygen:\t\t{s.oxygen_level}")
            print(f"\t[OK] Maintenance:\t\t{s.last_maintenance}")
            print(f"\t[OK] Status:\t\t{s.is_operational}")
            print(f"\t[OK] Notes:\t\t{s.notes}")
            print()
        except ValidationError as err:
            for error in err.errors():
                print(f"{data} validation error: {error['msg']}")


if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        print(f"Unexpected error: {err}")
