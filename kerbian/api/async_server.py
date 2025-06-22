from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from strawberry.fastapi import GraphQLRouter
from kerbian.db.models.user import User
from kerbian.graphql.autoschema import create_graphql_app

app = FastAPI()
models = [User]  # Add more models as needed
graphql_app = create_graphql_app(models)
app.include_router(graphql_app, prefix="/graphql")

# Example: async endpoint
@app.get("/healthz")
async def healthz():
    return {"status": "ok"}