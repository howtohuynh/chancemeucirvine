from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views.generic.edit import CreateView
from calculator.data.functions.csv_to_dict import *

from .models import Applicant
from .forms import ApplicantForm
# Create your views here.

appliedList = ['applied', 'admitted', 'enrolled', 'selectivity_rate', 'yield_rate', 'gpa', 'verbal', 'math',
               'writing']
appliedList2 = ['applied', 'admitted', 'enrolled', 'selectivity_rate', 'yield_rate']
highschoolList = ['admitted']

school = csv_to_dict('calculator/data/csv/school.csv', appliedList)
major = csv_to_dict('calculator/data/csv/major.csv', appliedList)
gender = csv_to_dict('calculator/data/csv/gender.csv', appliedList)
high_school = csv_to_dict('calculator/data/csv/high_school.csv', highschoolList)
residency = csv_to_dict('calculator/data/csv/residency.csv', appliedList[:5])
ethnicity = csv_to_dict('calculator/data/csv/ethnicity.csv', appliedList)
school_gender = csv_to_dict('calculator/data/csv/school_gender.csv', appliedList)
school_ethnicity = csv_to_dict('calculator/data/csv/school_ethnicity.csv', appliedList)
uc_gpa = csv_to_dict('calculator/data/csv/gpa.csv', appliedList2)
sat_verbal = csv_to_dict('calculator/data/csv/verbal.csv', appliedList2)
sat_math = csv_to_dict('calculator/data/csv/math.csv', appliedList2)
sat_writing = csv_to_dict('calculator/data/csv/writing.csv', appliedList2)

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
        td = table_data(form_data)
        cr = chance_range(td)
        hs = highSchool(form_data)
        form_data = form.cleaned_data
        args = {'form': form, 'td': td, 'hs': hs, 'cr': cr}
        return render(request, self.template_name, args)

def table_data(d: dict) -> list:
    td = []
    s = d['major'].split(' | ')[0]
    m = d['major'].split(' | ')[1]
    td.append((('School', s), school[s]))
    td.append((('Major', m), major[s][m]))
    td.append((('Gender', d['gender']), gender[d['gender']]))
    td.append((('Ethnicity', d['ethnicity']), ethnicity[d['ethnicity']]))
    td.append((('School & Gender', s + " & " + d['gender']), school_gender[s][d['gender']]))
    td.append((('School & Ethnicity', s + " & " + d['ethnicity']), school_ethnicity[s][d['ethnicity']]))
    td.append((('Residency', d['residency']), residency[d['residency']]))
    td.append((('UC GPA', d['uc_gpa']), uc_gpa[d['uc_gpa']]))
    td.append((('SAT Verbal', d['sat_verbal']), sat_verbal[d['sat_verbal']]))
    td.append((('SAT Math', d['sat_math']), sat_math[d['sat_math']]))
    td.append((('SAT Writing', d['sat_writing']), sat_writing[d['sat_writing']]))
    return td

def chance_range(l: list) -> str:
    result = []
    for element in l:
        result.append(float(element[1]['selectivity_rate'].strip('%')))
    return "Your chances of admission range between {}% to {}%.".format(sorted(result)[0], sorted(result)[-1])

def highSchool(d: dict) -> str:
    if d['high_school'] != 'OTHER / NOT LISTED':
        return "Fun Fact: In 2016, {} people from {} enrolled at UC Irvine.".format(high_school[d['high_school']]['admitted'], d['high_school'].title())
    else:
        return ""
