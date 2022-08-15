import string

from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from celery import shared_task

@shared_task
def create_random_user_accounts(total):
    for i in range(total):
        username = 'user_{}'.format(get_random_string(10, string.ascii_letters))
        email = '{}@gmail.com'.format(username)
        password = get_random_string(50)
        User.objects.create_user(username=username, email=email, password=password)
    return '{} random users created with success!'.format(total)

@shared_task
def num_sum(num):
    sum = 0
    for i in  range(num):
        sum += i
    return "{} sum of all numbers till {}".format(sum, num)