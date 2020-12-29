import itertools


# class that represents a polynomial
class Polynomial:

    def __init__(self, terms: list, reverse=True):

        # terms are stored from smallest degree first
        # i.e. x + 4 is [4, 1].
        # it will automatically reverse it so [1, 4] which is more recognizable
        # will be put in instead.

        if reverse:
            terms = list(reversed(terms))

        # remove excess 0 terms
        while True:
            if terms[-1] == 0 and len(terms) > 1:
                terms.pop()
            else:
                break

        # let our terms hit the floor
        self.terms = terms
        # degree of the polynomial. used in some calculations
        self.degree = len(terms) - 1

    def __call__(self, *args, **kwargs):
        # calculates the polynomial at the arg

        x = args[0]

        curr_deg = 0
        out = 0
        for i in self.terms:
            # raise x to the whatever power and multiply it by the coefficient.
            out += x ** curr_deg * float(i)
            curr_deg += 1

        return out

    def __add__(self, other):
        # adds two polynomials together
        # not much else to say it's pretty simple.
        if type(other) == Polynomial:
            return Polynomial([x + y for x, y in itertools.zip_longest(self.terms, other.terms, fillvalue=0)],
                              reverse=False)

        elif type(other) == int or type(other) == float:
            return self + Polynomial([other])

    def __mul__(self, other):
        # multiples two polynomials.
        if type(other) == Polynomial:
            # max size will be this
            # extra zeros will be cut down by the polynomial init
            new = [0] * (self.degree + other.degree + 1)
            for ic, i in enumerate(other.terms):
                for jc, j in enumerate(self.terms):
                    # multiply each term and add them.
                    new[ic + jc] += i * j

            return Polynomial(new, reverse=False)

        elif type(other) == int or type(other) == float:
            return self * Polynomial([other])

    def __radd__(self, other):
        # reverse add is normal add but reversed
        return self + other

    def __rmul__(self, other):
        # see above
        return self * other

    def __repr__(self):
        # creates a readable string

        # fallback in case the polynomial is "0"
        if self.degree == 0:
            return str(self.terms[0])

        out = ""
        deg = self.degree
        # for each term
        for i in reversed(self.terms):
            # if the coefficient is 0 skip it
            if i == 0:
                deg -= 1
                continue
            # if the coefficient is 1
            elif i == 1:
                # then if it's not the constant skip it
                if deg == 0:
                    out += str(round(i, 3))
            # see above
            elif i == -1:
                if deg == 0:
                    out += str(round(i, 3))
                # add a minus sign if it's not the constant tho
                else:
                    out += "-"
            else:
                # just add the coefficient
                out += str(round(i, 3))

            # write in the x (either a x^n or an x)
            if deg >= 2:
                out += "x^" + str(deg)
            elif deg == 1:
                out += "x"

            # add the plus sign.
            # TODO: handle negatives correctly
            out += " + "
            deg -= 1

        # strip the string of the extra plus sign.
        return out[:-3]


if __name__ == '__main__':
    a = Polynomial([1, 1, 0])
    b = Polynomial([1, 1, 2, 9137])
