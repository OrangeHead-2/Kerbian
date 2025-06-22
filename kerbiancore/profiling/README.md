# KerbianCore Profiling Module

Profile and optimize Python code performance.

## Features

- Decorator-based function profiling
- Manual code section profiling
- Aggregated results with timing info

## Example

```python
from kerbiancore.profiling.core import Profiler

prof = Profiler()

@prof.profile("fast_func")
def foo(): ...

prof.start_section("block")
# ... code ...
prof.end_section("block")

for r in prof.results():
    print(r.name, r.elapsed)
```

---