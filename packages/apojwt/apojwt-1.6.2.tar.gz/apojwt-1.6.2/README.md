# ApoJWT
The `apojwt` Package was created with the intention of providing JWT support to Intent's Apogee Microservices. These services require a hierarchy of permissions that vary across all endpoints. As such, this package aims to provide decorators that can be attached with route declarations to ensure a valid JWT with proper permissions is being sent in the request headers. The package is intended to be used alongside a Python API framework such as Flask or FastAPI.

---


## ApoJWT Class
The ApoJWT class has the following constructor:
```python
(
    self,
    secret: str,
    exp_period: int=900,
    iss: str="",
    server_audience: list=[],
    algorithm: str="HS256",
    template=None,
    async_framework: bool=False,
    token_finder=None,
    exception_handler=None)
"""
Keyword Arguments (those with asterisks are functions):

JWT Validation
    secret: 
        Secret string used to encode and decode the access JWT
    
    exp_period: 
        Length of time in seconds access tokens is valid for. 
        Default 900 (15 minutes) 
    
    iss: 
        Issuer string used for additional security.
        Default ""
    
    server_audience:
        Audience names of expected HTTP hosts. 
        Audience names are typically base address URLs.
        Ex: https://example.com
    
    algorithm: 
        The algorithm to use when encoding/decoding.
        Default HS256
    
    admin_permission: 
        Optional full admin permission
        JWTs carrying this will always be authorized
    

Framework Configuration
    Option 1: Flask/FastAPI Templates
        template: auto-configures ApoJWT to a known framework
                  Expected: "flask" | "fastapi"

    Option 2: Manual Configuration
    IF no template is used:
        async_framework:
            If True - ApoJWT awaits the decorated function
            (FastAPI needs this True)
            Default: False

        token_finder: 
            Returns the Access JWT (framework specific)
            Typically found as the "Authorization" header
            Default: None

            Expected Function Structure: 
                (*args, **kwargs) -> str


        exception_handler: 
            HTTP error handling function (framework specific)
            Expected Function Structure: 
            (code: int, msg: str) -> None
"""
```
<br>
<br>

## Higher Order Functionality in ApoJWT
---

### **Token Finder**
The token_finder function must be passed to the higher order constructor (if a template is not given) for decorated token validation to succeed. The function must return the JWT string, which can usually be found in the HTTP request headers with the key 'Authorization'. It is standard for JWTs to be prefixed with the word 'Bearer'. It will be up to this function to remove this substring.

Expected Function Structure: `(*args, **kwargs) -> str`

NOTE: `args` and `kwargs` are the same arguments given to the HTTP request handler and could be optional

***Example***
```python
# Flask's request object
request.headers["Authorization"]
>>> 'Bearer <token>'
request.headers["Authorization"].replace("Bearer ", "")
>>> '<token>'
```
```python
"""Token Finder: used to locate and return the JWT"""
# FastAPI
token_finder = lambda **kwargs: kwargs["Authorization"].replace("Bearer ", "")
ajwt = ("secret", iss="issuer", async_framework=True, token_finder=token_finder)
## NOTE: async_framework is True for FastAPI

# Flask
token_finder = lambda: request.headers["Authorization"].replace("Bearer ", "")
ajwt = ("secret", iss="issuer", token_finder=token_finder)
## NOTE: async_framework defaults to False for Flask
```
<br />

### **Exception Handler**
The exception handler is optional, but allows for decorated validation to properly be handled with an HTTP error response provided by the HTTP framework in use.

Expected Function Structure: `(code: int, exception_type: str, msg: str, *args, **kwargs) -> None`

***Example***
```python
"""Exception Handler"""
# FastAPI
def exception_handler(code: int, msg: str):
    raise HTTPException(status_code=code, detail=msg)
ajwt = ("secret", iss="issuer", async_framework=True, token_finder=..., exception_handler=exception_handler)

# Flask
def exception_handler(code: int, msg: str):
    abort(code, msg)

ajwt = ("secret", iss="issuer", token_finder=..., exception_handler=exception_handler)
```

<br />

## Decorators
---
Decorators are the main use case of the ApoJWT package after initialization. They allow any endpoint to be secured with a single simple line of code. 
```python
ajwt = ApoJWT(secret, iss, token_finder=lambda: ..., ...)


@ajwt.token_required
"""Validates JWT

Can return 'token_data' and 'token_subject' as kwargs to HTTP handler
"""


@ajwt.permission_required(permission_name: str)
"""Validates JWT and ensures permission_name is among the token permissions

permission_name: a permission string

Can return 'token_data' and 'token_subject' as kwargs to HTTP handler
"""
```
Both decorators return `token_data` and `token_subject` as keyword arguments to the HTTP handler that is being decorated. With these arguments, the additional data stored in the JWT and the JWT's subject are both accessible. 
<br />

***Example***
```python
# fast api
@app.get("/some/endpoint")
@ajwt.token_required
def some_endpoint(
    authorization=Header(None), # required
    token_data: Optional[dict] = Body(None), # optional
    token_subject: Optional[str] = Body(None) # optional
):
...

# flask
@app.route("/some/endpoint", methods=["GET"])
@ajwt.permission_required("permission")
def some_endpoint(
    token_data: dict, # optional
    token_subject: str # optional
):
...
```
<br />

