from django.core.management.base import BaseCommand

from courses import models


class Command(BaseCommand):

    def handle(self, *args, **options):
        course1, _ = models.Course.objects.get_or_create(name='Test Course1')
        course2, _ = models.Course.objects.get_or_create(name='Test Course2')

        section, _ = models.Section.objects.get_or_create(title='section title', number=1, test='some test',
                                                          course=course1)
        question, _ = models.Question.objects.get_or_create(text='some very hard question', section=section)
        answer, _ = models.Answer.objects.get_or_create(text='example answer', correct=True, question=question)