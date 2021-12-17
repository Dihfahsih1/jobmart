from datetime import datetime

from django import forms
from django.core.exceptions import ValidationError

from jobsapp.models import Job, Applicant

from django.forms import ModelForm, models,  inlineformset_factory

from accounts.models import User,Skillset
from .models import JobSkillset


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

    def clean_skills(self):
        skills = self.cleaned_data["skill"]
        if len(skills) > 6:
            raise forms.ValidationError("You can't add more than 6 skills")
        return skills

    def save(self, commit=True):
        job = super(CreateJobForm, self).save(commit=False)
        if commit:
            job.save()
            for skill in self.cleaned_data["skill"]:
                job.skill.add(skill)
        return job
    
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
