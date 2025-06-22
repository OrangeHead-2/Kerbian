"""
Unit tests for kerbiancore.profiling module.
"""

from kerbiancore.profiling.core import Profiler
import time

def test_profiler_decorator_and_sections():
    prof = Profiler()

    @prof.profile("fast_func")
    def fast():
        return 42

    @prof.profile("slow_func")
    def slow():
        time.sleep(0.01)
        return "done"

    prof.start_section("block")
    time.sleep(0.005)
    prof.end_section("block")
    assert fast() == 42
    assert slow() == "done"
    # Check results contain the correct keys
    names = [r.name for r in prof.results()]
    assert "fast_func" in names
    assert "slow_func" in names
    assert "block" in names

if __name__ == "__main__":
    test_profiler_decorator_and_sections()
    print("Profiling tests passed.")