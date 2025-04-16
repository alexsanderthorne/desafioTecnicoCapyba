from app import ma
from marshmallow import validates, ValidationError
from app.models.pessoa import Pessoa
import re
from datetime import datetime

class PessoaSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Pessoa
        load_instance = True

    id = ma.auto_field()
    nome = ma.auto_field(required=True)
    cpf = ma.auto_field(required=True)
    data_nascimento = ma.auto_field(required=True)
    email = ma.auto_field(required=True)
    naturalidade = ma.auto_field()
    nacionalidade = ma.auto_field()

    @validates('cpf')
    def validate_cpf(self, value):
        if not re.match(r'^\d{11}$', value):
            raise ValidationError("CPF deve conter 11 dígitos numéricos.")
        # Validação real de CPF (básica):
        if len(set(value)) == 1:
            raise ValidationError("CPF inválido.")

    @validates('data_nascimento')
    def validate_data(self, value):
        if isinstance(value, str):
            try:
                datetime.strptime(value, "%Y-%m-%d")
            except ValueError:
                raise ValidationError("Data deve estar no formato YYYY-MM-DD.")
