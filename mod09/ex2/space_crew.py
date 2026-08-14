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
        "\npip install pydantic\npip install mypy\npython3 space_crew.py"
        "\npython -m mypy space_crew.py"
        )
    exit(1)


class Rank(Enum):
    cadet = 'cadet'
    officer = 'officer'
    lieutenant = 'lieutenant'
    captain = 'captain'
    commander = 'commander'


class CrewMember(BaseModel):
    member_id: str = Field(..., min_length=3, max_length=10)
    name: str = Field(..., min_length=2, max_length=50)
    rank: Rank = Field(...)
    age: int = Field(..., ge=18, le=80)
    specialisation: str = Field(..., min_length=3, max_length=30)
    years_experience: int = Field(..., ge=0, le=50)
    is_active: bool = Field(default=True)


class SpaceMission(BaseModel):
    mission_id: str = Field(..., min_length=5, max_length=15)
    mission_name: str = Field(..., min_length=3, max_length=100)
    destination: str = Field(..., min_length=3, max_length=50)
    launch_date: datetime = Field(...)
    duration_days: int = Field(..., ge=1, le=3650)
    crew: list[CrewMember] = Field(..., min_length=1, max_length=12)
    mission_status: str = Field(default='planned')
    budget_millions: float = Field(..., ge=1.0, le=10000.0)

    @model_validator(mode='after')
    def mission_validation(self) -> 'SpaceMission':
        if not self.mission_id.startswith('M'):
            raise ValueError("Mission ID must start with \"M\"")
        if not any(
            member.rank.value in ['commander', 'captain']
            for member in self.crew
        ):
            raise ValueError(
                "Mission must have at least one Commander or Captain"
                )
        if self.duration_days > 365:
            count: int = 0
            for member in self.crew:
                if member.years_experience >= 5:
                    count += 1
            if count / len(self.crew) < 0.5:
                raise ValueError(
                    "Long missions (> 365 days) need 50% "
                    "experienced crew (5+ years)"
                    )
        if not all(member.is_active for member in self.crew):
            raise ValueError("All crew members must be active")
        return self

    def show_info(self) -> None:
        print(f"Mission: {self.mission_name}")
        print(f"ID: {self.mission_id}")
        print(f"Destination: {self.destination}")
        print(f"Duration: {self.duration_days} days")
        print(f"Budget: ${self.budget_millions}M")
        print(f"Crew size: {len(self.crew)}")
        print("Crew members:")
        for member in self.crew:
            print(
                f"- {member.name} ({member.rank.value})"
                f" - {member.specialisation}"
                )


def main() -> None:
    print("Alien Contact Log Validation")
    print("======================================")

    try:
        sarah_connor: CrewMember = CrewMember(
            member_id="SM001",
            name="Sarah Connor",
            rank=Rank('commander'),
            age=45,
            specialisation='Mission Command',
            years_experience=15
        )
        john_smith: CrewMember = CrewMember(
            member_id="SM019",
            name="John Smith",
            rank=Rank('lieutenant'),
            age=25,
            specialisation='Navigation',
            years_experience=5
        )
        alice_johnson: CrewMember = CrewMember(
            member_id="SM005",
            name="Alice Johnson",
            rank=Rank('officer'),
            age=33,
            specialisation='Engeneering',
            years_experience=6
        )
        valid_mission: SpaceMission = SpaceMission(
            mission_id='M2024_MARS',
            mission_name='Mars Colony Establishment',
            destination='Mars',
            launch_date=datetime.fromisoformat("2024-01-01T10:00:00"),
            duration_days=900,
            budget_millions=2500.0,
            crew=[sarah_connor, john_smith, alice_johnson],
        )

        print("Valid mission report:")
        valid_mission.show_info()

    except ValidationError as err:
        print("Expected validation error:")
        for error in err.errors():
            print(f"{error['msg'].replace('Value error, ', '')}")

    print("\n========================================")

    try:
        john_connor: CrewMember = CrewMember(
            member_id="SM010",
            name="John Connor",
            rank=Rank('cadet'),
            age=24,
            specialisation='Technician',
            years_experience=5
        )
        sarah_smith: CrewMember = CrewMember(
            member_id="SM008",
            name="Sarah Smith",
            rank=Rank('lieutenant'),
            age=25,
            specialisation='Navigation',
            years_experience=5
        )
        johnson_alice: CrewMember = CrewMember(
            member_id="SM007",
            name="Johnson_Alice",
            rank=Rank('officer'),
            age=33,
            specialisation='Engeneering',
            years_experience=6
        )
        invalid_mission: SpaceMission = SpaceMission(
            mission_id='M2024_MARS',
            mission_name='Mars attack',
            destination='Mars',
            launch_date=datetime.fromisoformat("2027-01-01T10:00:00"),
            duration_days=900,
            budget_millions=2500.0,
            crew=[john_connor, sarah_smith, johnson_alice],
        )

        print("Valid mission report:")
        invalid_mission.show_info()

    except ValidationError as err:
        print("Expected validation error:")
        for error in err.errors():
            print(f"{error['msg'].replace('Value error, ', '')}")


if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        print(f"Unexpected error: {err}")
