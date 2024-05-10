from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

import os
from dotenv import load_dotenv

# (1) 비동기 방식 - Starlette
# (2) 데이터 검증 - pydantic

load_dotenv()

# Retrieve MySQL connection details from environment variables
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_NAME = os.getenv("DATABASE_NAME")

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}?charset=utf8mb4"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
# SessionLocal = sessionmaker(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 비동기용 DB 접속(aiomysql 사용)
# 무거운 작업(I/O)요청(5초짜리)이 먼저와도, 뒤에 가벼운  I/O 작업 요청(1초짜리)이 들어오면 더 빨리 끝나는 녀석이 응답된다
# ASYNC_SQLALCHEMY_DATABASE_URL = "mysql+aiomysql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}?charset=utf8mb4"
# async_engine = create_async_engine(ASYNC_SQLALCHEMY_DATABASE_URL)
# AsyncSessionLocal = sessionmaker(bind=async_engine, class_=AsyncSession)

Base = declarative_base()


def get_db():  # db 세션 객체를 리턴
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# async def get_async_db():
#     async with AsyncSessionLocal() as session:
#         yield session
