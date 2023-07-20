def compute_gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def compute_lcm(x, y):
    gcd = compute_gcd(x, y)
    lcm = abs(x * y) // gcd
    return lcm