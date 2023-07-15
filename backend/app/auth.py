from flask import request, jsonify
from decouple import config
import jwt

def _verify_authentication_header():
    authToken = request.headers.get('Authorization', None)
    message = 'Se espera la cabecera: Authorization'
    token = None

    if authToken:
        parts = authToken.split()

        if parts[0] != 'Bearer':
            message = 'La cabecera de autenticación debe comenzar con Bearer.'
        elif len(parts) == 1:
            message = 'Token no encontrado.'
        elif len(parts) > 2:
            message = 'La cabecera debe ser: Bearer token.'
        else:
            token = parts[1]

    return (token, {
        'code': 401,
        'status': 'UNAUTHORIZED',
        'message': message
    })

def _verify_token(token):
    try:
        data = jwt.decode(
            token, 
            config('AUTH_PUBLIC_KEY').replace('\\n', '\n'), 
            algorithms=['RS256']
        )
        return (data, None)
    except:
        return (None, {
            'code': 401,
            'status': 'TOKEN NOT VALID',
            'message': 'El token no es válido o ha caducado.'
        })


def authentication_required_and_permissions(allowedRoles):
    environment = config('ENVIRONMENT')
    tokenEnabled = config('TOKEN_ENABLED')
    validateToken = tokenEnabled == 'True' if environment == 'testing' else True

    def real_decorator(function):
        def decorated_function(*args, **kws):
            if validateToken:
                # se valida el cabecera de autenticación
                token, error = _verify_authentication_header()

                if token: # se valida el token
                    data, error = _verify_token(token)
                    
                    if data: # se verifica el rol del usuario
                        if data['role'] in allowedRoles:
                            return function(*args, **kws)
                        
                        error = {
                            'code': 403,
                            'status': 'PERMISSION DENIED',
                            'message': 'No tiene permitido el acceso a esta url.'
                        }
                
                return jsonify(error), error['code']
            else:
                return function(*args, **kws)
        return decorated_function
    return real_decorator