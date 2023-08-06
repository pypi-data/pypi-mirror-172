=====
Django-JWT
=====

This is a package to verify and validate JSON Web Tokens (JWT) in Django. For 3d4Medical django projects.

### Installation
1. Install the package using pip.

2. Add "django_jwt" to your INSTALLED_APPS setting like this::
```
    INSTALLED_APPS = [
        ...
        'django_jwt',
    ]
```

### Configuration:
Required variables:
- JWT_CERTS_URL - certificate endpoint, like `https://keyCloak/realms/h/protocol/openid-connect/certs`

Optional variables:
- JWT_ALGORITHM - by default `ES256`
- JWT_AUDIENCE - by default ["account", "broker"]
- JWT_USER_UID - User model' unique identifier, by default `kc_id`

- JWT_USER_MAPPING - mapping between JWT claims and user model fields, by default:
```
    JWT_USER_MAPPING = {
        'first_name': 'first_name',
        'last_name': 'last_name',
        'username': 'username',
    }
```
- JWT_USER_DEFAULTS - default values for user model fields, by default:
```
    JWT_USER_DEFAULTS = {
        'is_active': True,
    }
```

- JWT_USER_ON_CREATE and JWT_USER_ON_UPDATE - functions to be called on user creation and update, by default:
```
    JWT_USER_ON_CREATE = None
    JWT_USER_ON_UPDATE = None
```

### Testing:
Run command `python runtests.py` to run tests.