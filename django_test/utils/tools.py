import random
import string


def get_current_user_id(request):
    return request.user.userprofile.id if request.user and request.user.userprofile else 0


def get_random_str(num):
    return ''.join(random.sample(string.ascii_letters + string.digits, num))
