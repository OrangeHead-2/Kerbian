"""
Unit tests for kerbiancore.security module.
"""

from kerbiancore.security.securestore import SecureStore, audit_secure_store
from kerbiancore.security.audit import audit_python_file
import os

def test_securestore_set_get(tmp_path=None):
    path = tmp_path / "test.secure" if tmp_path else "test.secure"
    store = SecureStore(str(path))
    store.set("key", "secret")
    assert store.get("key") == "secret"
    audit = audit_secure_store(store)
    assert "key" in audit
    os.remove(str(path))

def test_audit_python_file():
    code_file = "test_audit_pyfile.py"
    with open(code_file, "w") as f:
        f.write("password = 'notsecure'\n")
    issues = audit_python_file(code_file)
    assert isinstance(issues, list)
    os.remove(code_file)

if __name__ == "__main__":
    test_securestore_set_get()
    test_audit_python_file()
    print("Security tests passed.")