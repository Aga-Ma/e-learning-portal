from django.core.management.base import BaseCommand

from courses import models


class Command(BaseCommand):

    def handle(self, *args, **options):
        course1, _ = models.Course.objects.get_or_create(name='Simple Math')
        section, _ = models.Section.objects.get_or_create(title='Addition', number=1, test='simple addition test',
                                                          course=course1)
        question, _ = models.Question.objects.get_or_create(text='2+2', section=section)
        answer, _ = models.Answer.objects.get_or_create(text='4', correct=True, question=question)
        answer2, _ = models.Answer.objects.get_or_create(text='5', correct=False, question=question)
