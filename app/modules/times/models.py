from app.extensions import db


class TimeModel(db.Model):
    __tablename__ = "TbTimes"

    idTime = db.Column(db.Integer, primary_key=True)
    idSofascore = db.Column(db.Integer, nullable=True) 
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Time {self.name} (SofaScore: {self.idSofascore})>"