from flask import request
from flask_smorest import abort
from decouple import config
import jwt

def _verify_authentication_header():
    authToken = request.headers.get('Authorization', None)
    message = 'Se espera la cabecera: Authorization'
    token = None

    if authToken:
        parts = authToken.split()

        if parts[0] != 'Bearer':
            message = 'La cabecera de autenticación debe comenzar con Bearer'
        elif len(parts) == 1:
            message = 'Token no encontrado'
        elif len(parts) > 2:
            message = 'La cabecera debe ser: Bearer token'
        else:
            return parts[1]

        abort(401, message=message)

def _verify_token(token):
    try:
        return jwt.decode(
            token, 
            config('AUTH_PUBLIC_KEY').replace('\\n', '\n'), 
            algorithms=['RS256']
        )
    except:
        abort(401, message='El token no es válido o ha caducado')

def authentication_required_and_permissions(allowedRoles):
    environment = config('ENVIRONMENT')
    tokenEnabled = config('TOKEN_ENABLED')
    validateToken = tokenEnabled == 'True' if environment == 'testing' else True

    def real_decorator(function):
        def decorated_function(*args, **kws):
            if validateToken:
                # se valida la cabecera de autenticación
                token = _verify_authentication_header()
                
                # se valida el token
                data = _verify_token(token)
                
                # se verifica el rol del usuario
                if data['role'] not in allowedRoles:
                    abort(403, message='No tiene permitido el acceso a esta url')
            
            return function(*args, **kws)
        return decorated_function
    return real_decorator