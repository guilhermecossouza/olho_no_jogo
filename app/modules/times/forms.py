from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError, Optional
import json


class TimeForm(FlaskForm):
    nome = StringField(
        "Time",
        validators=[
            Optional(),
            Length(min=1, max=255, message="O nome deve ter entre 1 e 100 caracteres.")
        ]
    )
    
    codigo_sofascore = IntegerField(
        "Código SofaScore",
        validators=[
            Optional(),
            NumberRange(min=1, max=255, message="O código SofaScore deve estar entre 1 e 1000.")
        ]
    )
    
    times_json = TextAreaField(
        "Estatística da partida - Arquivo JSON Total",
        validators=[Optional()]
    )
    
    submit = SubmitField("Salvar")
    
    
    def validate_times_json(self, field):
        if not field.data or not field.data.strip():
            return
        
        try:
            dados =json.loads(field.data)
        except json.JSONDecodeError as e:
            raise ValidationError(f"JSON inválido: {e.msg} (linha {e.lineno})")
        
        if not isinstance(dados, (dict, list)):
            raise ValidationError("O JSON deve ser um objeto ou uma lista.")
        
    def validate(self, extra_validators=None, **kwargs):
        if not super().validate(extra_validators, **kwargs):
            return False
        
        nome_ok = bool(self.nome.data and self.nome.data.strip())
        codigo_ok = bool(self.codigo_sofascore.data)
        json_ok = bool(self.times_json.data and self.times_json.data.strip())
        
        if not nome_ok and not codigo_ok and not json_ok:
            self.nome.errors.append("Preencha o nome e o código do time, OU cole um JSON.")
            return False

        if nome_ok != codigo_ok:
            if not nome_ok:
                self.nome.errors.append("Preencha o nome do time.")
            if not codigo_ok:
                self.codigo_sofascore.errors.append("Preencha o código SofaScore.")
            return False

        if nome_ok and codigo_ok and json_ok:
            self.times_json.errors.append(
                "Você não pode preencher nome/código E o JSON ao mesmo tempo."
            )
            return False

        return True
    
    def erros_agrupados(self):
        todos = []
        for campo in self:
            if campo.errors:
                for erro in campo.errors:
                    todos.append(f"{campo.label.text}: {erro}")
        return todos
            
        
    