request_background_check = {
    'type': 'object',
    'properties': {
        'document': {
            'type': 'string',
            'pattern': '^[0-9]{8,10}$'
        },
        'antecedents': {
            'type': 'array',
            'items': {
                'enum': ['1', '2', '3', '4', '5', '6']
            },
            'minItems': 1, 
            'uniqueItems': True
        }
    },
    'required': [
        'document', 
        'antecedents'
    ]
}