## Functions
---
```python
ajwt = ApoJWT(...)

ajwt.create_token(
    self,
    sub: str="",
    permissions: list[str]=[],
    data: dict=dict(),
    refresh_data: dict=dict()
):
        """Encodes access and refresh* JWT(s)
            *if configured

        sub: 
            Subject of the JWT
            (typically a reference to the user of JWT)

        permissions:
            List of permissions to assign to token

        data:
            Any additional data that is needed

        refresh_data:
            IF refresh is configured:
            Additional data stored with the refresh token

        JWT will contain the following claims:
            - exp: Expiration Time
            - nbf: Not Before Time
            - iss: Issuer
            - aud: Audience
            - iat: Issued At
        """
```
<br>
<br>

## Refresh Tokens
---
ApoJWT 1.5.0 introduced Refresh Token functionality. This feature is highly recommended to provide an extra layer of security to applications. To read up on Refresh Tokens and their benefits, check out [this Auth0 article](https://auth0.com/blog/refresh-tokens-what-are-they-and-when-to-use-them/) for more information. The Refresh functionality in ApoJWT is activated with the following function:

```python
ajwt.config_refresh(refresh_secret: str, refresh_exp_period: int=86400, refresh_finder=None):
        """Configures ApoJWT for use with refresh tokens

        refresh_secret:
            Secret used to encode and decode the refresh JWT

        refresh_exp_period: 
            Number of seconds refresh JWT is valid
            Default 86400 (1 day)

        refresh_finder: 
            Function to retrieve the refresh JWT
            Default None
        """
```
The function `refresh_finder` is a similar function to `token_finder` in that it must return the refresh token. The main difference is that `refresh_finder`, in most cases, should find the refresh token in an http-only secure cookie instead of the HTTP Authorization header. 

Expected `refresh_finder` Function Structure: `(*args, **kwargs) -> str`

Once this function is called and initialized, ApoJWT is equipped to handle Refresh Tokens.
<br>

***Refresh Functionality***

The `create_token` function will now return a tuple containing the access token and the refresh token 
```python
access, refresh = ajwt.create_token(...)
```

Typically, this refresh token can then be stored in an HTTP-only cookie.

From there, the `@ajwt.refresh` decorator can be placed on any endpoint where a refresh should occur. This will return the refresh_data stored in the token. This can be another reference to the user which could be used to reauthorize.

***Example***
```python
# Here, the refresh data stores a user_id

# Fast Api
@app.get("/some/endpoint")
@ajwt.refresh
def refresh(refresh_data: dict):
    user_id = refresh_data["user_id"]
    user_permissions = get_user_permissions(user_id)
    
    ref_data = dict(user_id=user_id)
    access_token, refresh_token = ajwt.create_token(
        sub=user_id,
        permissions=user_permissions,
        refresh_data=ref_data
    )
```
<br>
<br>

## Usage Examples
---
### Constructing ApoJWT
```python
# FastAPI
ajwt = (
    "secret", 
    iss="issuer", 
    template="fastapi" # configures ApoJWT for fastapi
)
```
```python
# Flask
ajwt = (
    "secret", 
    iss="issuer", 
    template="fastapi" # configures ApoJWT for flask
)

```

### Validating JWT with Decorators
```python
# fast api
@app.get("/some/endpoint")
@ajwt.permission_required("permission")
def some_endpoint(authorization=Header(None)):
...

# flask
@app.route("/some/endpoint", methods=["GET"])
@ajwt.token_required
def some_endpoint()
...
```

### Refresh Configuration
```python
# flask
ajwt.config_refresh(
    "refresh_secret",
    refresh_finder=lambda: request.cookies.get('refresh_token')
)

# fast api
def refresh_finder(
    refresh_token: Union[str, None] = Cookie(default=None)
):
    return refresh_token

ajwt.config_refresh(
    "refresh_secret",
    refresh_finder=refresh_finder
)


```

### Creating a New JWT
```python
"""Permissions will be assigned to the new token"""

sub = "user_id_1"
permissions = ["permission", ...]
data = dict(...=...)


# If refresh IS NOT configured
# NOTE: all arguments are optional
token = ajwt.create_token(
    sub=sub,
    permissions=permissions,
    data=data
)

# If refresh IS configured
refresh_data = dict(...=...)
access, refresh = ajwt.create_token(
    sub=sub, 
    permissions=permissions, 
    data=data, 
    refresh_data=refresh_data
)
```

### Getting Token Data and Subject from JWT
```python
# flask
@app.route("/...")
@ajwt.token_required
def route(token_data: dict, token_subject: str):
    print(token_subject)
    return token_data


# fastapi
@app.get("/...")
@ajwt.permission_required("...")
def route(
    authorization=Header(None),
    # token_data and token_subject are unexpected to fastapi
    # Optional forces fastapi to ignore unexpected parameters
    token_data: Optional[dict]=Body(None),
    token_subject: Optional[str]=Body(None)
)
```