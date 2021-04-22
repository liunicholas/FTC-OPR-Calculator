from sympy.matrices.expressions.applyfunc import ElementwiseApplyFunction
from sympy import (Matrix, Lambda, MatrixSymbol, exp, symbols, MatMul, sin, simplify)
from sympy.utilities.pytest import raises
from sympy.matrices.common import ShapeError


X = MatrixSymbol("X", 3, 3)
Y = MatrixSymbol("Y", 3, 3)

k = symbols("k")
Xk = MatrixSymbol("X", k, k)

Xd = X.as_explicit()

x, y, z, t = symbols("x y z t")


def test_applyfunc_matrix():
    double = Lambda(x, x**2)

    expr = ElementwiseApplyFunction(double, Xd)
    assert isinstance(expr, ElementwiseApplyFunction)
    assert expr.doit() == Xd.applyfunc(lambda x: x**2)
    assert expr.shape == (3, 3)
    assert expr.func(*expr.args) == expr
    assert simplify(expr) == expr
    assert expr[0, 0] == double(Xd[0, 0])

    expr = ElementwiseApplyFunction(double, X)
    assert isinstance(expr, ElementwiseApplyFunction)
    assert isinstance(expr.doit(), ElementwiseApplyFunction)
    assert expr == X.applyfunc(double)
    assert expr.func(*expr.args) == expr

    expr = ElementwiseApplyFunction(exp, X*Y)
    assert expr.expr == X*Y
    assert expr.function == exp
    assert expr == (X*Y).applyfunc(exp)
    assert expr.func(*expr.args) == expr

    assert isinstance(X*expr, MatMul)
    assert (X*expr).shape == (3, 3)
    Z = MatrixSymbol("Z", 2, 3)
    assert (Z*expr).shape == (2, 3)

    expr = ElementwiseApplyFunction(exp, Z.T)*ElementwiseApplyFunction(exp, Z)
    assert expr.shape == (3, 3)
    expr = ElementwiseApplyFunction(exp, Z)*ElementwiseApplyFunction(exp, Z.T)
    assert expr.shape == (2, 2)

    raises(ShapeError, lambda: ElementwiseApplyFunction(exp, Z)*ElementwiseApplyFunction(exp, Z))

    M = Matrix([[x, y], [z, t]])
    expr = ElementwiseApplyFunction(sin, M)
    assert isinstance(expr, ElementwiseApplyFunction)
    assert expr.function == sin
    assert expr.expr == M
    assert expr.doit() == M.applyfunc(sin)
    assert expr.doit() == Matrix([[sin(x), sin(y)], [sin(z), sin(t)]])
    assert expr.func(*expr.args) == expr

    expr = ElementwiseApplyFunction(double, Xk)
    assert expr.doit() == expr
    assert expr.subs(k, 2).shape == (2, 2)
    assert (expr*expr).shape == (k, k)
    M = MatrixSymbol("M", k, t)
    expr2 = M.T*expr*M
    assert isinstance(expr2, MatMul)
    assert expr2.args[1] == expr
    assert expr2.shape == (t, t)
    expr3 = expr*M
    assert expr3.shape == (k, t)

    raises(ShapeError, lambda: M*expr)

    expr1 = ElementwiseApplyFunction(lambda x: x+1, Xk)
    expr2 = ElementwiseApplyFunction(lambda x: x, Xk)
    assert expr1 != expr2


def test_applyfunc_entry():

    af = X.applyfunc(sin)
    assert af[0, 0] == sin(X[0, 0])

    af = Xd.applyfunc(sin)
    assert af[0, 0] == sin(X[0, 0])


def test_applyfunc_as_explicit():

    af = X.applyfunc(sin)
    assert af.as_explicit() == Matrix([
        [sin(X[0, 0]), sin(X[0, 1]), sin(X[0, 2])],
        [sin(X[1, 0]), sin(X[1, 1]), sin(X[1, 2])],
        [sin(X[2, 0]), sin(X[2, 1]), sin(X[2, 2])],
    ])
