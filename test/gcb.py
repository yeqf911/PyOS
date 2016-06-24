def gcd(p, q):
    result = 1
    if p > q:
        c = p % q
        if c == 0:
            return q
        else:
            return gcd(q, c)
    else:
        c = q % p
        if c == 0:
            return p
        else:
            return gcd(p, c)

x = gcd(3, 2)
print x