from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Length, NumberRange, Optional


class TimeForm(FlaskForm):
    id_time = HiddenField()

    nome = StringField(
        "Time",
        validators=[
            DataRequired(message="O nome do time é obrigatório."),
            Length(min=1, max=100, message="O nome deve ter entre 1 e 100 caracteres."),
        ],
    )

    codigo_sofascore = IntegerField(
        "Código SofaScore",
        validators=[
            Optional(),
            NumberRange(min=1, message="O código SofaScore deve ser um número positivo."),
        ],
    )

    submit = SubmitField("Salvar")

    def __init__(self, time=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if time is not None:
            self.id_time.data = str(time.idTime)
            self.nome.data = time.name
            self.codigo_sofascore.data = time.idSofascore


class TimeJsonForm(FlaskForm):
    json = TextAreaField(
        "JSON - statistic",
        validators=[DataRequired(message="O JSON é obrigatório.")],
        render_kw={"rows": 20},
    )
    submit = SubmitField("Salvar")