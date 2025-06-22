"""
Unit tests for kerbiancore.testing module.
"""

from kerbiancore.testing.core import test, TestRunner, discover_tests
from kerbiancore.testing.asserts import Assert

@test
def test_assert_equal():
    Assert.equal(5, 5)
    Assert.equal("abc", "abc")
    try:
        Assert.equal(1, 2)
        assert False, "Expected AssertionError"
    except AssertionError:
        pass

@test
def test_assert_true():
    Assert.true(True)
    try:
        Assert.true(False)
        assert False, "Expected AssertionError"
    except AssertionError:
        pass

def run_tests():
    suite = discover_tests(globals())
    runner = TestRunner()
    runner.add_suite(suite)
    results = runner.run_all()
    for result in results:
        print(result.test_func.__name__, "->", "PASS" if result.success else "FAIL")
    assert all(r.success for r in results), "Some tests failed"

if __name__ == "__main__":
    run_tests()