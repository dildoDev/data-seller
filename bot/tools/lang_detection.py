def detect(phone_number: str) -> str:
    match phone_number:
        case "+7":
            return "ru"
        case "+375":
            return "ru"
        case _:
            return "en"