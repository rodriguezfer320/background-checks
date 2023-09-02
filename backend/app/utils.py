from enum import Enum
 
class State(Enum):
    ALL = 'todos'
    PENDING = 'pendiente'
    DENIED = 'rechazada'
    CORRECTED = 'corregida'
    APPROVED = 'aprobada'

class Role(Enum):
    COMPANY = 'company'
    CANDIDATE = 'student'
    OFFICER = 'program_direction'

class BackgroundNoWeb(Enum):
    UD = 'university degree'

class BackgroundWeb(Enum):
    DB = 'disciplinary'
    FB = 'fiscal'
    JB = 'judicial'
    CAB = 'corrective actions'
    MSB = 'military situation'
    TIB = 'traffic infraction'

TYPEWEB = 'web'