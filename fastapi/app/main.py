from fastapi import FastAPI, Request, Depends, Response, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse
from pathlib import Path
from starlette.templating import Jinja2Templates
from schemas import UserForm
from sqlalchemy.orm import Session
from database import get_db
import re
import crud
import datetime

BASE_DIR = Path(__file__).resolve().parent

# templates 경로 지정
# print(str(Path(BASE_DIR, "templates")))
templates = Jinja2Templates(directory=str(Path(BASE_DIR, "templates")))

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", context={"request": request})


@app.get("/verify", response_class=HTMLResponse)
def verify(request: Request):
    return templates.TemplateResponse("verification.html", context={"request": request})


@app.post("/verify")
def verify(
    response: Response,
    db: Session = Depends(get_db),
    user: UserForm = Depends(UserForm.as_form),
):

    pattern = re.compile(r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?")

    if not re.fullmatch(pattern, user.member_email):
        return {"msg": f"{user.member_email} is not a valid email address."}

    db_user = crud.get_user(db, user)

    if db_user:  # 생성하고자 하는 admin이 이미 존재하면 set cookie

        # set cookie
        response.set_cookie(
            key="email",
            value=db_user.member_email,
            expires=datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=1),
            httponly=False,
            secure=False,
            domain=None,
            path="/",
        )
    else:
        # user date: db에 저장
        crud.create_user(db, user)
        # set cookie
        response.set_cookie(
            key="email",
            value=user.member_email,
            expires=datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=1),
            httponly=False,
            secure=False,
            domain=None,
            path="/",
        )
    print({"message": "Cookie is set on the browser"})

    return RedirectResponse(url="/", status_code=302)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True, log_level="info")
