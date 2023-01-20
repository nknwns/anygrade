from .models import *
from faker import Faker

fake = Faker('ru_RU')


def seed_users(n):
    for i in range(n):
        User.objects.create(
            username=fake.user_name(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            password=fake.password(length=20),
            email=fake.email()
        )


def seed_categories(n):
    users = User.objects.all().values_list('id', flat=True)

    for i in range(n):
        Category.objects.create(
            title=fake.word(),
            author_id=fake.random_element(users)
        )


def seed_questions(n):
    users = User.objects.all().values_list('id', flat=True)
    categories = Category.objects.all().values_list('id', flat=True)

    for i in range(n):
        Question.objects.create(
            title=fake.text(128),
            author_id=fake.random_element(users),
            category_id=fake.random_element(categories)
        )


def seed_reviews(n):
    users = list(User.objects.all().values_list('id', flat=True))
    questions = list(Question.objects.all().values_list('id', flat=True))

    for i in range(n):
        review = Review.objects.create(
            title=fake.text(32),
            description=fake.text(256),
            start_time=fake.date_time(),
            end_time=fake.date_time(),
            author_id=fake.random_element(users),
            subject_id=fake.random_element(users)
        )

        review.participant.set(fake.random_elements(users, length=fake.random_int(5, len(users)), unique=True))
        review.question.set(fake.random_elements(questions, length=fake.random_int(5, len(questions)), unique=True))


def seed_results():
    reviews = list(map(
        lambda el: {'id': el.id, 'participants': list(el.participant.all().values_list('id', flat=True))},
        Review.objects.all()
    ))

    for review in reviews:
        participants_list = fake.random_elements(review['participants'],
                                                 length=fake.random_int(0, len(review['participants'])), unique=True)
        current_review = Review.objects.get(pk=review['id'])
        for element in participants_list:
            Result.objects.create(
                author_id=element,
                data=fake.lexify(text='?' * current_review.question.count(), letters='01234'),
                subject_id=review['id']
            )


def seed_templates(n):
    users = list(User.objects.all().values_list('id', flat=True))
    questions = list(Question.objects.all().values_list('id', flat=True))

    for i in range(n):
        template = Template.objects.create(
            title=fake.text(32),
            description=fake.text(256),
            author_id=fake.random_element(users)
        )

        template.question.set(fake.random_elements(questions, length=fake.random_int(1, len(questions)), unique=True))
