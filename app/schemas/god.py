from pydantic import BaseModel, ConfigDict


class GodBase(BaseModel):
    name: str
    domain: str
    icon: str
    coaching_style: str
    focus_messages: list[str]
    break_messages: list[str]
    session_start_messages: list[str]


class God(GodBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
