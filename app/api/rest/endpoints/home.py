from fastapi import APIRouter
from starlette.templating import Jinja2Templates

router = APIRouter()


# @router.get("/")
@router.get("/")
async def read_main():
    return {"msg": "Hello World"}


templates = Jinja2Templates("templates")


# async def homepage(request):
#     template = "index.html"
#     context = {"request": request}
#     return templates.TemplateResponse(template, context)
