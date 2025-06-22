import traceback
import time
import inspect

class TestResult:
    def __init__(self, test_name, passed, duration, error=None, traceback_str=None):
        self.test_name = test_name
        self.passed = passed
        self.duration = duration
        self.error = error
        self.traceback_str = traceback_str

    def as_dict(self):
        return {
            "test_name": self.test_name,
            "passed": self.passed,
            "duration": self.duration,
            "error": self.error,
            "traceback": self.traceback_str
        }

class TestSuite:
    def __init__(self, name=None):
        self.tests = []
        self.name = name

    def add_test(self, func):
        self.tests.append(func)

    def run(self, show_output=True):
        results = []
        for func in self.tests:
            start = time.time()
            try:
                func()
                passed = True
                error = None
                tb = None
            except Exception as e:
                passed = False
                error = str(e)
                tb = traceback.format_exc()
            end = time.time()
            result = TestResult(
                test_name=func.__name__,
                passed=passed,
                duration=end - start,
                error=error,
                traceback_str=tb
            )
            results.append(result)
            if show_output:
                status = "PASS" if passed else "FAIL"
                print(f"[{status}] {func.__name__} ({end-start:.4f}s)")
                if not passed:
                    print(f"  Error: {error}\n  Traceback:\n{tb}")
        return results

class TestRunner:
    def __init__(self):
        self.suites = []

    def add_suite(self, suite):
        self.suites.append(suite)

    def run_all(self, show_output=True):
        all_results = []
        for suite in self.suites:
            if show_output:
                print(f"\n=== Suite: {suite.name or 'unnamed'} ===")
            results = suite.run(show_output=show_output)
            all_results.extend(results)
        passed = sum(1 for r in all_results if r.passed)
        total = len(all_results)
        if show_output:
            print(f"\nTotal: {total}, Passed: {passed}, Failed: {total-passed}")
        return all_results

def test(func):
    func._is_test = True
    return func

def discover_tests(namespace):
    suite = TestSuite(getattr(namespace, "__name__", None))
    if isinstance(namespace, dict):
        items = namespace.items()
    else:
        items = ((name, getattr(namespace, name)) for name in dir(namespace))
    for name, obj in items:
        if callable(obj) and getattr(obj, "_is_test", False):
            suite.add_test(obj)
    return suite