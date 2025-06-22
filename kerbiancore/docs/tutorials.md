````markdown
# KerbianCore Real Guides & Tutorials

## 📦 End-to-End App Build, Test, and Release

### 1. Write and Test Your Code

```python
from kerbiancore.testing.core import test, TestRunner, discover_tests
from kerbiancore.testing.asserts import Assert

@test
def test_math():
    Assert.equal(2 + 2, 4)

suite = discover_tests(globals())
runner = TestRunner()
runner.add_suite(suite)
results = runner.run_all()