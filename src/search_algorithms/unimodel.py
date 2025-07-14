import math


def grid_search(func, lo, hi, tol=None, max_iter=100):
    if max_iter == 1:
        return func((lo + hi) / 2), (lo + hi) / 2

    if tol is not None:
        max_iter = max(2, min(max_iter, math.ceil((hi - lo) / tol)))

    step = (hi - lo) / (max_iter - 1)
    x = lo
    min_fx, min_x = math.inf, 0

    for i in range(max_iter):
        x = lo + step * i
        fx = func(x)

        if fx < min_fx:
            min_x, min_fx = x, fx

    return min_fx, min_x


def golden_section_search(func, lo, hi, tol=1e-9, max_iter=100):
    invphi = (math.sqrt(5) - 1) / 2  # ≈ 0.618

    x1 = hi - (hi - lo) * invphi
    x2 = lo + (hi - lo) * invphi
    f1, f2 = func(x1), func(x2)

    for _ in range(max_iter):
        if abs(hi - lo) < tol:
            break

        if f1 <= f2:
            hi = x2
            x2, f2 = x1, f1
            x1 = hi - (hi - lo) * invphi
            f1 = func(x1)
        else:
            lo = x1
            x1, f1 = x2, f2
            x2 = lo + (hi - lo) * invphi
            f2 = func(x2)

    if f1 < f2:
        return f1, x1
    else:
        return f2, x2


def brent_search(func, lo, hi, tol=1e-9, max_iter=100):
    # Initialization
    a, b = lo, hi
    x = w = v = a + 0.5 * (b - a)
    fx = fw = fv = func(x)
    d = e = 0.0

    for _ in range(max_iter):
        xm = 0.5 * (a + b)
        tol1 = tol * abs(x) + 1e-10
        tol2 = 2.0 * tol1

        # Check for convergence
        if abs(x - xm) <= tol2 - 0.5 * (b - a):
            return fx, x

        p = q = r = 0.0
        u = None

        if abs(e) > tol1:
            r = (x - w) * (fx - fv)
            q = (x - v) * (fx - fw)
            p = (x - v) * q - (x - w) * r
            q = 2.0 * (q - r)
            if q > 0.0:
                p = -p
            q = abs(q)
            etemp = e
            e = d

            # Accept parabolic step if within bounds
            if abs(p) < abs(0.5 * q * etemp) and a <= x + p / q <= b:
                d = p / q
                u = x + d
                if not (a + tol1 <= u <= b - tol1):
                    u = x + (tol1 if d > 0 else -tol1)
            else:
                e = b - x if x < xm else a - x
                d = 0.3819660 * e
        else:
            e = b - x if x < xm else a - x
            d = 0.3819660 * e

        u = x + (d if abs(d) >= tol1 else tol1 if d > 0 else -tol1)
        fu = func(u)

        if fu <= fx:
            if u < x:
                b = x
            else:
                a = x
            v, fv = w, fw
            w, fw = x, fx
            x, fx = u, fu
        else:
            if u < x:
                a = u
            else:
                b = u
            if fu <= fw or w == x:
                v, fv = w, fw
                w, fw = u, fu
            elif fu <= fv or v == x or v == w:
                v, fv = u, fu

    return fx, x  # Return best guess after max_iter
