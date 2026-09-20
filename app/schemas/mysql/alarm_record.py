from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AlarmRecordBase(BaseModel):
    vehicle_id: int | None = None
    device_id: int | None = None
    alarm_code: str | None = None
    alarm_type: str | None = None
    alarm_level: str | None = None
    alarm_time: datetime | None = None
    clear_time: datetime | None = None
    alarm_content: str | None = None
    status: str | None = None


class AlarmRecordCreate(AlarmRecordBase):
    pass


class AlarmRecordUpdate(BaseModel):
    vehicle_id: int | None = None
    device_id: int | None = None
    alarm_code: str | None = None
    alarm_type: str | None = None
    alarm_level: str | None = None
    alarm_time: datetime | None = None
    clear_time: datetime | None = None
    alarm_content: str | None = None
    status: str | None = None


class AlarmRecordRead(AlarmRecordBase):
    alarm_id: int
    created_at: datetime | None = None

    model_config = ConfigDict(
        from_attributes=True
    )