from datetime import datetime

from django import forms
from django.core.exceptions import ValidationError

from jobsapp.models import Job, Applicant

from django.forms import ModelForm, models,  inlineformset_factory

from .models import JobSkillset

from multiupload.fields import MultiFileField, MultiMediaField, MultiImageField

class MultipleCvUploadForm(forms.Form):
    cv_files = MultiFileField(min_num=1, max_num=3000, max_file_size=1024*1024*5)
    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'ModelName'
        verbose_name_plural = 'ModelNames'
    
class CreateJobForm(forms.ModelForm):
    class Meta:
        model = Job
        exclude = (
            "user",
            "created_at",
        )
        labels = {
            "last_date": "Last Date",
            "company_name": "Company Name",
            "company_description": "Company Description",
        }

    def is_valid(self):
        valid = super(CreateJobForm, self).is_valid()

        # if already valid, then return True
        if valid:
            return valid
        return valid

    def clean_last_date(self):
        date = self.cleaned_data["last_date"]
        if date.date() < datetime.now().date():
            raise ValidationError("Last date can't be before from today")
        return date

    

    
class JobSkillsetForm(ModelForm):
    class Meta:
        model = JobSkillset
        fields = ['user','skill']
        exclude = ()
JobskilsFormset = inlineformset_factory(Job, JobSkillset, form=JobSkillsetForm, extra=2)

class ApplyJobForm(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = ("job",)
