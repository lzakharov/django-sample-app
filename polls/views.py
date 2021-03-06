from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Choice, Question
from .forms import VoteForm


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


def detail(request, question_id):
    question = get_object_or_404(Question, pub_date__lte=timezone.now(), pk=question_id)
    choices = question.choice_set.all()
    form = VoteForm(choices)
    return render(request, 'polls/detail.html', {'question': question, 'form': form})


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'
    context_object_name = 'question'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    choices = question.choice_set.all()

    if request.method == 'POST':
        form = VoteForm(choices, request.POST)
        print(form.is_valid())
        if form.is_valid():
            selected_choice = form.cleaned_data['choice']
            selected_choice.votes += 1
            selected_choice.save()
            return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
    else:
        form = VoteForm(choices)

    return render(request, 'polls/detail.html', {'question': question, 'form': form})
