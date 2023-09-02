from werkzeug.datastructures import ImmutableMultiDict, FileStorage
from flask import request
from flask_smorest.fields import Upload
from marshmallow import Schema, ValidationError, fields, validate, validates, pre_load, post_load
from ...utils import State
import re, os

class VerificationRequestArgsSchema(Schema):
    page = fields.Integer(
        required = False, 
        missing = 1,
        error_messages = {
            'invalid': 'Debe ingresar un número entero.'
        }
    )
    search = fields.String(
        required = False, 
        missing = None
    )
    state = fields.String(
        required = False, 
        missing = State.ALL.value
    )

    @validates('page')
    def validate_page(self, page):
        if page <= 0:
            raise ValidationError('Debe ingresar una pagina mayor a cero.')

class VerificationRequestPutDataSchema(Schema):
    title = fields.String(
        required = True,
        error_messages = {
            'required': 'Debe ingresar un título.'
        }
    )
    document = fields.String(
        required = True,
        validate = validate.Regexp(regex='^[0-9]{8,10}$', error='Ingrese un número entre 8 y 10 digitos.'),
        error_messages = {
            'required': 'Debe ingresar el número de identificación.'
        }
    )

class VerificationRequestPutStateSchema(Schema):
    comment = fields.String(
        required = True,
        error_messages = {
            'required': 'Debe ingresar un comentario.'
        }
    )
    state = fields.String(
        required = True,
        validate=validate.OneOf(
            ['aprobada', 'rechazada'], 
            error="No modifique las propidades de las opciones, solo se admiten dos tipos ['aprobada', 'rechazada']"
        ),
        error_messages = {
            'required': 'Debe seleccionar un estado.'
        }
    )

class VerificationRequestFileSchema(Schema):
    file_document = Upload(
        error_messages = {
            'null': 'Debe seleccionar un documento.'
        }
    )

    @pre_load
    def load_file_document(self, data, many, **kwargs):
        file = request.files.get('file_document')
        dataTemp = data.to_dict()
        dataTemp['file_document'] = None

        if file:
            old_file_position = file.tell()
            file.seek(0, os.SEEK_END)
            dataTemp['file_document'] = FileStorage(
                stream=file.stream,
                filename=file.filename,
                content_type=file.mimetype,
                content_length=file.tell()
            )            
            file.seek(old_file_position, os.SEEK_SET)

        return ImmutableMultiDict((key, dataTemp[key]) for key in dataTemp.keys())
    
    @validates('file_document')
    def validate_file_document(self, file_document):
        if file_document.mimetype != 'application/pdf':
            raise ValidationError('Debe seleccionar un archivo en formato pdf.')
        elif (file_document.content_length / 1000000) > 10.0:
            raise ValidationError('Debe seleccionar un archivo que no supere los 10Mb.')

class VerificationRequestPostSchema(VerificationRequestPutDataSchema, VerificationRequestFileSchema):
    antecedent = fields.Integer(
        required = True,
        error_messages = {
            'required': 'Debe seleccionar un antecedente.',
            'invalid': 'No modifique las propiedades de las opciones, deben ser numeros enteros.'
        }
    )