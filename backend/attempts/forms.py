from django import forms

class AttemptAnswerForm(forms.Form):
    question_id = forms.IntegerField(widget=forms.HiddenInput())
    selected_answer = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
