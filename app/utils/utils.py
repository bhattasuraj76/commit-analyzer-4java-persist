from enum import Enum
import functools
import logging
from pydantic import ValidationError
from flask import request, jsonify
from http import HTTPStatus

logger = logging.getLogger(__name__)


class ValidationTypes(Enum):
    JSON = "json"
    ARGS = "args"
    FORM = "form"


def validate_payload(validator: object, type: ValidationTypes):
    def decorated(f):
        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            try:
                if type == ValidationTypes.ARGS:
                    payload = validator.parse_obj(request.args)
                elif type == ValidationTypes.JSON:
                    payload = validator.parse_obj(request.json)
                else:
                    payload = validator.parse_obj(request.form)
                return f(payload, *args, **kwargs)
            except ValidationError as e:
                logger.warning(e, exc_info=True)
                return jsonify(e.__str__()), HTTPStatus.UNPROCESSABLE_ENTITY
        return wrapped
    return decorated



