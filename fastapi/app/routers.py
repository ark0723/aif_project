from fastapi import (
    APIRouter,
    Depends,
    Form,
    Response,
    Request,
    File,
    UploadFile,
    HTTPException,
    status,
    Cookie,
)
from typing import Annotated
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from database import get_db
import uuid
import os

from pathlib import Path
from starlette.templating import Jinja2Templates
from generator import generate_ai_image
from s3_utils import upload_byte_to_s3
import crud

BASE_DIR = Path(__file__).resolve().parent
print(BASE_DIR)

# templates 경로 지정
templates = Jinja2Templates(directory=str(Path(BASE_DIR, "templates")))

# router setting
img_router = APIRouter(prefix="/image")


@img_router.post("/create")
def get_ai_images(
    email: Annotated[str | None, Cookie()] = None,
    keyword: str = Form(...),
    style: str = Form(...),
    db: Session = Depends(get_db),
):
    # 1. user email을 쿠키로부터 받아온후, email을 이용해서 user id를 db에서 받아온다
    if not email:
        return HTTPException(
            status_code=400, detail="Youre email info does not exists in cookie!"
        )

    user = crud.get_user(db=db, user_email=email)
    if user:
        # 2. 이미지를 생성한다
        img_urls = generate_ai_image(keyword, style)

        # 3. 이미지 info를 db에 insert한다
        for url in img_urls:
            crud.create_image(db, user.member_id, url, keyword, style)

    return {"img_list": img_urls}
