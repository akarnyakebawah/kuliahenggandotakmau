def get_user_or_none(user):
    if user.is_authenticated():
        return user
    return None
