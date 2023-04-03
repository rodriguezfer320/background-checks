from marshmallow import Schema, ValidationError, fields, validate, validates

class GetDataSchema(Schema):
    document = fields.String(
        required = True,
        validate = validate.Regexp(regex='^[0-9]{8,10}$', error='Ingrese un número entre 8 y 10 digitos.'),
        error_messages = {
            'required': 'Debe ingresar el número de identificación.'
        }
    )
    antecedents = fields.List(
        fields.String(
            validate = [
                validate.OneOf(
                    choices = ['1', '2', '3', '4', '5', '6', '7'],
                    error = 'Solo debe seleccionar antecedentes disponibles.'
                )
            ]
        ),
        required = True,
        validate = [
            validate.Length(
                min = 1,
                error = 'Debe seleccionar uno o varios antecedente(s).'
            )
        ],
        error_messages = {
            'required': 'Debe seleccionar al menos un antecedente.'
        }
    )

    @validates('antecedents')
    def no_duplicate_currencies(self, antecedents):
        if len(antecedents) != len(set(antecedents)):
            raise ValidationError('No debe seleccionar un mismo antecedentes dos veces.')