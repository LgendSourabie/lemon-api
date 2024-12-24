

def is_user_in_group(request, group_name):
    return request.user.groups.filter(name = group_name).exists()