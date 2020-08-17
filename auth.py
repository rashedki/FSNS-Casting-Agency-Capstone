# Note: This file is pretty much a copy/paste from my Coffeeshop project
import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen

# Defining Autho0 information
AUTH0_DOMAIN = 'rashedki.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'casting'

## AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


## Auth Header

'''
Defining function to obtain authorization token from request header
'''
def get_token_auth_header():
    '''Obtains access token from the Authoization header'''
     # Getting auth info from header
    auth_header = request.headers['Authorization']

    # Checking to see if auth information is present, else raises 401 error
    if "Authorization" not in request.headers:
        raise AuthError({
            'code': 'invalid_authorization',
            'description': 'Authorization not included in Header.'
        }, 401)
    
    # Splitting out parts of auth header
    header_parts = auth_header.split()
    
    # Checking if 'parts' info looks as we would expect it to
    if len(header_parts)!=2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Invalid Header.'
        }, 401)
    elif header_parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_bearer token',
            'description': 'Bearer missing in header.'
        }, 401)
    bearer  = header_parts[0]
    
    # Grabbing token from auth parts
    token = header_parts[1]
    return token

# Defining function to check if user has proper permissions given auth credentials
def check_permissions(permission, payload):
    
     # Checking to see if permissions are included in JWT
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permissions not included in JWT.'
        }, 400)
    
    # Checking to see if permission from JWT matches what's available in general
    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission not found.'
        }, 401)
    
     # If all checks out from above, return true
    return True
    #(note note note check the following line)
    # raise Exception('Not Implemented')

# Defining a function to check that the provided token matches what is expected from Auth0
def verify_decode_jwt(token):
     # Getting the public key from Auth0
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    
    # Getting header information from the provided token
    unverified_header = jwt.get_unverified_header(token)
    
    # Instantiating empty object to append RSA key info to
    rsa_key = {}
    
    # Checking to see if 'kid' is in the unverified header
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Missing kid.'
        }, 401)

    # Appending information to RSA key dictionary from jwks if 'kid' matches the unverified header
    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
   
    # Getting payload information from the token using key if everything checks out fine (else raises error)
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )
            return payload

        # Handling respective error scenarios
        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)
        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    # If RSA_key info not present, raising AuthError
    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 400)

# Defining a function to create a nice Python decorator to easily ensure if auhtoirzation info is present
# before allowing user to perform any activities.
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):           
            try:
                token = get_token_auth_header()
                payload = verify_decode_jwt(token)
                check_permissions(permission, payload)
            except:
                raise AuthError({
                    'code': 'invalid_token',
                    'description': 'Token could not be verified.'
                }, 401)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator