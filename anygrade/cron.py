from django.core.mail import send_mail

from service.models import Review
import datetime


def review_scheduled_job():
    reviews = Review.objects.filter(end_time__contains=datetime.date.today() + datetime.timedelta(days=1))

    for review in reviews:

        subject = f'Опрос #. {review.pk}. [{review.title}]'

        message = f'Уважаемый пользователь,\n\nНапоминаем, что уже завтра заканчивается опрос оценки вашего коллеги.\
                            Пожалуйста, успейте выполнить опрос!.'

        emails = [participant.email for participant in review.participant.all()]

        send_mail(subject, message, 'admin@anygrade.com', emails)
