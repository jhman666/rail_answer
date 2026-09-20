from datetime import datetime

from pydantic import BaseModel, ConfigDict


class FaultRecordBase(BaseModel):
    vehicle_id: int | None = None
    device_id: int | None = None
    fault_code: str | None = None
    fault_type: str | None = None
    fault_level: str | None = None
    fault_time: datetime | None = None
    recover_time: datetime | None = None
    fault_description: str | None = None
    fault_cause: str | None = None
    status: str | None = None


class FaultRecordCreate(FaultRecordBase):
    pass


class FaultRecordUpdate(BaseModel):
    vehicle_id: int | None = None
    device_id: int | None = None
    fault_code: str | None = None
    fault_type: str | None = None
    fault_level: str | None = None
    fault_time: datetime | None = None
    recover_time: datetime | None = None
    fault_description: str | None = None
    fault_cause: str | None = None
    status: str | None = None


class FaultRecordRead(FaultRecordBase):
    fault_id: int
    created_at: datetime | None = None

    model_config = ConfigDict(
        from_attributes=True
    )