from fastapi.exceptions import RequestValidationError
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse


def camel_case_split(text):
    try:
        words = [[text[0]]]

        for c in text[1:]:
            if words[-1][-1].islower() and c.isupper():
                words.append(list(c))
            else:
                words[-1].append(c)

        return " ".join(["".join(word).capitalize() for word in words])
    except TypeError:
        return text


def base_validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for count, error in enumerate(exc.errors()):
        loc, message, types = error["loc"], error["msg"], error['type']
        try:
            field = error["loc"][1]
        except IndexError:
            field = None
        errors.append({
            "code": "validation-error",
            "type": types,
            "message": message,
            "field": None if types == 'value_error.jsondecode' else field
        })
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=errors
    )

