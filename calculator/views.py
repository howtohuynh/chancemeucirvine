from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views.generic.edit import CreateView

from .models import Applicant
from .forms import ApplicantForm
# Create your views here.

class index(CreateView):
    template_name = 'calculator/index.html'
    model = Applicant

    def get(self, request):
        form = ApplicantForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ApplicantForm(request.POST or None)
        if form.is_valid():
            form_data = form.cleaned_data
            form.save()

        form_data = form.cleaned_data
        args = {'form': form, 'form_data': form_data, 'apple': apple}
        return render(request, self.template_name, args)

def apple():
    return