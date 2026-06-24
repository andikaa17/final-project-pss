from ninja.errors import HttpError


def get_role(user):
    if user.is_superuser:
        return "admin"

    
    if user.groups.filter(name="instructor").exists() or user.groups.filter(name="teacher").exists():
        return "instructor"

    return "student"


def is_admin(user):
    """Check if user is admin, raise error if not"""
    if get_role(user) != "admin":
        raise HttpError(403, "Admin only")
    return True


def is_admin_user(user):
    """Return boolean whether user is admin (without raising error)"""
    return get_role(user) == "admin"


def is_instructor(user):
    if get_role(user) not in ["instructor", "admin"]:
        raise HttpError(403, "Instructor only")
    return True


def is_student(user):
    if not user.is_authenticated:
        raise HttpError(401, "Login required")
    return True


def is_course_owner(user, course):
    if course.teacher_id != user.id and get_role(user) != "admin":
        raise HttpError(403, "Not course owner")
    return True