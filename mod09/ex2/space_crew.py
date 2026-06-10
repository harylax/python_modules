from enum import Enum
from datetime import datetime


try:
    from pydantic import BaseModel, Field, ValidationError, model_validator
except ImportError:
    print("Pydantic not installed\n")
    print("Usage:")
    print("\tpython3 -m venv venv")
    print("\tsource venv/bin/activate")
    print("\tpip install pydantic")
    exit(1)


class Rank(str, Enum):
    cadet = "cadet"
    officer = "officer"
    lieutenant = "lieutenant"
    captain = "captain"
    commander = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(..., min_length=3, max_length=10)
    name: str = Field(..., min_length=2, max_length=50)
    rank: Rank = Field(...)
    age: int = Field(..., ge=18, le=80)
    specialization: str = Field(..., min_length=3, max_length=30)
    years_experience: int = Field(..., ge=0, le=50)
    is_active: bool = Field(default=True)


class SpaceMission(BaseModel):
    mission_id: str = Field(..., min_length=5, max_length=15)
    mission_name: str = Field(..., min_length=3, max_length=100)
    destination: str = Field(..., min_length=3, max_length=50)
    launch_date: datetime = Field(...)
    duration_days: int = Field(..., ge=1, le=3650)
    crew: list[CrewMember] = Field(..., min_length=1, max_length=12)
    mission_status: str = Field(default="planned")
    budget_millions: float = Field(..., ge=1.0, le=10000.0)

    @model_validator(mode='after')
    def mission_validation_rules(self) -> 'SpaceMission':
        if not self.mission_id.startswith('M'):
            raise ValueError("Mission ID must start with \"M\"")
        count: int = 0
        for member in self.crew:
            if member.rank == Rank.commander:
                count += 1
            if member.rank == Rank.captain:
                count += 1
        if count == 0:
            raise ValueError("Must have at least one Commander or Captain")
        count = 0
        if self.duration_days > 365:
            for member in self.crew:
                if member.years_experience >= 5:
                    count += 1
            ratio: float = count / len(self.crew)
            if ratio < 0.5:
                raise ValueError(
                    "Long missions (> 365 days) need "
                    "50% experienced crew (5+ years)"
                    )
        if not all(member.is_active for member in self.crew):
            raise ValueError("All crew members must be active")
        return self


try:
    print()
except ValidationError:
    pass
