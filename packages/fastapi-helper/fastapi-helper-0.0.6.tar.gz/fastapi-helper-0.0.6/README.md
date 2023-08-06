# FastAPI Helper

## Simple and customizable HTTP exceptions
```python
import uvicorn
from fastapi import FastAPI
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse
from src.fastapi_fancy_exceptions import FancyHTTPException


app = FastAPI()


class AuthException(FancyHTTPException):
    code = "auth_error"
    type = "AuthError"
    message = "Auth error"
    status_code = status.HTTP_401_UNAUTHORIZED


@app.exception_handler(FancyHTTPException)
async def http_exception_accept_handler(request: Request, exc: FancyHTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=[{"code": exc.code, "type": exc.type, "message": exc.message}]
    )


@app.get("/")
async def root():
    raise AuthException()

uvicorn.run(app, host="localhost", port=8000)
```

#### This code will lead to this response with status code 401:

```json
[
  {
    "code": "auth_error",
    "type": "AuthError",
    "message": "Auth error"
  }
]
```
