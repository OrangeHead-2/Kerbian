import os
import inspect

def check_file_permissions(path, required="600"):
    if not os.path.exists(path):
        return False, "File does not exist"
    perms = oct(os.stat(path).st_mode)[-3:]
    return perms == required, f"Permissions: {perms}"

def audit_python_file(file_path):
    issues = []
    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()
        if "eval(" in code:
            issues.append("Use of eval() detected.")
        if "exec(" in code:
            issues.append("Use of exec() detected.")
        if "pickle" in code:
            issues.append("Use of pickle detected (unsafe for untrusted data).")
        if "os.system(" in code or "subprocess." in code:
            issues.append("Use of shell/system calls detected.")
    return issues

def audit_module(module):
    issues = []
    for name, obj in inspect.getmembers(module):
        if inspect.isfunction(obj):
            source = inspect.getsource(obj)
            if "eval(" in source:
                issues.append(f"{name}: Use of eval() detected.")
            if "exec(" in source:
                issues.append(f"{name}: Use of exec() detected.")
            if "pickle" in source:
                issues.append(f"{name}: Use of pickle detected.")
    return issues