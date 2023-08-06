from random import choice, randint

from pandas import DataFrame


def combobox(*args, hierarchy=False) -> str:
    """
        It is a function with the equivalent values of the present combobox in the question.

        :param args: The values of the combobox.
        :param hierarchy: If the combobox has simple hierarchy.

        :return: A random combobox between the present combobox.
        :rtype: str

        :Example:
            >>> combobox("estado", "cidade", "canal", "tipo", "loja", hierarchy=True)
            >>> combobox("estado", "cidade", "canal", "tipo")
    """
    if len(args) > 1:
        if hierarchy:
            args = list(args)
            first = choice(args[:-1])
            args = args[args.index(first):]
            second = choice(args)
            if second == first:
                return f'por {first.capitalize()}'
            return f'por {first.capitalize()} e por {second.capitalize()}'
        else:
            return f'por {choice(args).capitalize()}'
    else:
        return f'por {args[0].capitalize()}'


def combobox_hierarchy(data: dict | DataFrame) -> str:
    """
        It is a function with generate a random combobox with hierarchy.

        :param data: A dict or DataFrame with the data.

        :return: A random combobox between the present combobox.
        :rtype: str

        :Example:
            >>> combobox_hierarchy({'a': [1, 2, 3], 'b': [4, 5, 6]})
    """
    if isinstance(data, dict):
        df = DataFrame(data)
        first = choice(df.iloc[:, 0])
        df = df[df.iloc[:, 0] == first]
        second = randint(0, len(df) - 1)
        return f'{df.columns[0]} {first.upper()} e {df.columns[1]} {df.iloc[second, 1].capitalize()}'
    elif isinstance(data, DataFrame):
        first = choice(data.iloc[:, 0])
        df = data[data.iloc[:, 0] == first]
        second = randint(0, len(df) - 1)
        return f'{df.columns[0]} {first.upper()} e {df.columns[1]} {df.iloc[second, 1].capitalize()}'
    else:
        raise TypeError('The data must be a dict or a DataFrame')
