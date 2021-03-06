from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

from contests.models import Contest, Tag


class Quiz(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=25, unique=True)
    description = models.CharField(max_length=256, blank=True)
    tags = models.ManyToManyField(Tag)
    score = models.IntegerField(editable=False, default=0)
    # make score dependent on problems contained or some final normalized score

    DIFF_CHOICES = (('n00b', 'n00b'), ('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard'), ('1337', '1337'))
    difficulty = models.CharField(max_length=10, choices=DIFF_CHOICES)
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE, null=True, blank=True)
    creators = models.ManyToManyField(User)

    hidden = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)


class Question(models.Model):
    question = models.CharField(max_length=256)
    slug = models.SlugField(max_length=16, unique=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    hints = models.CharField(max_length=256, blank=True)

    tags = models.ManyToManyField(Tag)
    score = models.IntegerField()

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.slug)


class SimpleQuestion(Question):
    answer = models.CharField(max_length=64)
    is_mcq = models.BooleanField(default=False, editable=False)


class MCQ(Question):
    choices = models.CharField(choices=[], max_length=256)
    answer = models.IntegerField()
    is_mcq = models.BooleanField(default=True, editable=False)

    @classmethod
    def create(cls, question, slug, hints, choices, correct, score, quiz):
        CHOICES = [(index, item) for index, item in enumerate(choices)]
        mcq = cls(question=question, slug=slug, hints=hints, choices=CHOICES, correct=correct, answer=answer, score=score, quiz=quiz)
        return mcq


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'question', 'score', 'created', 'modified')
    search_fields = ('quiz', 'question')
    list_filter = ('tags', 'score', 'modified', 'created')
    ordering = ['score', 'modified', 'created']


class SimpleQuestionAdmin(QuestionAdmin):
    pass


class MCQAdmin(QuestionAdmin):
    pass


class QuizAdmin(admin.ModelAdmin):
    list_display = ('name', 'score', 'contest', 'hidden', 'created', 'modified')
    search_fields = ('name', 'description', 'contest')
    raw_id_fields = ('creators',)
    list_filter = ('tags', 'score', 'modified', 'created', 'creators')
    ordering = ['name', 'score', 'creators', 'modified', 'created']
