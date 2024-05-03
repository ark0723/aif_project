from pydantic import BaseModel
from fastapi import Form


class EmailForm(BaseModel):
    email_address: str

    @classmethod
    def as_form(cls, email_address: str = Form(...)):

        return cls(email_address=email_address)


class UserForm(BaseModel):
    member_email: str

    @classmethod
    def as_form(cls, member_email: str = Form(...)):
        return cls(member_email=member_email)


class ImageForm(BaseModel):
    keyword_input: str
    style_code: str

    @classmethod
    def as_form(cls, keyword_input: str = Form(...), style_code: str = Form(...)):
        return cls(keyword_input=keyword_input, style_code=style_code)


class ImageSave(BaseModel):
    member_id: int
    img_url: str
    keyword_input: str
    style_code: str


class ImageUpdate(BaseModel):
    generating_count: int
