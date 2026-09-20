from app.models.mysql.alarm_record import AlarmRecordMySQL
from app.schemas.mysql.alarm_record import (
    AlarmRecordCreate,
    AlarmRecordRead,
    AlarmRecordUpdate,
)


class AlarmRecordConverter:

    @staticmethod
    def to_entity(
        alarm_mysql: AlarmRecordMySQL,
    ) -> AlarmRecordRead:

        return AlarmRecordRead(
            alarm_id=alarm_mysql.alarm_id,
            vehicle_id=alarm_mysql.vehicle_id,
            device_id=alarm_mysql.device_id,
            alarm_code=alarm_mysql.alarm_code,
            alarm_type=alarm_mysql.alarm_type,
            alarm_level=alarm_mysql.alarm_level,
            alarm_time=alarm_mysql.alarm_time,
            clear_time=alarm_mysql.clear_time,
            alarm_content=alarm_mysql.alarm_content,
            status=alarm_mysql.status,
            created_at=alarm_mysql.created_at,
        )

    @staticmethod
    def to_mysql(
        alarm: AlarmRecordCreate,
    ) -> AlarmRecordMySQL:

        return AlarmRecordMySQL(
            vehicle_id=alarm.vehicle_id,
            device_id=alarm.device_id,
            alarm_code=alarm.alarm_code,
            alarm_type=alarm.alarm_type,
            alarm_level=alarm.alarm_level,
            alarm_time=alarm.alarm_time,
            clear_time=alarm.clear_time,
            alarm_content=alarm.alarm_content,
            status=alarm.status,
        )
