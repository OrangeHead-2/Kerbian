import json

class TestReport:
    def __init__(self, results):
        self.results = results

    def summary(self):
        total = len(self.results)
        passed = sum(1 for r in self.results if r.passed)
        failed = total - passed
        return {
            "total": total,
            "passed": passed,
            "failed": failed
        }

    def export_json(self, path=None):
        data = [r.as_dict() for r in self.results]
        out = json.dumps(data, indent=2)
        if path:
            with open(path, "w") as f:
                f.write(out)
        return out

    def print_failures(self):
        fails = [r for r in self.results if not r.passed]
        for r in fails:
            print(f"FAILED: {r.test_name}\n  Error: {r.error}\n  Traceback:\n{r.traceback_str}")

    def print_summary(self):
        s = self.summary()
        print(f"Total: {s['total']}, Passed: {s['passed']}, Failed: {s['failed']}")