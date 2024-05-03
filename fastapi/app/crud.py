from models import User, Image
from schemas import UserForm, ImageForm, ImageSave, ImageUpdate
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from tempfile import NamedTemporaryFile
from typing import IO
from fastapi import File, UploadFile, Form


# 유저 생성
def create_user(db: Session, user: UserForm):
    db_user = User(member_email=user.member_email)
    db.add(db_user)
    db.commit()
    return db_user


# 유저 조회
def get_user(db: Session, user_email: str):
    return db.query(User).filter(User.member_email == user_email).first()


# 이미지생성
def create_image(
    db: Session,
    user_id: int,
    url: str,
    keyword: str = Form(...),
    style: str = Form(...),
):

    member_id = user_id
    img_url = url
    keyword_input = keyword
    style_code = style

    db_img = Image(
        member_id=member_id,
        img_url=img_url,
        keyword_input=keyword_input,
        style_code=style_code,
    )
    db.add(db_img)
    db.commit()
    return db_img


def update_image(db: Session, img_id: int):
    db_img = db.query(Image).filter(Image.img_id == img_id).first()

    if not db_img:
        return None

    # 최대 생성 가능 횟수: 2
    if db_img.generating_count >= 2:
        return {
            "message": "you have reached the maxium attempts (2) of generating AI images."
        }
    db_img.generating_count += 1
    db.commit()
    db.refresh(db_img)

    return db_img


# 이미지 조회 by user_id
def get_image_list(db: Session, user_id: int, file_pattern: str):
    img_list = (
        db.query(Image)
        .filter(Image.member_id == user_id, Image.img_url.contains(file_pattern))
        .all()
    )
    return img_list


# 샘플 이미지 최신순 조회
def get_sample_image_list(db: Session, limit_num: int):
    img_sample_list = (
        db.query(Image).order_by(Image.created_at.desc()).limit(limit_num).all()
    )
    return img_sample_list


# 이미지파일 저장
async def save_file(file: IO):
    # s3 업로드: delete = True(기본값)이면
    # 현재 함수가 닫히고 파일도 지워집니다.
    with NamedTemporaryFile("wb", delete=False) as tempfile:
        tempfile.write(file.read())
        return tempfile.name
