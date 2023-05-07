def code(x, y):
    z = x + y
    if z == 0:
        if y > 0:
            z = y - x
        else:
            z = x - y
    else:
        if x > 0:
            z = z - x
        else:
            z = z + x
    return z
