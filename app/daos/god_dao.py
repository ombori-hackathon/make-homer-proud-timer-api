from sqlalchemy.orm import Session

from app.daos.base import BaseDAO
from app.models.god import God


class GodDAO(BaseDAO[God]):
    def __init__(self, db: Session):
        super().__init__(db, God)

    def get_by_name(self, name: str) -> God | None:
        return self.db.query(God).filter(God.name == name).first()
