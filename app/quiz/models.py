from django.db import models

# Question Models

BOOLEAN_CHOICES = ((True, "True"), (False, "False"))


class Question(models.Model):
    question = models.CharField(max_length=1024, blank=False, null=False)
    answer = models.BooleanField(null=False, choices=BOOLEAN_CHOICES)

    def __str__(self):
        return "Question: {}: {}".format(self.question, self.answer)


class QuizQuestion(models.Model):
    question = models.ForeignKey(Question)
    quiz = models.ForeignKey("quiz.Quiz")


class Quiz(models.Model):
    content = models.CharField(max_length=16384)
    questions = models.ManyToManyField(Question, through="quiz.QuizQuestion")
    name = models.CharField(max_length=256)

    def __str__(self):
        return "Quiz {} {}".format(self.id, self.name)

    class Meta:
        verbose_name_plural = "Quizzes"


# Answer Models

class UserQuiz(models.Model):
    quiz = models.ForeignKey(Quiz)
    name = models.CharField(max_length=256)
    num_correct = models.IntegerField(null=True)

    def __str__(self):
        return "Results: {} for Quiz {}>".format(self.name, self.quiz.name)

    class Meta:
        verbose_name_plural = "UserQuizzes"


class Answer(models.Model):
    user_quiz = models.ForeignKey(UserQuiz, related_name="answers")
    question = models.ForeignKey(Question, related_name="+")
    user_answer = models.BooleanField(choices=BOOLEAN_CHOICES)
    correct = models.BooleanField(null=False, default=False)

    def __str__(self):
        correct = "correct"
        if not self.correct:
            correct = "incorrect"
        return "<{}: {}>".format(self.question.question, correct)
