from fractions import gcd
from math import atan2, sin, cos, pi


####################
# Rational numbers #
####################

def add_rational(x, y):
    """Add rational numbers x and y."""
    nx, dx = x.numer, x.denom
    ny, dy = y.numer, y.denom
    return Rational(nx * dy + ny * dx, dx * dy)


def sub_rational(x, y):
    """Add rational numbers x and y."""
    nx, dx = x.numer, x.denom
    ny, dy = y.numer, y.denom
    return Rational(nx * dy - ny * dx, dx * dy)

def div_rational(x,y):
    return Rational(x.numer * y.denom, x.denom * y.numer)


def mul_rational(x, y):
    """Multiply rational numbers x and y."""
    return Rational(x.numer * y.numer, x.denom * y.denom)


class Rational(object):
    """A rational number represented as a numerator and denominator.
    All rational numbers are represented in lowest terms.
    >>> Rational(6, 4)
    Rational(3, 2)
    >>> add_rational(Rational(3, 14), Rational(2, 7))
    Rational(1, 2)
    >>> mul_rational(Rational(7, 10), Rational(2, 7))
    Rational(1, 5)
    """

    def __init__(self, numer, denom):
        g = gcd(numer, denom)
        self.numer = numer // g
        self.denom = denom // g

    def __repr__(self):
        return 'Rational({0}, {1})'.format(self.numer, self.denom)

    def __str__(self):
        return '{0}/{1}'.format(self.numer, self.denom)

    def __add__(self, other):
        return coerce_apply('add', self ,other)
        # return apply('add', self ,other)

    def __mul__(self, other):
        return coerce_apply('mul', self ,other)
        # return apply('mul', self ,other)

    def __sub__(self, other):
        return coerce_apply('sub', self ,other)
        # return apply('sub', self ,other)

###################
# Complex numbers #
###################

def add_complex(z1, z2):
    """Return a complex number z1 + z2"""
    return ComplexRI(z1.real + z2.real, z1.imag + z2.imag)


def sub_complex(z1, z2):
    return ComplexRI(z1.real - z2.real, z1.imag + z2.imag)


def mul_complex(z1, z2):
    """Return a complex number z1 * z2"""
    return ComplexMA(z1.magnitude * z2.magnitude, z1.angle + z2.angle)

def div_complex(z1, z2):
    """Return a complex number z1 * z2"""
    return ComplexMA(z1.magnitude / z2.magnitude, z1.angle - z2.angle)


class ComplexRI(object):
    """A rectangular representation of a complex number.

    >>> from math import pi
    >>> add_complex(ComplexRI(1, 2), ComplexMA(2, pi/2))
    ComplexRI(1.0000000000000002, 4.0)
    >>> mul_complex(ComplexRI(0, 1), ComplexRI(0, 1))
    ComplexMA(1.0, 3.141592653589793)
    """

    def __init__(self, real, imag):
        self.real = real
        self.imag = imag

    @property
    def magnitude(self):
        return (self.real ** 2 + self.imag ** 2) ** 0.5

    @property
    def angle(self):
        return atan2(self.imag, self.real)

    def __repr__(self):
        return 'ComplexRI({0}, {1})'.format(self.real, self.imag)

    def __add__(self, other):
        # return apply('add', self ,other)
        return coerce_apply('add', self ,other)

    def __mul__(self, other):
        return coerce_apply('mul', self ,other)
        # return apply('mul', self ,other)

    def __sub__(self, other):
        return coerce_apply('sub', self ,other)
        # return apply('sub', self ,other)



class ComplexMA(object):
    """A polar representation of a complex number."""

    def __init__(self, magnitude, angle):
        self.magnitude = magnitude
        self.angle = angle

    @property
    def real(self):
        return self.magnitude * cos(self.angle)

    @property
    def imag(self):
        return self.magnitude * sin(self.angle)

    def __repr__(self):
        return 'ComplexMA({0}, {1})'.format(self.magnitude, self.angle)

    def __add__(self, other):
        return coerce_apply('add', self ,other)
        # return apply('add', self ,other)

    def __mul__(self, other):
        return coerce_apply('mul', self ,other)
        # return apply('mul', self ,other)

    def __sub__(self, other):
        return coerce_apply('sub', self ,other)
        # return apply('sub', self ,other)


##############################
# Tag-based type dispatching #
##############################

def type_tag(x):
    """Return the tag associated with the type of x."""
    return type_tag.tags[type(x)]


type_tag.tags = {ComplexRI: 'com', ComplexMA: 'com', Rational: 'rat'}



def add_complex_and_rational(z, r):
    return ComplexRI(z.real + float(r.numer) / r.denom, z.imag)


