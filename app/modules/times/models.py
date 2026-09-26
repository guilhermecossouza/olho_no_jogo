from typing import Optional

from app.extensions import db


class TimeModel(db.Model):
    __tablename__ = "TbTimes"

    idTime = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idSofascore = db.Column(db.Integer, nullable=True, unique=True, index=True)
    name = db.Column(db.String(100), nullable=False, unique=True, index=True)

    def __init__(self, name: str, idSofascore: Optional[int] = None, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.idSofascore = idSofascore

    def __repr__(self):
        return f"<Time {self.name} (SofaScore: {self.idSofascore})>"