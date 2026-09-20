from typing import Any

from sqlalchemy import text
from sqlalchemy.orm import Session


class MySQLRepository:

    def __init__(self, session: Session):
        self.session = session

    def execute_query(
        self,
        sql: str,
        params: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:

        result = self.session.execute(
            text(sql),
            params or {}
        )

        return [
            dict(row)
            for row in result.mappings().all()
        ]