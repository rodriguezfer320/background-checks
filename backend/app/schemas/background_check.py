from marshmallow import Schema, ValidationError, fields, validate, validates
from ..entities import BackgroundModel

class BackgroundCheckQueryArgsSchema(Schema):
    document = fields.String(
        required = True,
        validate = validate.Regexp(
            regex = '^[0-9]{8,10}$', error='Ingrese un número de identificación entre 8 y 10 digitos.'),
        error_messages = {
            'required': 'Debe ingresar el número de identificación.'
        }
    )
    antecedents = fields.List(
        fields.String(),
        required = True,
        error_messages = {
            'required': 'Debe seleccionar al menos un antecedente.'
        }
    )

    @validates('antecedents')
    def antecedents_validate(self, antecedents):
        if len(antecedents) == 1 and not antecedents[0].isdigit():
            raise ValidationError('Debe seleccionar al menos un antecedente.')
        elif any(not elem.isdigit() for elem in antecedents):
            raise ValidationError('No modifique las propiedades de las opciones, deben ser numeros enteros.')
        elif len(antecedents) != len(set(antecedents)):
            raise ValidationError('No modifique las propiedades de las opciones, no deden haber opciones repetidas.')
        else:
            result = BackgroundModel.query.with_entities(BackgroundModel.id).all()
            ants_bd = [elem.id for elem in result]

            if any(int(elem) not in ants_bd for elem in antecedents):
                raise ValidationError(f'No modifique las propiedades de las opciones, el rango de opciones es [{str(ants_bd[0])},{str(ants_bd[-1])}].')