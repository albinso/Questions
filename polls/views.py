from django.shortcuts import render, HttpResponse, HttpResponseRedirect, get_object_or_404
from django.template import loader
from django.core.urlresolvers import reverse
from .models import Question, Choice

def index(request):
	latest_question_list = Question.objects.order_by('-pub_date')[:5]
	template = loader.get_template('polls/index.html')
	context = {
		'latest_question_list': latest_question_list
	}
	return HttpResponse(template.render(context, request))

def detail(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	template = loader.get_template('polls/question_details.html')
	context = {
		'question': question
	}
	return HttpResponse(template.render(context, request))

def results(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	return render(request, 'polls/results.html', {'question': question,})

def vote(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	try:
		selected = question.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		return render(request, 'polls/detail.html', {
			'question': question,
			'error_message': "You didn't select a choice",
		})
	else:
		selected.votes += 1
		selected.save()
		return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))