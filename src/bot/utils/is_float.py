async def is_float_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
