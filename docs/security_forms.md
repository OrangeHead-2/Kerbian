# Security, RBAC, and Auto-Generated Forms

- **JWT/OAuth2:** Secure API and admin with modern authentication.
- **Role-Based Access:** Restrict resources to roles (admin, editor, user, etc).
- **Auto-Generated Forms:** Use Pydantic models to generate HTML forms for your admin interface.

## Example: Secure Admin Route

```python
@app.get("/admin", dependencies=[Depends(require_role(["admin"]))])
async def admin_dashboard():
    ...
```