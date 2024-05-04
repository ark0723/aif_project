from models import User, Image
from schemas import UserForm
from sqlalchemy.orm import Session
from fastapi import Form


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

    db_img = Image(
        member_id=user_id,
        img_url=url,
        keyword_input=keyword,
        style_code=style,
    )
    db.add(db_img)
    db.commit()
    return db_img


# 이미지생성
def create_tshirt_image(
    db: Session,
    user_id: int,
    url: str,
):

    db_img = Image(
        member_id=user_id,
        img_url=url,
    )
    db.add(db_img)
    db.commit()
    return db_img


# 이미지 생성시 count 1씩 증가, max = 2
def update_user_count(db: Session, user_id: int):
    db_user = db.query(User).filter(User.member_id == user_id).first()

    if not db_user:
        return

    # 최대 생성 가능 횟수: 2
    if db_user.img_generate_count >= 2:
        return

    db_user.img_generate_count += 1
    db.commit()
    db.refresh(db_user)

    return db_user


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
