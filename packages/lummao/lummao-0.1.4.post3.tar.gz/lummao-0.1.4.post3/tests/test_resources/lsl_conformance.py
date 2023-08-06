from lummao import *


class Script(BaseLSLScript):
    gTestsPassed: int
    gTestsFailed: int
    gInteger: int
    gFloat: float
    gString: str
    gVector: Vector
    gRot: Quaternion
    gList: list
    gCallOrder: list

    def __init__(self):
        super().__init__()
        self.gTestsPassed = 0
        self.gTestsFailed = 0
        self.gInteger = 5
        self.gFloat = bin2float('1.500000', '0000c03f')
        self.gString = "foo"
        self.gVector = Vector((1.0, 2.0, 3.0))
        self.gRot = Quaternion((1.0, 2.0, 3.0, 4.0))
        self.gList = [1, 2, 3]
        self.gCallOrder = []

    def testPassed(self, _description: str, _actual: str, _expected: str) -> None:
        self.gTestsPassed += 1

    def testFailed(self, _description: str, _actual: str, _expected: str) -> None:
        self.gTestsFailed += 1
        print(radd(")", radd(_expected, radd(" expected ", radd(_actual, radd(" (", radd(_description, "FAILED!: ")))))))
        self.builtin_funcs.llOwnerSay(typecast(rdiv(0, 0), str))

    def ensureTrue(self, _description: str, _actual: int) -> None:
        if cond(_actual):
            self.testPassed(_description, typecast(_actual, str), typecast(1, str))
        else:
            self.testFailed(_description, typecast(_actual, str), typecast(1, str))

    def ensureFalse(self, _description: str, _actual: int) -> None:
        if cond(_actual):
            self.testFailed(_description, typecast(_actual, str), typecast(0, str))
        else:
            self.testPassed(_description, typecast(_actual, str), typecast(0, str))

    def ensureIntegerEqual(self, _description: str, _actual: int, _expected: int) -> None:
        if cond(req(_expected, _actual)):
            self.testPassed(_description, typecast(_actual, str), typecast(_expected, str))
        else:
            self.testFailed(_description, typecast(_actual, str), typecast(_expected, str))

    def floatEqual(self, _actual: float, _expected: float) -> int:
        _error: float = self.builtin_funcs.llFabs(rsub(_actual, _expected))
        _epsilon: float = bin2float('0.001000', '6f12833a')
        if cond(rgreater(_epsilon, _error)):
            print(radd(typecast(_error, str), "Float equality delta "))
            return 0
        return 1

    def ensureFloatEqual(self, _description: str, _actual: float, _expected: float) -> None:
        if cond(self.floatEqual(_actual, _expected)):
            self.testPassed(_description, typecast(_actual, str), typecast(_expected, str))
        else:
            self.testFailed(_description, typecast(_actual, str), typecast(_expected, str))

    def ensureStringEqual(self, _description: str, _actual: str, _expected: str) -> None:
        if cond(req(_expected, _actual)):
            self.testPassed(_description, typecast(_actual, str), typecast(_expected, str))
        else:
            self.testFailed(_description, typecast(_actual, str), typecast(_expected, str))

    def ensureVectorEqual(self, _description: str, _actual: Vector, _expected: Vector) -> None:
        if cond(rbooland(self.floatEqual(_actual[2], _expected[2]), rbooland(self.floatEqual(_actual[1], _expected[1]), self.floatEqual(_actual[0], _expected[0])))):
            self.testPassed(_description, typecast(_actual, str), typecast(_expected, str))
        else:
            self.testFailed(_description, typecast(_actual, str), typecast(_expected, str))

    def ensureRotationEqual(self, _description: str, _actual: Quaternion, _expected: Quaternion) -> None:
        if cond(rbooland(self.floatEqual(_actual[3], _expected[3]), rbooland(self.floatEqual(_actual[2], _expected[2]), rbooland(self.floatEqual(_actual[1], _expected[1]), self.floatEqual(_actual[0], _expected[0]))))):
            self.testPassed(_description, typecast(_actual, str), typecast(_expected, str))
        else:
            self.testFailed(_description, typecast(_actual, str), typecast(_expected, str))

    def ensureListEqual(self, _description: str, _actual: list, _expected: list) -> None:
        if cond(rbooland((req(typecast(_expected, str), typecast(_actual, str))), req(_expected, _actual))):
            self.testPassed(_description, typecast(_actual, str), typecast(_expected, str))
        else:
            self.testFailed(_description, typecast(_actual, str), typecast(_expected, str))

    def callOrderFunc(self, _num: int) -> int:
        self.gCallOrder = radd([_num], self.gCallOrder)
        return 1

    def testReturn(self) -> int:
        return 1

    def testReturnFloat(self) -> float:
        return 1.0

    def testReturnString(self) -> str:
        return "Test string"

    def testReturnList(self) -> list:
        return [1, 2, 3]

    def testReturnVector(self) -> Vector:
        return Vector((1.0, 2.0, 3.0))

    def testReturnRotation(self) -> Quaternion:
        return Quaternion((1.0, 2.0, 3.0, 4.0))

    def testReturnVectorNested(self) -> Vector:
        return self.testReturnVector()

    def testReturnVectorWithLibraryCall(self) -> Vector:
        self.builtin_funcs.llSin(0.0)
        return Vector((1.0, 2.0, 3.0))

    def testReturnRotationWithLibraryCall(self) -> Quaternion:
        self.builtin_funcs.llSin(0.0)
        return Quaternion((1.0, 2.0, 3.0, 4.0))

    def testParameters(self, _param: int) -> int:
        _param = radd(1, _param)
        return _param

    def testRecursion(self, _param: int) -> int:
        if cond(rleq(0, _param)):
            return 0
        else:
            return self.testRecursion(rsub(1, _param))

    def testExpressionLists(self, _l: list) -> str:
        return radd(typecast(_l, str), "foo")

    @with_goto
    def tests(self) -> None:
        _a: Optional[list] = None
        _b: Optional[list] = None
        _c: Optional[list] = None
        _i: int = 0
        _v: Vector = Vector((0.0, 0.0, 0.0))
        _q: Quaternion = Quaternion((0.0, 0.0, 0.0, 0.0))
        _l: Optional[list] = None
        _l2: Optional[list] = None
        self.ensureIntegerEqual("TRUE", 1, 1)
        self.ensureIntegerEqual("FALSE", 0, 0)
        if cond(0.0):
            self.testFailed("if(0.0)", "TRUE", "FALSE")
        else:
            self.testPassed("if(0.0)", "TRUE", "TRUE")
        if cond(bin2float('0.000001', 'bd378635')):
            self.testPassed("if(0.000001)", "TRUE", "TRUE")
        else:
            self.testFailed("if(0.000001)", "TRUE", "FALSE")
        if cond(bin2float('0.900000', '6666663f')):
            self.testPassed("if(0.9)", "TRUE", "TRUE")
        else:
            self.testFailed("if(0.9)", "TRUE", "FALSE")
        if cond(Vector((0.0, 0.0, 0.0))):
            self.testFailed("if(ZERO_VECTOR)", "TRUE", "FALSE")
        else:
            self.testPassed("if(ZERO_VECTOR)", "TRUE", "TRUE")
        if cond(Quaternion((0.0, 0.0, 0.0, 1.0))):
            self.testFailed("if(ZERO_ROTATION)", "TRUE", "FALSE")
        else:
            self.testPassed("if(ZERO_ROTATION)", "TRUE", "TRUE")
        if cond("00000000-0000-0000-0000-000000000000"):
            self.testPassed("if(NULL_KEY)", "TRUE", "TRUE")
        else:
            self.testFailed("if(NULL_KEY)", "TRUE", "FALSE")
        if cond(typecast("00000000-0000-0000-0000-000000000000", Key)):
            self.testFailed("if((key)NULL_KEY)", "TRUE", "FALSE")
        else:
            self.testPassed("if((key)NULL_KEY)", "TRUE", "TRUE")
        if cond(""):
            self.testFailed("if(\"\")", "TRUE", "FALSE")
        else:
            self.testPassed("if(\"\")", "TRUE", "TRUE")
        if cond([]):
            self.testFailed("if([])", "TRUE", "FALSE")
        else:
            self.testPassed("if([])", "TRUE", "TRUE")
        self.ensureIntegerEqual("(TRUE == TRUE)", (req(1, 1)), 1)
        self.ensureIntegerEqual("(TRUE == FALSE)", (req(0, 1)), 0)
        self.ensureIntegerEqual("(FALSE == TRUE)", (req(1, 0)), 0)
        self.ensureIntegerEqual("(FALSE == FALSE)", (req(0, 0)), 1)
        self.ensureIntegerEqual("(TRUE != TRUE)", (rneq(1, 1)), 0)
        self.ensureIntegerEqual("(TRUE != FALSE)", (rneq(0, 1)), 1)
        self.ensureIntegerEqual("(FALSE != TRUE)", (rneq(1, 0)), 1)
        self.ensureIntegerEqual("(FALSE != FALSE)", (rneq(0, 0)), 0)
        self.ensureIntegerEqual("(TRUE && TRUE)", (rbooland(1, 1)), 1)
        self.ensureIntegerEqual("(TRUE && FALSE)", (rbooland(0, 1)), 0)
        self.ensureIntegerEqual("(FALSE && TRUE)", (rbooland(1, 0)), 0)
        self.ensureIntegerEqual("(FALSE && FALSE)", (rbooland(0, 0)), 0)
        self.ensureIntegerEqual("(1 && 2)", (rbooland(2, 1)), 1)
        self.ensureIntegerEqual("(1 && 0)", (rbooland(0, 1)), 0)
        self.ensureIntegerEqual("(0 && 2)", (rbooland(2, 0)), 0)
        self.ensureIntegerEqual("(0 && 0)", (rbooland(0, 0)), 0)
        self.ensureIntegerEqual("(TRUE || TRUE)", (rboolor(1, 1)), 1)
        self.ensureIntegerEqual("(TRUE || FALSE)", (rboolor(0, 1)), 1)
        self.ensureIntegerEqual("(FALSE || TRUE)", (rboolor(1, 0)), 1)
        self.ensureIntegerEqual("(FALSE || FALSE)", (rboolor(0, 0)), 0)
        self.ensureIntegerEqual("(1 || 2)", (rboolor(2, 1)), 1)
        self.ensureIntegerEqual("(1 || 0)", (rboolor(0, 1)), 1)
        self.ensureIntegerEqual("(0 || 2)", (rboolor(2, 0)), 1)
        self.ensureIntegerEqual("(0 || 0)", (rboolor(0, 0)), 0)
        self.ensureIntegerEqual("(! TRUE)", (boolnot(1)), 0)
        self.ensureIntegerEqual("(! FALSE)", (boolnot(0)), 1)
        self.ensureIntegerEqual("(! 2)", (boolnot(2)), 0)
        self.ensureIntegerEqual("(! 0)", (boolnot(0)), 1)
        self.ensureIntegerEqual("(1 > 0)", (rgreater(0, 1)), 1)
        self.ensureIntegerEqual("(0 > 1)", (rgreater(1, 0)), 0)
        self.ensureIntegerEqual("(1 > 1)", (rgreater(1, 1)), 0)
        self.ensureIntegerEqual("(0 < 1)", (rless(1, 0)), 1)
        self.ensureIntegerEqual("(1 < 0)", (rless(0, 1)), 0)
        self.ensureIntegerEqual("(1 < 1)", (rless(1, 1)), 0)
        self.ensureIntegerEqual("(1 >= 0)", (rgeq(0, 1)), 1)
        self.ensureIntegerEqual("(0 >= 1)", (rgeq(1, 0)), 0)
        self.ensureIntegerEqual("(1 >= 1)", (rgeq(1, 1)), 1)
        self.ensureIntegerEqual("(0 <= 1)", (rleq(1, 0)), 1)
        self.ensureIntegerEqual("(1 <= 0)", (rleq(0, 1)), 0)
        self.ensureIntegerEqual("(1 <= 1)", (rleq(1, 1)), 1)
        self.ensureIntegerEqual("(10 & 25)", (rbitand(25, 10)), 8)
        self.ensureIntegerEqual("(10 | 25)", (rbitor(25, 10)), 27)
        self.ensureIntegerEqual("~10", bitnot(10), -11)
        self.ensureIntegerEqual("(10 ^ 25)", (rbitxor(25, 10)), 19)
        self.ensureIntegerEqual("(523 >> 2)", (rshr(2, 523)), 130)
        self.ensureIntegerEqual("(523 << 2)", (rshl(2, 523)), 2092)
        self.ensureIntegerEqual("(1 + 1)", (radd(1, 1)), 2)
        self.ensureFloatEqual("(1 + 1.1)", (radd(bin2float('1.100000', 'cdcc8c3f'), 1.0)), bin2float('2.100000', '66660640'))
        self.ensureFloatEqual("(1.1 + 1)", (radd(1.0, bin2float('1.100000', 'cdcc8c3f'))), bin2float('2.100000', '66660640'))
        self.ensureFloatEqual("(1.1 + 1.1)", (radd(bin2float('1.100000', 'cdcc8c3f'), bin2float('1.100000', 'cdcc8c3f'))), bin2float('2.200000', 'cdcc0c40'))
        self.ensureStringEqual("\"foo\" + \"bar\"", radd("bar", "foo"), "foobar")
        self.ensureVectorEqual("(<1.1, 2.2, 3.3> + <4.4, 5.5, 6.6>)", (radd(Vector((bin2float('4.400000', 'cdcc8c40'), bin2float('5.500000', '0000b040'), bin2float('6.600000', '3333d340'))), Vector((bin2float('1.100000', 'cdcc8c3f'), bin2float('2.200000', 'cdcc0c40'), bin2float('3.300000', '33335340'))))), Vector((bin2float('5.500000', '0000b040'), bin2float('7.700000', '6666f640'), bin2float('9.900000', '66661e41'))))
        self.ensureRotationEqual("(<1.1, 2.2, 3.3, 4.4> + <4.4, 5.5, 6.6, 3.3>)", (radd(Quaternion((bin2float('4.400000', 'cdcc8c40'), bin2float('5.500000', '0000b040'), bin2float('6.600000', '3333d340'), bin2float('3.300000', '33335340'))), Quaternion((bin2float('1.100000', 'cdcc8c3f'), bin2float('2.200000', 'cdcc0c40'), bin2float('3.300000', '33335340'), bin2float('4.400000', 'cdcc8c40'))))), Quaternion((bin2float('5.500000', '0000b040'), bin2float('7.700000', '6666f640'), bin2float('9.900000', '66661e41'), bin2float('7.700000', '6666f640'))))
        self.ensureListEqual("([1] + 2)", (radd(2, [1])), [1, 2])
        self.ensureListEqual("([] + 1.5)", (radd(bin2float('1.500000', '0000c03f'), [])), [bin2float('1.500000', '0000c03f')])
        self.ensureListEqual("([\"foo\"] + \"bar\")", (radd("bar", ["foo"])), ["foo", "bar"])
        self.ensureListEqual("([] + <1,2,3>)", (radd(Vector((1.0, 2.0, 3.0)), [])), [Vector((1.0, 2.0, 3.0))])
        self.ensureListEqual("([] + <1,2,3,4>)", (radd(Quaternion((1.0, 2.0, 3.0, 4.0)), [])), [Quaternion((1.0, 2.0, 3.0, 4.0))])
        self.ensureListEqual("(1 + [2])", (radd([2], 1)), [1, 2])
        self.ensureListEqual("(1.0 + [2])", (radd([2], 1.0)), [1.0, 2])
        self.ensureListEqual("(1 + [2])", (radd([2], "one")), ["one", 2])
        self.ensureListEqual("(<1.0,1.0,1.0,1.0> + [2])", (radd([2], Quaternion((1.0, 1.0, 1.0, 1.0)))), [Quaternion((1.0, 1.0, 1.0, 1.0)), 2])
        self.ensureListEqual("(<1.0,1.0,1.0> + [2])", (radd([2], Vector((1.0, 1.0, 1.0)))), [Vector((1.0, 1.0, 1.0)), 2])
        _a = []
        _b = _a
        _a = radd(["foo"], _a)
        self.ensureListEqual("list a = []; list b = a; a += [\"foo\"]; a == [\"foo\"]", _a, ["foo"])
        self.ensureListEqual("list a = []; list b = a; a += [\"foo\"]; b == []", _b, [])
        _a = ["a"]
        _b = ["b"]
        _c = radd(_b, _a)
        self.ensureListEqual("a = [\"a\"]; b = [\"b\"]; list c = a + b; a == [\"a\"];", _a, ["a"])
        self.ensureListEqual("a = [\"a\"]; b = [\"b\"]; list c = a + b; b == [\"b\"];", _b, ["b"])
        self.ensureListEqual("a = [\"a\"]; b = [\"b\"]; list c = a + b; c == [\"a\", \"b\"];", _c, ["a", "b"])
        self.ensureIntegerEqual("(1 - 1)", (rsub(1, 1)), 0)
        self.ensureFloatEqual("(1 - 0.5)", (rsub(bin2float('0.500000', '0000003f'), 1.0)), bin2float('0.500000', '0000003f'))
        self.ensureFloatEqual("(1.5 - 1)", (rsub(1.0, bin2float('1.500000', '0000c03f'))), bin2float('0.500000', '0000003f'))
        self.ensureFloatEqual("(2.2 - 1.1)", (rsub(bin2float('1.100000', 'cdcc8c3f'), bin2float('2.200000', 'cdcc0c40'))), bin2float('1.100000', 'cdcc8c3f'))
        self.ensureVectorEqual("(<1.5, 2.5, 3.5> - <4.5, 5.5, 6.5>)", (rsub(Vector((bin2float('4.500000', '00009040'), bin2float('5.500000', '0000b040'), bin2float('6.500000', '0000d040'))), Vector((bin2float('1.500000', '0000c03f'), bin2float('2.500000', '00002040'), bin2float('3.500000', '00006040'))))), Vector((-3.0, -3.0, -3.0)))
        self.ensureRotationEqual("(<1.5, 2.5, 3.5, 4.5> - <4.5, 5.5, 6.5, 7.5>)", (rsub(Quaternion((bin2float('4.500000', '00009040'), bin2float('5.500000', '0000b040'), bin2float('6.500000', '0000d040'), bin2float('7.500000', '0000f040'))), Quaternion((bin2float('1.500000', '0000c03f'), bin2float('2.500000', '00002040'), bin2float('3.500000', '00006040'), bin2float('4.500000', '00009040'))))), Quaternion((-3.0, -3.0, -3.0, -3.0)))
        self.ensureIntegerEqual("(2 * 3)", (rmul(3, 2)), 6)
        self.ensureFloatEqual("(2 * 3.5)", (rmul(bin2float('3.500000', '00006040'), 2.0)), 7.0)
        self.ensureFloatEqual("(2.5 * 3)", (rmul(3.0, bin2float('2.500000', '00002040'))), bin2float('7.500000', '0000f040'))
        self.ensureFloatEqual("(2.5 * 3.5)", (rmul(bin2float('3.500000', '00006040'), bin2float('2.500000', '00002040'))), bin2float('8.750000', '00000c41'))
        self.ensureVectorEqual("(<1.1, 2.2, 3.3> * 2)", (rmul(2.0, Vector((bin2float('1.100000', 'cdcc8c3f'), bin2float('2.200000', 'cdcc0c40'), bin2float('3.300000', '33335340'))))), Vector((bin2float('2.200000', 'cdcc0c40'), bin2float('4.400000', 'cdcc8c40'), bin2float('6.600000', '3333d340'))))
        self.ensureVectorEqual("(2 * <1.1, 2.2, 3.3>)", (rmul(2.0, Vector((bin2float('1.100000', 'cdcc8c3f'), bin2float('2.200000', 'cdcc0c40'), bin2float('3.300000', '33335340'))))), (rmul(Vector((bin2float('1.100000', 'cdcc8c3f'), bin2float('2.200000', 'cdcc0c40'), bin2float('3.300000', '33335340'))), 2.0)))
        self.ensureVectorEqual("(<2.2, 4.4, 6.6> * 2.0)", (rmul(2.0, Vector((bin2float('2.200000', 'cdcc0c40'), bin2float('4.400000', 'cdcc8c40'), bin2float('6.600000', '3333d340'))))), Vector((bin2float('4.400000', 'cdcc8c40'), bin2float('8.800000', 'cdcc0c41'), bin2float('13.200000', '33335341'))))
        self.ensureVectorEqual("(2.0 * <2.2, 4.4, 6.6>)", (rmul(2.0, Vector((bin2float('2.200000', 'cdcc0c40'), bin2float('4.400000', 'cdcc8c40'), bin2float('6.600000', '3333d340'))))), (rmul(Vector((bin2float('2.200000', 'cdcc0c40'), bin2float('4.400000', 'cdcc8c40'), bin2float('6.600000', '3333d340'))), 2.0)))
        self.ensureFloatEqual("<1,3,-5> * <4,-2,-1>", rmul(Vector((4.0, -2.0, -1.0)), Vector((1.0, 3.0, -5.0))), 3.0)
        self.ensureVectorEqual("<-1,0,0> * <0, 0, 0.707, 0.707>", rmul(Quaternion((0.0, 0.0, bin2float('0.707000', 'f4fd343f'), bin2float('0.707000', 'f4fd343f'))), Vector((-1.0, 0.0, 0.0))), Vector((0.0, -1.0, 0.0)))
        self.ensureRotationEqual("(<1.0, 2.0, 3.0, 4.0> * <5.0, 6.0, 7.0, 8.0>)", (rmul(Quaternion((5.0, 6.0, 7.0, 8.0)), Quaternion((1.0, 2.0, 3.0, 4.0)))), Quaternion((32.0, 32.0, 56.0, -6.0)))
        self.ensureIntegerEqual("(2 / 2)", (rdiv(2, 2)), 1)
        self.ensureFloatEqual("(2.2 / 2)", (rdiv(2.0, bin2float('2.200000', 'cdcc0c40'))), bin2float('1.100000', 'cdcc8c3f'))
        self.ensureFloatEqual("(3 / 1.5)", (rdiv(bin2float('1.500000', '0000c03f'), 3.0)), 2.0)
        self.ensureFloatEqual("(2.2 / 2.0)", (rdiv(2.0, bin2float('2.200000', 'cdcc0c40'))), bin2float('1.100000', 'cdcc8c3f'))
        self.ensureVectorEqual("(<1.0, 2.0, 3.0> / 2)", (rdiv(2.0, Vector((1.0, 2.0, 3.0)))), Vector((bin2float('0.500000', '0000003f'), 1.0, bin2float('1.500000', '0000c03f'))))
        self.ensureVectorEqual("(<3.0, 6.0, 9.0> / 1.5)", (rdiv(bin2float('1.500000', '0000c03f'), Vector((3.0, 6.0, 9.0)))), Vector((2.0, 4.0, 6.0)))
        self.ensureVectorEqual("<-1,0,0> / <0, 0, 0.707, 0.707>", rdiv(Quaternion((0.0, 0.0, bin2float('0.707000', 'f4fd343f'), bin2float('0.707000', 'f4fd343f'))), Vector((-1.0, 0.0, 0.0))), Vector((0.0, 1.0, 0.0)))
        self.ensureRotationEqual("(<1.0, 2.0, 3.0, 4.0> / <5.0, 6.0, 7.0, 8.0>)", (rdiv(Quaternion((5.0, 6.0, 7.0, 8.0)), Quaternion((1.0, 2.0, 3.0, 4.0)))), Quaternion((-16.0, 0.0, -8.0, 70.0)))
        self.ensureIntegerEqual("(3 % 1)", (rmod(1, 3)), 0)
        self.ensureVectorEqual("(<1.0, 2.0, 3.0> % <4.0, 5.0, 6.0>)", (rmod(Vector((4.0, 5.0, 6.0)), Vector((1.0, 2.0, 3.0)))), Vector((-3.0, 6.0, -3.0)))
        _i = 1
        self.ensureIntegerEqual("i = 1;", _i, 1)
        _i = 1
        _i = radd(1, _i)
        self.ensureIntegerEqual("i = 1; i += 1;", _i, 2)
        _i = 1
        _i = rsub(1, _i)
        self.ensureIntegerEqual("i = 1; i -= 1;", _i, 0)
        _i = 2
        _i = rmul(2, _i)
        self.ensureIntegerEqual("i = 2; i *= 2;", _i, 4)
        _i = 1
        (_i := typecast(rmul(bin2float('0.500000', '0000003f'), _i), int))
        self.ensureIntegerEqual("i = 1; i *= 0.5;", _i, 0)
        _i = 2
        _i = rdiv(2, _i)
        self.ensureIntegerEqual("i = 2; i /= 2;", _i, 1)
        _i = rdiv(-1, -2147483648)
        self.ensureIntegerEqual("i = 0x80000000 / -1;", _i, -2147483648)
        _i = 3
        _i = rmod(1, _i)
        self.ensureIntegerEqual("i = 3; i %= 1;", _i, 0)
        _i = rmod(-1, -2147483648)
        self.ensureIntegerEqual("i = 0x80000000 % -1;", _i, 0)
        _i = 1
        self.ensureIntegerEqual("postinc", rbooland((req(1, postincr(locals(), "_i"))), (req(2, _i))), 1)
        _i = 1
        self.ensureIntegerEqual("preinc", rbooland((req(2, preincr(locals(), "_i"))), (req(2, _i))), 1)
        _i = 2
        self.ensureIntegerEqual("postdec", rbooland((req(2, postdecr(locals(), "_i"))), (req(1, _i))), 1)
        _i = 2
        self.ensureIntegerEqual("predec1", rbooland((req(1, predecr(locals(), "_i"))), (req(1, _i))), 1)
        _i = 2
        _i -= 1
        self.ensureIntegerEqual("predec2", _i, 1)
        self.ensureFloatEqual("((float)2)", (2.0), 2.0)
        self.ensureStringEqual("((string)2)", (typecast(2, str)), "2")
        self.ensureIntegerEqual("((integer) 1.5)", (typecast(bin2float('1.500000', '0000c03f'), int)), 1)
        self.ensureStringEqual("((string) 1.5)", (typecast(bin2float('1.500000', '0000c03f'), str)), "1.500000")
        self.ensureIntegerEqual("((integer) \"0xF\")", (typecast("0xF", int)), 15)
        self.ensureIntegerEqual("((integer) \"2\")", (typecast("2", int)), 2)
        self.ensureFloatEqual("((float) \"1.5\")", (typecast("1.5", float)), bin2float('1.500000', '0000c03f'))
        self.ensureVectorEqual("((vector) \"<1,2,3>\")", (typecast("<1,2,3>", Vector)), Vector((1.0, 2.0, 3.0)))
        self.ensureRotationEqual("((quaternion) \"<1,2,3,4>\")", (typecast("<1,2,3,4>", Quaternion)), Quaternion((1.0, 2.0, 3.0, 4.0)))
        self.ensureStringEqual("((string) <1,2,3>)", (typecast(Vector((1.0, 2.0, 3.0)), str)), "<1.00000, 2.00000, 3.00000>")
        self.ensureStringEqual("((string) <1,2,3,4>)", (typecast(Quaternion((1.0, 2.0, 3.0, 4.0)), str)), "<1.00000, 2.00000, 3.00000, 4.00000>")
        self.ensureStringEqual("((string) [1,2.5,<1,2,3>])", (typecast([1, bin2float('2.500000', '00002040'), Vector((1.0, 2.0, 3.0))], str)), "12.500000<1.000000, 2.000000, 3.000000>")
        _i = 0
        while cond(rless(10, _i)):
            _i += 1
        self.ensureIntegerEqual("i = 0; while(i < 10) ++i", _i, 10)
        _i = 0
        while True == True:
            _i += 1
            if not cond(rless(10, _i)):
                break
        self.ensureIntegerEqual("i = 0; do {++i;} while(i < 10);", _i, 10)
        _i = 0
        while True == True:
            if not cond(rless(10, _i)):
                break
            pass
            _i += 1
        self.ensureIntegerEqual("for(i = 0; i < 10; ++i);", _i, 10)
        _i = 1
        goto ._SkipAssign
        self.builtin_funcs.llSetText("Error", Vector((1.0, 0.0, 0.0)), 1.0)
        _i = 2
        label ._SkipAssign
        self.ensureIntegerEqual("assignjump", _i, 1)
        self.ensureIntegerEqual("testReturn()", self.testReturn(), 1)
        self.ensureFloatEqual("testReturnFloat()", self.testReturnFloat(), 1.0)
        self.ensureStringEqual("testReturnString()", self.testReturnString(), "Test string")
        self.ensureVectorEqual("testReturnVector()", self.testReturnVector(), Vector((1.0, 2.0, 3.0)))
        self.ensureRotationEqual("testReturnRotation()", self.testReturnRotation(), Quaternion((1.0, 2.0, 3.0, 4.0)))
        self.ensureListEqual("testReturnList()", self.testReturnList(), [1, 2, 3])
        self.ensureVectorEqual("testReturnVectorNested()", self.testReturnVectorNested(), Vector((1.0, 2.0, 3.0)))
        self.ensureVectorEqual("libveccall", self.testReturnVectorWithLibraryCall(), Vector((1.0, 2.0, 3.0)))
        self.ensureRotationEqual("librotcall", self.testReturnRotationWithLibraryCall(), Quaternion((1.0, 2.0, 3.0, 4.0)))
        self.ensureIntegerEqual("testParameters(1)", self.testParameters(1), 2)
        _i = 1
        self.ensureIntegerEqual("i = 1; testParameters(i)", self.testParameters(_i), 2)
        self.ensureIntegerEqual("testRecursion(10)", self.testRecursion(10), 0)
        self.ensureIntegerEqual("gInteger", self.gInteger, 5)
        self.ensureFloatEqual("gFloat", self.gFloat, bin2float('1.500000', '0000c03f'))
        self.ensureStringEqual("gString", self.gString, "foo")
        self.ensureVectorEqual("gVector", self.gVector, Vector((1.0, 2.0, 3.0)))
        self.ensureRotationEqual("gRot", self.gRot, Quaternion((1.0, 2.0, 3.0, 4.0)))
        self.ensureListEqual("gList", self.gList, [1, 2, 3])
        self.gInteger = 1
        self.ensureIntegerEqual("gInteger = 1", self.gInteger, 1)
        self.gFloat = bin2float('0.500000', '0000003f')
        self.ensureFloatEqual("gFloat = 0.5", self.gFloat, bin2float('0.500000', '0000003f'))
        self.gString = "bar"
        self.ensureStringEqual("gString = \"bar\"", self.gString, "bar")
        self.gVector = Vector((3.0, 3.0, 3.0))
        self.ensureVectorEqual("gVector = <3,3,3>", self.gVector, Vector((3.0, 3.0, 3.0)))
        self.gRot = Quaternion((3.0, 3.0, 3.0, 3.0))
        self.ensureRotationEqual("gRot = <3,3,3,3>", self.gRot, Quaternion((3.0, 3.0, 3.0, 3.0)))
        self.gList = [4, 5, 6]
        self.ensureListEqual("gList = [4,5,6]", self.gList, [4, 5, 6])
        self.gVector = Vector((3.0, 3.0, 3.0))
        self.ensureVectorEqual("-gVector = <-3,-3,-3>", neg(self.gVector), Vector((-3.0, -3.0, -3.0)))
        self.gRot = Quaternion((3.0, 3.0, 3.0, 3.0))
        self.ensureRotationEqual("-gRot = <-3,-3,-3,-3>", neg(self.gRot), Quaternion((-3.0, -3.0, -3.0, -3.0)))
        _v = Vector((0.0, 0.0, 0.0))
        _v = replace_coord_axis(_v, 0, 3.0)
        self.ensureFloatEqual("v.x", _v[0], 3.0)
        _q = Quaternion((0.0, 0.0, 0.0, 1.0))
        _q = replace_coord_axis(_q, 3, 5.0)
        self.ensureFloatEqual("q.s", _q[3], 5.0)
        self.gVector = replace_coord_axis(self.gVector, 1, bin2float('17.500000', '00008c41'))
        self.ensureFloatEqual("gVector.y = 17.5", self.gVector[1], bin2float('17.500000', '00008c41'))
        self.gRot = replace_coord_axis(self.gRot, 2, bin2float('19.500000', '00009c41'))
        self.ensureFloatEqual("gRot.z = 19.5", self.gRot[2], bin2float('19.500000', '00009c41'))
        _l = typecast(5, list)
        _l2 = typecast(5, list)
        self.ensureListEqual("leq1", _l, _l2)
        self.ensureListEqual("leq2", _l, [5])
        self.ensureListEqual("leq3", [bin2float('1.500000', '0000c03f'), 6, Vector((1.0, 2.0, 3.0)), Quaternion((1.0, 2.0, 3.0, 4.0))], [bin2float('1.500000', '0000c03f'), 6, Vector((1.0, 2.0, 3.0)), Quaternion((1.0, 2.0, 3.0, 4.0))])
        self.ensureIntegerEqual("sesc1", self.builtin_funcs.llStringLength("\\"), 1)
        self.ensureIntegerEqual("sesc2", self.builtin_funcs.llStringLength("    "), 4)
        self.ensureIntegerEqual("sesc3", self.builtin_funcs.llStringLength("\n"), 1)
        self.ensureIntegerEqual("sesc4", self.builtin_funcs.llStringLength("\""), 1)
        self.ensureStringEqual("testExpressionLists([testExpressionLists([]), \"bar\"]) == \"foofoobar\"", self.testExpressionLists([self.testExpressionLists([]), "bar"]), "foofoobar")
        if cond(rboolor(1, rbooland(rbitor(rbitxor(rdiv(self.callOrderFunc(5), self.callOrderFunc(4)), self.callOrderFunc(3)), self.callOrderFunc(2)), rboolor(rmul(self.callOrderFunc(1), self.callOrderFunc(0)), 1)))):
            pass
        self.ensureListEqual("gCallOrder expected order", self.gCallOrder, [5, 4, 3, 2, 1, 0])
        self.ensureIntegerEqual("(gInteger = 5)", (assign(self.__dict__, "gInteger", 5)), 5)
        self.ensureFloatEqual("(gVector.z = 6)", (assign(self.__dict__, "gVector", replace_coord_axis(self.gVector, 2, 6.0))[2]), 6.0)
        self.gVector = Vector((1.0, 2.0, 3.0))
        self.ensureFloatEqual("++gVector.z", preincr(self.__dict__, "gVector", 2), 4.0)
        self.gVector = Vector((1.0, 2.0, 3.0))
        self.ensureFloatEqual("gVector.z++", postincr(self.__dict__, "gVector", 2), 3.0)
        self.ensureFloatEqual("(v.z = 6)", ((_v := replace_coord_axis(_v, 2, 6.0))[2]), 6.0)
        _v = Vector((1.0, 2.0, 3.0))
        self.ensureFloatEqual("++v.z", preincr(locals(), "_v", 2), 4.0)
        _v = Vector((1.0, 2.0, 3.0))
        self.ensureFloatEqual("v.z++", postincr(locals(), "_v", 2), 3.0)

    def runTests(self) -> None:
        self.gInteger = 5
        self.gFloat = bin2float('1.500000', '0000c03f')
        self.gString = "foo"
        self.gVector = Vector((1.0, 2.0, 3.0))
        self.gRot = Quaternion((1.0, 2.0, 3.0, 4.0))
        self.gList = [1, 2, 3]
        self.gTestsPassed = 0
        self.gTestsFailed = 0
        self.gCallOrder = []
        self.tests()
        print("All tests passed")

    def edefaultstate_entry(self) -> None:
        self.runTests()

