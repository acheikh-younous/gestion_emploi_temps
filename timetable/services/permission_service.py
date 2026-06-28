def is_admin(user):
    return user.is_staff or user.is_superuser


def get_user_section(user):
    if is_admin(user):
        return None

    return getattr(user, "managed_section", None)


def user_can_manage_subject(user, subject):
    if is_admin(user):
        return True

    section = get_user_section(user)

    if not section:
        return False

    return subject.level.section_id == section.id


def user_can_manage_course(user, course):
    if is_admin(user):
        return True

    section = get_user_section(user)

    if not section:
        return False

    return course.subject.level.section_id == section.id