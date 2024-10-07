
def short_number(value):
    try:
        value = float(value)
        if value >= 1_000_000:
            return f'{round(value/1_000_000)}M'
        if value >= 10_000:
            return f'{round(value/1_000)}k'
        elif value >= 1_000:
            return f'{round(value/1_000, 1)}k'
        else:
            return str(int(value))
    except (ValueError, TypeError):
        return value
