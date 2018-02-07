from django import forms

from .models import Choice


class VoteForm(forms.Form):
    choice = forms.ModelChoiceField(widget=forms.RadioSelect, queryset=Choice.objects.none(), initial=0)

    def __init__(self, choices, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['choice'].queryset = choices
