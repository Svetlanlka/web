from random import choice
from itertools import islice
from django.core.management.base import BaseCommand
from app.models import Profile, Tag, Question, Answer, QuestionVote, AnswerVote
from django.contrib.auth.models import User
from faker import Faker
import glob
import random
from random import shuffle, seed, sample, randint
from faker.providers.person.en import Provider
from django.utils import timezone
import datetime

size_values = {
    'small': {
        'questions': 10,
        'answers': 20,
        'tags': 5,
        'users': 5,
        'avotes': 10,
        'qvotes': 10
    },
    'medium': {
        'questions': 100,
        'answers': 200,
        'tags': 50,
        'users': 50,
        'avotes': 100,
        'qvotes': 100
    },
    'large': {
        'questions': 110000,
        'answers': 1100000,
        'tags': 11000,
        'users': 11000,
        'avotes': 1100000,
        'qvotes': 1100000
    }
}

fake = Faker()
datetime.datetime.now(tz=timezone.utc)

class Command(BaseCommand):
    help = "filling db with random data"

    def add_arguments(self, parcer):
        parcer.add_argument("-u", "--users", type=int)
        parcer.add_argument("-t", "--tags", type=int)
        parcer.add_argument("-q", "--questions", type=int)
        parcer.add_argument("-a", "--answers", type=int)
        parcer.add_argument("-qv", "--question_votes", type=int)
        parcer.add_argument("-av", "--answer_votes", type=int)
        parcer.add_argument("-all", "--all", type=str)
        

    def handle(self, *args, **options):
        users_amount = options["users"]
        questions_amount = options["questions"]
        answers_amount = options["answers"]
        tags_amount = options["tags"]
        question_votes_amount = options["question_votes"]
        answer_votes_amount = options["answer_votes"]
        total_amount = options["all"]

        if total_amount:
            total_sizes = size_values[total_amount]
            self.fill_tags(total_sizes['tags'])
            self.fill_users(total_sizes['users'])
            self.fill_questions(total_sizes['questions'])
            self.fill_answers(total_sizes['answers'])
            self.fill_question_votes(total_sizes['qvotes'])
            self.fill_answer_votes(total_sizes['avotes'])
        if tags_amount:
            self.fill_tags(tags_amount)
        if users_amount:
            self.fill_users(users_amount)
        if questions_amount:
            self.fill_questions(questions_amount)
        if answers_amount:
            self.fill_answers(answers_amount)
        if question_votes_amount:
            self.fill_question_votes(question_votes_amount)
        if answer_votes_amount:
            self.fill_answer_votes(answer_votes_amount)
        
    def fill_tags(self, n):
        print("filling ", n, " tags")

        first_names = list(set(Provider.first_names))
        seed(4321)
        shuffle(first_names)

        for i in range(n):
            Tag.objects.create(name=Faker().word() + str(Faker().random.randint(0,100000)))

    def fill_users(self, n):
        print("filling ", n, " users")

        usernames = set()

        file_path_type = "uploads/*.jpg"
        images = glob.glob(file_path_type)
        images = [images[8:] for images in images]
        print(images)

        while len(usernames) != n:
            usernames.add(Faker().user_name() + str(Faker().random.randint(0, 1000000)))

        for name in usernames:
            profile = fake.simple_profile()
            u = User.objects.create(
                is_superuser=False,
                username=name,
                password=Faker().password(),
                email=Faker().email()
            )
            u.set_password(Faker().password())
            u.save(update_fields=['password'])
            new_profile = Profile.objects.get(pk=u.pk)
            new_profile.photo = choice(images)
            new_profile.save(update_fields=['photo'])
        

    def fill_questions(self, n):
        print("filling ", n, " questions")

        users = list(Profile.objects.values_list('id', flat=True))
        tags = list(Tag.objects.values_list('id', flat=True))
        for i in range(n):
            question = Question.objects.create(
                user_id=choice(users),
                title=Faker().sentence()[:200],
                text=". ".join(
                    Faker().sentences(
                        Faker().random_int(min=2, max=5)
                    )
                ),
                date=Faker().date_between("-100d", "today"),
            )

            tags_set = sample(tags, k=randint(1, 5))
            tags_update = Tag.objects.filter(pk=i)
            for i in tags_update:
                i.set_rating()
                i.save(update_fields=['rating'])
            question.tags.set(tags_set)


    def fill_answers(self, n):
        print("filling ", n, " answers")

        questions = list(Question.objects.values_list("id", flat=True))
        users = list(User.objects.values_list("id", flat=True))
        answers = []

        for i in range(n):
            answer = Answer(
                question_id=choice(questions),
                user_id=choice(users),
                text=". ".join(Faker().sentences(Faker().random_int(min=2, max=5))),
                date=Faker().date_between("-100d", "today"),
            )
            if (Faker().random_int(min=0, max=5) == 0):
                answer.marked_correct = True
            answers.append(answer)

        batch_size = 100
        n_batches = len(answers)
        if len(answers) % batch_size != 0:
            n_batches += 1
        for i in range(n_batches):
            start = batch_size * i
            end = batch_size * (i + 1)
            Answer.objects.bulk_create(answers[start:end], batch_size)

    def fill_question_votes(self, n):
        print("filling ", n, " question votes")

        questions = list(Question.objects.values_list("id", flat=True))
        users = list(User.objects.values_list("id", flat=True))
        votes = []

        for i in range(n):
            vote = QuestionVote(
                question_id=choice(questions),
                user_id=choice(users),
                vote=Faker().random.randint(-1, 1)
            )
            votes.append(vote)

        batch_size = 100
        n_batches = len(votes)
        if len(votes) % batch_size != 0:
            n_batches += 1
        for i in range(n_batches):
            start = batch_size * i
            end = batch_size * (i + 1)
            QuestionVote.objects.bulk_create(votes[start:end], batch_size)

    def fill_answer_votes(self, n):
        print("filling ", n, " answer votes")

        answers = list(Answer.objects.values_list("id", flat=True))
        users = list(Profile.objects.values_list("id", flat=True))
        votes = []

        for i in range(n):
            ans_id = choice(answers)
            usr_id = choice(users)
            vote = AnswerVote(
                answer_id= ans_id,
                user_id=usr_id,
                vote=Faker().random.randint(-1, 1))
            votes.append(vote)
            # ans = Answer.objects.get_on_id(ans_id)
            # ans.update_rating()
            # ans.save(update_fields=['rating'])

        batch_size = 100
        n_batches = len(votes)
        if len(votes) % batch_size != 0:
            n_batches += 1
        for i in range(n_batches):
            start = batch_size * i
            end = batch_size * (i + 1)
            AnswerVote.objects.bulk_create(votes[start:end], batch_size)

