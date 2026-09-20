from typing import Optional

from app.extensions import db
from .models import TimeModel


class TimeRepository:
    def __init__(self):
        self.model = TimeModel

    def criar(self, nome: str, id_sofascore: Optional[int] = None) -> TimeModel:
        time = self.model(name=nome.strip(), idSofascore=id_sofascore)
        db.session.add(time)
        return time

    def buscar_por_id(self, id_time: int) -> Optional[TimeModel]:
        return db.session.get(self.model, id_time)

    def buscar_por_nome(self, nome: str) -> Optional[TimeModel]:
        return (
            db.session.query(self.model)
            .filter(self.model.name == nome.strip())
            .first()
        )

    def buscar_por_sofascore(self, id_sofascore: int) -> Optional[TimeModel]:
        return (
            db.session.query(self.model)
            .filter(self.model.idSofascore == id_sofascore)
            .first()
        )

    def listar_todos(self, ordem: str = "asc") -> list[TimeModel]:
        query = db.session.query(self.model)
        if ordem == "desc":
            query = query.order_by(self.model.name.desc())
        else:
            query = query.order_by(self.model.name.asc())
        return query.all()

    def existe_com_nome(self, nome: str) -> bool:
        return (
            db.session.query(self.model)
            .filter(self.model.name == nome.strip())
            .count() > 0
        )

    def existe_com_sofascore(self, id_sofascore: int) -> bool:
        return (
            db.session.query(self.model)
            .filter(self.model.idSofascore == id_sofascore)
            .count() > 0
        )

    def atualizar(self, time: TimeModel, **campos) -> TimeModel:
        for campo, valor in campos.items():
            if hasattr(time, campo):
                setattr(time, campo, valor)
        return time

    def deletar(self, time: TimeModel) -> None:
        db.session.delete(time)

    def contar(self) -> int:
        return db.session.query(self.model).count()