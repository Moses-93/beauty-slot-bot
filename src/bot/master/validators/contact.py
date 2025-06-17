from typing import Union
import validators
import phonenumbers


class ContactValidators:

    @staticmethod
    def is_valid_url(url: str) -> bool:
        return validators.url(url.strip())

    @staticmethod
    def parse_phone(phone_str: str, region: str = "UA") -> Union[str, None]:
        try:
            number = phonenumbers.parse(phone_str, region)
            if phonenumbers.is_possible_number(number) and phonenumbers.is_valid_number(
                number
            ):
                return phonenumbers.format_number(
                    number, phonenumbers.PhoneNumberFormat.E164
                )
        except phonenumbers.NumberParseException:
            return None
