from .line import (
    LineCreate,
    LineUpdate,
    LineRead,
)

from .vehicle import (
    VehicleCreate,
    VehicleUpdate,
    VehicleRead,
)

from .device import (
    DeviceCreate,
    DeviceUpdate,
    DeviceRead,
)

from .fault_record import (
    FaultRecordCreate,
    FaultRecordUpdate,
    FaultRecordRead,
)

from .alarm_record import (
    AlarmRecordCreate,
    AlarmRecordUpdate,
    AlarmRecordRead,
)

from .vehicle_daily_health import (
    VehicleDailyHealthCreate,
    VehicleDailyHealthUpdate,
    VehicleDailyHealthRead,
)


__all__ = [
    "LineCreate",
    "LineUpdate",
    "LineRead",

    "VehicleCreate",
    "VehicleUpdate",
    "VehicleRead",

    "DeviceCreate",
    "DeviceUpdate",
    "DeviceRead",

    "FaultRecordCreate",
    "FaultRecordUpdate",
    "FaultRecordRead",

    "AlarmRecordCreate",
    "AlarmRecordUpdate",
    "AlarmRecordRead",

    "VehicleDailyHealthCreate",
    "VehicleDailyHealthUpdate",
    "VehicleDailyHealthRead",
]