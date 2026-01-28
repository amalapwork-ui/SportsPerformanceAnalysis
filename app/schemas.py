from pydantic import BaseModel


class PlayerInput(BaseModel):
    age: int
    potential: int
    stamina: int
    strength: int
    sprint_speed: int
    work_rate_encoded: int


class InjuryInput(BaseModel):
    age: int
    stamina: int
    work_rate: int
