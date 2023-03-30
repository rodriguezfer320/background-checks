from marshmallow import Schema, ValidationError, fields, validate, validates
from os import path

class PutDataSchema(Schema):
    title = fields.String(
        required = True,
        error_messages = {
            'required': 'Debe ingresar un título.'
        }
    )
    candidate_id = fields.String(
        required = True,
        validate = validate.Regexp(regex='^[0-9]{8,10}$', error='Ingrese un número entre 8 y 10 digitos.'),
        error_messages = {
            'required': 'Debe ingresar el número de identificación.'
        }
    )

class PostDataSchema(PutDataSchema):
    background_id = fields.Integer(
        required = True,
        error_messages = {
            'required': 'Debe seleccionar un antecedente.',
            'invalid': 'Debe ingresar un número entero.'
        }
    )

class PutStateSchema(Schema):
    comment = fields.String(
        required = True,
        error_messages = {
            'required': 'Debe ingresar un comentario.'
        }
    )
    state = fields.String(
        required = True,
        error_messages = {
            'required': 'Debe seleccionar un estado.'
        }
    )
        
class FileSchema(Schema):
    document = fields.Raw(
        required = True,
        error_messages = {
            'required': 'Debe seleccionar un documento.'
        }
    )

    @validates('document')
    def validate_document(self, document):
        filename, file_ext = path.splitext(document.filename)
        file_size = len(document.read()) / 1000000

        if file_ext != '.pdf':
            raise ValidationError(f'Debe seleccionar un archivo en formato pdf.')
        elif file_size > 10.0:
            raise ValidationError(f'Debe seleccionar un archivo que no supere los 10Mb.')