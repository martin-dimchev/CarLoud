from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class IsAlphaValidator:

    def __init__(self, message=None):
        self.message = message

    @property
    def message(self):
        return self.__message

    @message.setter
    def message(self, value):
        if not value:
            self.__message = 'This field must contain only characters.'

    def __call__(self, value):
        if not value.isalpha():
            raise ValidationError(message=self.message)

@deconstructible
class CapFirstValidator:

    def __init__(self, message=None):
        self.message = message

    @property
    def message(self):
        return self.__message

    @message.setter
    def message(self, value):
        if not value:
            self.__message = 'This field must start with a capital letter.'
        else:
            self.__message = value

    def __call__(self, value):
        if value:
            if not value[0].isupper():
                raise ValidationError(message=self.message)
