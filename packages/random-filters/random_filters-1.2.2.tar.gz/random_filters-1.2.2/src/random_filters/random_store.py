from random import randint, choice


def store(*args) -> str:
    """
        It is a function to generate a random store.

        :param: tuple int args: stores to generate a store

        :return: A random store between the present stores.
        :rtype: str

        :Example:
            >>> store(1, 10)
            >>> store(25)
    """
    if len(args) == 0:
        return f'por loja'
    elif len(args) <= 2:
        if isinstance(args, tuple):
            if len(args) == 1:
                return f'na loja {randint(1, args[0])}'
            args = list(args)
            args.sort()
            return f'na loja {randint(args[0], args[-1])}'
        else:
            return f'Insert a list or tuple of stores.'
    else:
        args = list(args)
        args.sort()
        return f'na loja {choice(args)}'
