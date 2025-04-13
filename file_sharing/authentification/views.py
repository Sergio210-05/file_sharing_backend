import json
import logging

from django.contrib.auth import authenticate, login, logout
from django.contrib.sessions.models import Session
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import status

from authentification.models import User
from storage.models import File


logger = logging.getLogger(__name__)


def auth_required(view_func):
    def wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            logger.error('Пользователь не авторизован')
            return JsonResponse({'error': 'Вы не авторизованы'}, status=status.HTTP_401_UNAUTHORIZED)
        return view_func(request, *args, **kwargs)
    return wrapped


def admin_required(view_func):
    def wrapped(request, *args, **kwargs):
        if not request.user.is_superuser:
            logger.error('Недостаточно прав для данного запроса')
            return JsonResponse({'error': 'У Вас недостаточно прав'}, status=status.HTTP_403_FORBIDDEN)
        return view_func(request, *args, **kwargs)
    return wrapped


def get_csrf(request):
    response = JsonResponse({'detail': 'Установка CSRF cookie'})
    response['X-CSRFToken'] = get_token(request)
    response['status'] = status.HTTP_200_OK
    return response


@require_POST
def login_view(request):
    data = json.loads(request.body)
    username = data['username']
    password = data['password']

    if username is None or password is None:
        return JsonResponse({'detail': 'Заполните поля "логин" и "пароль"'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)
    if user is None:
        return JsonResponse({'detail': 'Пользователь не найден в системе'}, status=status.HTTP_404_NOT_FOUND)

    login(request, user)
    return JsonResponse({'detail': 'Авторизация выполнена'}, status=status.HTTP_200_OK)


# Сессия удаляется из БД и session_id на клиенте более недействителен
@auth_required
def logout_view(request):
    logout(request)
    return JsonResponse({'detail': 'Сессия завершена'}, status=status.HTTP_200_OK)


# Получение информации о пользователе
@auth_required
def user_info(request, member_id=None):
    user_id = member_id if member_id else request.user.id
    user = User.objects.get(pk=user_id)
    return JsonResponse({'isAuth': True,
                         'user': {
                             'id': user.id,
                             'login': user.username,
                             'fullName': user.full_name,
                             'email': user.email,
                             'isAdmin': user.is_superuser}
                         },
                        status=status.HTTP_200_OK
                        )


@auth_required
@admin_required
def get_all_users(request):

    def files_count(request, member_id):
        files = File.objects.filter(owner=member_id)
        quantity = len(files)
        sum_size = sum([x.size for x in files])
        return {'amountOfFiles': quantity, 'sizeOfFiles': sum_size}

    users = User.objects.order_by('id')
    users_data = [{'id': x.id,
                   'login': x.username,
                   'fullName': x.full_name,
                   'email': x.email,
                   **files_count(request, x.id),
                   'isAdmin': x.is_superuser} for x in users]

    return JsonResponse({'users': users_data}, status=status.HTTP_200_OK)


@admin_required
def change_admin_status(request, member_id):
    data = json.loads(request.body)
    admin_status = json.loads(data['is_superuser'])
    user = User.objects.get(pk=member_id)
    user.is_superuser = not admin_status
    user.save()
    log_message = f'Пользователю {user.username} ' \
                  f'присвоены права администратора' if user.is_superuser \
        else f'С пользователя {user.username} сняты права администратора'
    logger.info(log_message)
    return JsonResponse({'detail': 'Права пользователя успешно изменены'}, status=status.HTTP_200_OK)


@admin_required
def remove_user(_request, member_id):
    user = User.objects.get(pk=member_id)
    user_name = user.username
    folder = user.folder_path
    user.delete()
    return JsonResponse({'detail': f'Пользователь {user_name} удалён'}, status=status.HTTP_200_OK)


# Узнать авторизован ли пользователь и получить его данные
@ensure_csrf_cookie  # <- Принудительная отправка CSRF cookie
def session_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({'isAuth': False}, status=status.HTTP_200_OK)
    return user_info(request)


# Регистрация нового пользователя
@require_POST
def registration_view(request):
    data = json.loads(request.body)
    username = data['username']
    password = data['password']
    email = data['email']
    full_name = data['fullName']
    new_user = User.objects.create_user(username=username,
                                        password=password,
                                        email=email,
                                        full_name=full_name)
    new_user.save()
    logger.info(f'Создан пользователь с именем {username}')
    return JsonResponse({'detail': f'Пользователь {username} успешно создан'}, status=status.HTTP_201_CREATED)


@auth_required
def change_userdata(request):
    current_user = request.user
    current_user.email = request.GET.get('email', current_user.email)
    user = User.objects.get(pk=current_user.id)
    user.email = f'{current_user}@mail.ru'
    user.save()
    return JsonResponse({'detail': 'Запрос прошёл'})


# Удаление сессий из БД
@auth_required
def remove_user_sessions(request):
    user = request.user
    sessions = Session.objects.filter(user=user)
    sessions.delete()
    return JsonResponse({'detail': 'Сессии успешно завершены'})
