from app.models.mysql.vehicle_daily_health import (
    VehicleDailyHealthMySQL,
)
from app.schemas.mysql.vehicle_daily_health import (
    VehicleDailyHealthCreate,
    VehicleDailyHealthRead,
    VehicleDailyHealthUpdate,
)


class VehicleDailyHealthConverter:

    @staticmethod
    def to_entity(
        health_mysql: VehicleDailyHealthMySQL,
    ) -> VehicleDailyHealthRead:

        return VehicleDailyHealthRead(
            health_id=health_mysql.health_id,
            vehicle_id=health_mysql.vehicle_id,
            stat_date=health_mysql.stat_date,
            health_score=health_mysql.health_score,
            health_level=health_mysql.health_level,
            device_score=health_mysql.device_score,
            fault_score=health_mysql.fault_score,
            alarm_score=health_mysql.alarm_score,
            fault_count=health_mysql.fault_count,
            alarm_count=health_mysql.alarm_count,
            critical_fault_count=health_mysql.critical_fault_count,
            critical_alarm_count=health_mysql.critical_alarm_count,
            calculated_at=health_mysql.calculated_at,
        )

    @staticmethod
    def to_mysql(
        health: VehicleDailyHealthCreate,
    ) -> VehicleDailyHealthMySQL:

        return VehicleDailyHealthMySQL(
            vehicle_id=health.vehicle_id,
            stat_date=health.stat_date,
            health_score=health.health_score,
            health_level=health.health_level,
            device_score=health.device_score,
            fault_score=health.fault_score,
            alarm_score=health.alarm_score,
            fault_count=health.fault_count,
            alarm_count=health.alarm_count,
            critical_fault_count=health.critical_fault_count,
            critical_alarm_count=health.critical_alarm_count,
        )

