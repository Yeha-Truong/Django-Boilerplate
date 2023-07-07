from rest_framework.serializers import ValidationError


def _raiseValidatorError(message):
    raise ValidationError(detail=message)


def min_length(length: int):
    if length < 0:
        raise Exception("Invalid minimum length!")
    else:
        return (
            lambda value: _raiseValidatorError(
                "Text length must be longer than {length}".format(length=str(length))
            )
            if value.length < length
            else None
        )
