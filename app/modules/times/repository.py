from typing import Optional, Type

from app.extensions import db
from .models import TimeModel


class TimeRepository:
    model: Type[TimeModel] = TimeModel

    def __init__(self):
        self.model = TimeModel

    # ---------- CREATE ----------

    def criar(self, nome: str, id_sofascore: Optional[int] = None) -> TimeModel:
        time = self.model(name=nome.strip(), idSofascore=id_sofascore)
        db.session.add(time)
        db.session.commit()
        return time

    # ---------- READ ----------

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

    def existe_com_nome(self, nome: str, ignorar_id: Optional[int] = None) -> bool:
        query = db.session.query(self.model).filter(self.model.name == nome.strip())
        if ignorar_id is not None:
            query = query.filter(self.model.idTime != ignorar_id)
        return query.count() > 0

    def existe_com_sofascore(self, id_sofascore: int, ignorar_id: Optional[int] = None) -> bool:
        query = db.session.query(self.model).filter(self.model.idSofascore == id_sofascore)
        if ignorar_id is not None:
            query = query.filter(self.model.idTime != ignorar_id)
        return query.count() > 0

    # ---------- UPDATE ----------

    def atualizar(self, time: TimeModel, campos: dict) -> TimeModel:
        for campo, valor in campos.items():
            if hasattr(time, campo):
                setattr(time, campo, valor)
        db.session.commit()
        return time

    # ---------- DELETE ----------

    def deletar(self, time: TimeModel) -> None:
        db.session.delete(time)
        db.session.commit()