def sub_complex_and_rational(z, r):
    return ComplexRI(z.real - float(r.numer) / r.denom, z.imag)


def mul_complex_and_rational(z, r):
    return ComplexMA(z.magnitude * r.numer / r.denom, z.angle)


add_rational_and_complex = lambda r, z: add_complex_and_rational(z, r)
sub_rational_and_complex = lambda r, z: sub_complex_and_rational(z, r)
mul_rational_and_complex = lambda r, z: mul_complex_and_rational(z, r)













############
# Coercion #
############

def rational_to_complex(x):
    return ComplexRI(x.numer / x.denom, 0)


coercions = {('rat', 'com'): rational_to_complex}


def coerce_apply(operator_name, x, y):
    """Apply an operation ('add' or 'mul') to x and y.

    >>> coerce_apply('add', ComplexRI(1.5, 0), Rational(3, 2))
    ComplexRI(3.0, 0)
    >>> coerce_apply('mul', Rational(1, 2), ComplexMA(10, 1))
    ComplexMA(5.0, 1.0)
    """
    tx, ty = type_tag(x), type_tag(y)
    if tx != ty:
        if (tx, ty) in coercions:
            tx, x = ty, coercions[(tx, ty)](x)
        elif (ty, tx) in coercions:
            ty, y = tx, coercions[(ty, tx)](y)
        else:
            return 'No coercion possible.'
    assert tx == ty
    key = (operator_name, tx)
    return coerce_apply.implementations[key](x, y)


coerce_apply.implementations = {('mul', 'com'): mul_complex,
                                ('mul', 'rat'): mul_rational,
                                ('add', 'com'): add_complex,
                                ('add', 'rat'): add_rational,
                                ('sub','com'): sub_complex,
                                ('sub','rat'): sub_rational,
                                ('div','rat'): div_rational,
                                ('div','com'): div_complex
                                }


def apply(operator_name, x, y):
    tags = (type_tag(x), type_tag(y))
    key = (operator_name, tags)
    return apply.implementations[key](x, y)


apply.implementations = {
    ('add', ('com', 'com')): add_complex,
    ('add', ('com', 'rat')): add_complex_and_rational,
    ('add', ('rat', 'com')): add_rational_and_complex,
    ('add', ('rat', 'rat')): add_rational,
    ('sub', ('com', 'com')): sub_complex,
    ('sub', ('com', 'rat')): sub_complex_and_rational,
    ('sub', ('rat', 'com')): sub_rational_and_complex,
    ('sub', ('rat', 'rat')): sub_rational,
    ('mul', ('com', 'com')): mul_complex,
    ('mul', ('com', 'rat')): mul_complex_and_rational,
    ('mul', ('rat', 'com')): mul_rational_and_complex,
    ('mul', ('rat', 'rat')): mul_rational
}


def driver():
    # 1
    print(Rational(6, 4))  # Rational(3, 2)
    print(add_rational(Rational(3, 14), Rational(2, 7)))  # Rational(1, 2)
    print(mul_rational(Rational(7, 10), Rational(2, 7)))  # print Rational(1, 5)
    # 2
    from math import pi
    print(add_complex(ComplexRI(1, 2), ComplexMA(2, pi / 2)))  # ComplexRI(1.0000000000000002, 4.0)
    print(mul_complex(ComplexRI(0, 1), ComplexRI(0, 1)))  # ComplexMA(1.0, 3.141592653589793)
    print(apply('add', Rational(3, 14), Rational(2, 7)))
    print(apply('add', ComplexRI(1, 2), ComplexMA(2, pi / 2)))
    print (apply('sub', ComplexRI(1, 2), Rational(2, 3))) #ComplexRI(0.3333333333, 2)
    print (ComplexRI(1, 2) + ComplexMA(2, pi/2)) #ComplexRI(1.0000000000000002, 4.0)
    print (ComplexRI(0, 1) * ComplexRI(0, 1)) # ComplexMA(1.0, 3.141592653589793)
    print (ComplexRI(1, 2) - Rational(2, 3)) #ComplexRI(0.3333333333, 2)
    print(coerce_apply('add', ComplexRI(1, 2), ComplexMA(2, pi / 2)))
    # ComplexRI(1.0000000000000002, 4.0 )
    print(coerce_apply('mul', ComplexRI(0, 1), ComplexRI(0, 1)))
    # ComplexMA(1.0, 3.141592653589793) )
    print(coerce_apply('sub', ComplexRI(1, 2), Rational(2, 3)))
    # ComplexRI(0.3333333333, 2)
driver()
