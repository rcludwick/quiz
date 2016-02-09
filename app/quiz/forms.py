from django import forms
from .models import BOOLEAN_CHOICES


class UserQuizForm(forms.Form):
    name = forms.CharField(max_length=256)

    def __init__(self, quiz, *args, **kwargs):
        super(UserQuizForm, self).__init__(*args, **kwargs)
        for q in quiz.questions.all():
            label = "qid_{}".format(q.id)
            self.fields[label] = forms.ChoiceField(label=id, choices=BOOLEAN_CHOICES)

    def get_answers(self):
        for k, v in self.cleaned_data.items():
            if k.startswith('qid_'):
                qid = int(k.split('_')[1])
                yield qid, v
