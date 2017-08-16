from django.forms import ModelForm
from calculator.models import Applicant

class ApplicantForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ApplicantForm, self).__init__(*args, **kwargs)
        self.fields['high_school'].label = "High School"
        self.fields['uc_gpa'].label = "UC GPA"
        self.fields['sat_math'].label = "SAT Math"
        self.fields['sat_verbal'].label = "SAT Verbal"
        self.fields['sat_writing'].label = "SAT Writing"
    class Meta:
        model = Applicant
        fields = '__all__'