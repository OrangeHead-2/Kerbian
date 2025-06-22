# Kerbian: Automatic GraphQL, Async APIs, and Secure Admin

- **Automatic GraphQL:** Your ORM models are exposed as a GraphQL API instantly.
- **Async Everywhere:** All APIs and DB operations support async/await.
- **Admin Authentication:** Admin UI uses secure, session-based login.

### Example: Run FastAPI Admin and GraphQL

```bash
pip install fastapi strawberry-graphql[fastapi] aiosqlite uvicorn
uvicorn kerbian.api.async_server:app --reload
```

Visit `/admin` for the admin UI and `/graphql` for the GraphQL playground.