from kerbiancore.testing.core import test, TestRunner, discover_tests
from kerbiancore.testing.asserts import Assert

@test
def test_addition():
    Assert.equal(1 + 1, 2)

@test
def test_truth():
    Assert.true(True)

def run():
    runner = TestRunner()
    suite = discover_tests(globals())
    runner.add_suite(suite)
    results = runner.run_all()
    print("Ran", len(results), "tests")
    for result in results:
        print(result.test_func.__name__, "->", "PASS" if result.success else "FAIL")

if __name__ == "__main__":
    run()