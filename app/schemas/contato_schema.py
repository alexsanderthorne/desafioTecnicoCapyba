from app import ma
from marshmallow import validates, ValidationError
from app.models.contato import Contato

class ContatoSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Contato
        load_instance = True

    id = ma.auto_field()
    tipo = ma.auto_field(required=True)
    valor = ma.auto_field(required=True)
    pessoa_id = ma.auto_field(required=True)

    @validates('tipo')
    def validate_tipo(self, value):
        if value.lower() not in ['email', 'telefone']:
            raise ValidationError("Tipo deve ser 'email' ou 'telefone'.")
