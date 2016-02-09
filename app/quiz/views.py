from django.http import Http404
from django.shortcuts import render
from .forms import UserQuizForm
from .models import Quiz, UserQuiz, Answer


def quiz(request, quiz_id=None):
    quiz = Quiz.objects.filter(pk=quiz_id).first()
    if quiz is None:
        raise Http404
    if request.method == 'POST':
        form = UserQuizForm(quiz, request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
        uq = UserQuiz.objects.create(quiz=quiz, name=name)
        for qid, answer in form.get_answers():
            Answer.objects.create(question_id=qid, user_answer=answer, user_quiz=uq)

        num_right, num_questions = grade_results(uq)
        return render(request, 'results.html', {'num_right': num_right, 'num_questions': num_questions})

    elif request.method == 'GET':
        return render(request, 'quiz.html', {'quiz': quiz})


def index(request):
    # Render the list of quizzes that are available.
    qs = Quiz.objects.all()
    return render(request, 'quiz_index.html', {'quiz_list': qs})


def grade_results(user_quiz):
    # Generate the answers for the results for each of the quiz questions.
    user_quiz.refresh_from_db()
    num_right = 0
    for answer in user_quiz.answers.all():
        if answer.user_answer == answer.question.answer:
            num_right += 1
            answer.correct = True
            answer.save()
    total = user_quiz.answers.count()
    user_quiz.num_correct = num_right
    user_quiz.save()
    return num_right, total
