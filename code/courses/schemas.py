from ninja import Schema
from typing import Optional, List
from datetime import datetime


class RegisterIn(Schema):
    username: str
    email: str
    password: str
    first_name: Optional[str] = ""
    last_name: Optional[str] = ""
    role: Optional[str] = "student"  


class LoginIn(Schema):
    username: str
    password: str


class RefreshIn(Schema):
    refresh: str


class TokenOut(Schema):
    access: str
    refresh: str


class UserOut(Schema):
    id: int
    username: str
    email: str
    first_name: str
    last_name: str
    role: str


class ProfileUpdateIn(Schema):  
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None


class CourseIn(Schema):
    name: str
    description: Optional[str] = "-"
    price: Optional[int] = 10000


class CoursePatchIn(Schema):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = None


class CourseOut(Schema):
    id: int
    name: str
    description: str
    price: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CourseListOut(Schema):
    count: int
    results: List[CourseOut]


class EnrollmentIn(Schema):
    course_id: int


class ProgressIn(Schema):
    content_id: int


class CourseMemberOut(Schema):
    id: int
    course_id: CourseOut  
    roles: str

    class Config:
        from_attributes = True


class CourseContentCompletionOut(Schema):
    id: int
    member_id: int      
    content_id: int    
    completed: bool
    completed_at: datetime

    class Config:
        from_attributes = True

    @staticmethod
    def resolve_member_id(obj):
        return obj.member_id_id  

    @staticmethod
    def resolve_content_id(obj):
        return obj.content_id_id