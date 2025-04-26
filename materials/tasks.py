from django.core.mail import send_mail
from .models import Course, Subscription
from celery import shared_task
from django.utils import timezone
from django.contrib.auth import get_user_model
from datetime import timedelta


@shared_task
def my_periodic_task():
    print("Эта задача выполняется периодически.")


@shared_task
def send_course_update_email(course_id):
    course = Course.objects.get(id=course_id)
    subscriptions = Subscription.objects.filter(course=course)

    # Проверка, прошло ли более 4 часов с момента последнего обновления
    if timezone.now() - course.updated_at > timedelta(hours=4):
        for subscription in subscriptions:
            send_mail(
                subject=f'Обновление курса: {course.title}',
                message=f'Курс "{course.title}" был обновлен. Проверьте новые материалы!',
                from_email='from@example.com',  # Укажите ваш адрес отправителя
                recipient_list=[subscription.user.email],
            )


@shared_task
def deactivate_inactive_users():
    User = get_user_model()
    one_month_ago = timezone.now() - timedelta(days=30)

    # Получаем всех пользователей, которые не заходили более месяца
    inactive_users = User.objects.filter(last_login__lt=one_month_ago, is_active=True)

    # Блокируем их
    inactive_users.update(is_active=False)
    print(f"Заблокировано {inactive_users.count()} пользователей.")
