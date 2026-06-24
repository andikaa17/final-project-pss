import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.models import User, Group
from ninja import Router  
from ninja.security import HttpBearer
from ninja.errors import HttpError
from .schemas import RegisterIn, LoginIn, RefreshIn, ProfileUpdateIn


ALGORITHM = "HS256"
router = Router()


def create_token(user, token_type="access"):
    minutes = 60 if token_type == "access" else 60 * 24 * 7
    payload = {
        "user_id": user.id,
        "type": token_type,
        "exp": datetime.utcnow() + timedelta(minutes=minutes),
        "iat": datetime.utcnow(),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token):
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HttpError(401, "Token expired")
    except jwt.InvalidTokenError:
        raise HttpError(401, "Invalid token")


class JWTAuth(HttpBearer):
    def authenticate(self, request, token):
        payload = decode_token(token)
        if payload.get("type") != "access":
            raise HttpError(401, "Invalid token type")
        try:
            return User.objects.get(id=payload["user_id"])
        except User.DoesNotExist:
            raise HttpError(401, "User not found")


auth = JWTAuth()


def get_role(user):
    if user.is_superuser:
        return "admin"
    if user.groups.filter(name="instructor").exists():
        return "instructor"
    return "student"


@router.post('/register')
def register(request, payload: RegisterIn):
    if User.objects.filter(username=payload.username).exists():
        raise HttpError(400, "Username already exists")
    if User.objects.filter(email=payload.email).exists():
        raise HttpError(400, "Email already exists")
    
    user = User.objects.create_user(
        username=payload.username,
        email=payload.email,
        password=payload.password,
        first_name=payload.first_name or '',
        last_name=payload.last_name or ''
    )
    
    role = payload.role or "student"
    if role == "instructor":
        group, _ = Group.objects.get_or_create(name='instructor')
    else:
        group, _ = Group.objects.get_or_create(name='student')
    user.groups.add(group)
    
    access = create_token(user, "access")
    refresh = create_token(user, "refresh")
    
    return {
        "access": access,
        "refresh": refresh,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": role
        }
    }


@router.post('/login')
def login(request, payload: LoginIn):
    from django.contrib.auth import authenticate
    user = authenticate(username=payload.username, password=payload.password)
    if not user:
        raise HttpError(401, "Invalid credentials")
    return {
        "access": create_token(user, "access"),
        "refresh": create_token(user, "refresh")
    }


@router.post('/refresh')
def refresh_token(request, payload: RefreshIn):
    try:
        data = jwt.decode(payload.refresh, settings.SECRET_KEY, algorithms=[ALGORITHM])
        if data.get("type") != "refresh":
            raise HttpError(401, "Invalid token type")
        user = User.objects.get(id=data["user_id"])
        return {"access": create_token(user, "access")}
    except jwt.ExpiredSignatureError:
        raise HttpError(401, "Refresh token expired")
    except jwt.InvalidTokenError:
        raise HttpError(401, "Invalid refresh token")
    except User.DoesNotExist:
        raise HttpError(401, "User not found")


@router.get('/me', auth=auth)
def get_me(request):
    user = request.auth
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "role": get_role(user)
    }


@router.put('/me', auth=auth)
def update_me(request, payload: ProfileUpdateIn):
    user = request.auth
    if payload.first_name is not None:
        user.first_name = payload.first_name
    if payload.last_name is not None:
        user.last_name = payload.last_name
    if payload.email is not None:
        user.email = payload.email
    user.save()
    return {"message": "Profile updated"}