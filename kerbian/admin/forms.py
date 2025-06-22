from pydantic import BaseModel, Field
from typing import Type
from fastapi import Request
from fastapi.responses import HTMLResponse

def generate_form(model: Type[BaseModel], action_url: str = ""):
    html = f'<form method="post" action="{action_url}">'
    for name, field in model.__fields__.items():
        field_type = field.outer_type_
        html += f'<label>{name}</label>'
        html += f'<input name="{name}" type="{"number" if field_type==int else "text"}" required={not field.required}><br>'
    html += '<button type="submit">Submit</button></form>'
    return html

# Usage in FastAPI
@app.get("/admin/create/user", response_class=HTMLResponse)
async def create_user_form():
    from kerbian.db.models.user import UserPydanticModel
    return generate_form(UserPydanticModel, "/admin/create/user")