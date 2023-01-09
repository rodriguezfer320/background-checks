request_background_check = {
    'type': 'object',
    'properties': {
        'document': {
            'type': 'string',
            'pattern': '^[0-9]{10}$'
        },
        'antecedents': {
            'type': 'array',
            'items': {
                'enum': [
                    'disciplinary',
                    'fiscal', 
                    'judicial',
                    'corrective-actions',
                    'military-situation',
                    'traffic-infraction'
                ]
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