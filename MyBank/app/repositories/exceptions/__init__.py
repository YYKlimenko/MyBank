class FieldError(Exception):

    def __init__(self, message=None):
        if message:
            self.message = message

    def __str__(self):
        return f'FieldError, {self.message}' if self.message else 'FieldError Field(s) are incorrect'

