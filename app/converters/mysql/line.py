from app.models.mysql.line import LineMySQL
from app.schemas.mysql.line import (
    LineCreate,
    LineRead,
    LineUpdate,
)


class LineConverter:

    @staticmethod
    def to_entity(line_mysql: LineMySQL) -> LineRead:
        return LineRead(
            line_id=line_mysql.line_id,
            line_code=line_mysql.line_code,
            line_name=line_mysql.line_name,
            city=line_mysql.city,
            status=line_mysql.status,
            created_at=line_mysql.created_at,
        )

    @staticmethod
    def to_mysql(line: LineCreate) -> LineMySQL:
        return LineMySQL(
            line_code=line.line_code,
            line_name=line.line_name,
            city=line.city,
            status=line.status,
        )