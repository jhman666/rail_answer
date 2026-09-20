from datetime import datetime

from pydantic import BaseModel, ConfigDict


class LineBase(BaseModel):
    line_code: str
    line_name: str
    city: str | None = None
    status: str | None = None


class LineCreate(LineBase):
    pass


class LineUpdate(BaseModel):
    line_code: str | None = None
    line_name: str | None = None
    city: str | None = None
    status: str | None = None


class LineRead(LineBase):
    line_id: int
    created_at: datetime | None = None

    model_config = ConfigDict(
        from_attributes=True
    )