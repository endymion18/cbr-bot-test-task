
async def parse_args(args: str, currencies: list):
    if args is None:
        raise AttributeError("Введите, пожалуйста, необходимые аргументы\n"
                             "Например, /exchange USD RUB 10")

    args = args.split()
    if len(args) > 3:
        raise AttributeError("Введено слишком много аргументов")
    if len(args) < 3:
        raise AttributeError("Введено слишком мало аргументов")
    if args[0].upper() not in currencies:
        raise AttributeError("Первым аргументом введена неправильная валюта")
    if args[1].upper() not in currencies:
        raise AttributeError("Вторым аргументом введена неправильная валюта")
    if not args[2].isdecimal():
        raise AttributeError("Третьим аргументом должно быть корректное число")

    return args[0].upper(), args[1].upper(), int(args[2])

