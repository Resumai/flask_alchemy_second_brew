
from string import punctuation as valid_symbols
from wtforms import ValidationError

class CustomPasswordValidator():
    def __init__(self):
        self.message = 'Password must have at least one upper letter, one lower letter, one symbol, one number and no space.'

    def __call__(self, form, field):
        text : str = field.data
        is_any_upper = any(c.isupper() for c in text)
        is_any_lower = any(c.islower() for c in text)
        is_any_number = any(c.isdigit() for c in text)
        is_no_space = not any(c.isspace() for c in text)
        is_any_symbol = any(c in valid_symbols for c in text)
        if not all([is_any_upper, is_any_lower, is_any_number, is_no_space, is_any_symbol]):
            raise ValidationError(self.message)