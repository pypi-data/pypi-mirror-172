from calculations import Calculator
cal=Calculator()


def test_add():
    total = cal.add(2,3)
    assert total==5

def test_subtract():
    result = cal.subtract(5,2)
    assert result==3

def test_multiply():
    mul = cal.multiply(2,3)
    assert mul==6

def test_division():
    div = cal.division(10,2)
    assert div==5

def test_nthroot():
    nth = cal.nthroot(22,2)
    assert nth==4.69041575982343

def test_reset_memory():
    rest=cal.reset_memory()
    assert rest ==0