from django.shortcuts import render
import pandas
from .forms import TicketForm
# Create your views here.


def index(request):
    context = {
        'query_param_cookie': {},
        'message': '',
        'result': {},
        'form': MailJobForm(),
    }
    if request.method == 'POST':
        form = TicketForm(request.POST)
        context['form'] = form
        if form.is_valid():
            department = form.cleaned_data['department']
            event = form.cleaned_data['event']
        try:
            # do script here
            context['message'] = 'Finished.'
        except:
            context['message'] = 'Failed.'
    return render(request, 'mail_job/index.html', context)
