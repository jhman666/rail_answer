from .base import Base

from .line import LineMySQL
from .vehicle import VehicleMySQL
from .device import DeviceMySQL
from .fault_record import FaultRecordMySQL
from .alarm_record import AlarmRecordMySQL
from .vehicle_daily_health import VehicleDailyHealthMySQL


__all__ = [
    "Base",
    "LineMySQL",
    "VehicleMySQL",
    "DeviceMySQL",
    "FaultRecordMySQL",
    "AlarmRecordMySQL",
    "VehicleDailyHealthMySQL",
]