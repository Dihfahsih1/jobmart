from django.db import models
from django.urls import reverse
from django.utils import timezone

from accounts.models import User
from tags.models import Tag
from .manager import JobManager
from accounts.models import Skillset
from ckeditor.fields import RichTextField

JOB_TYPE = (
    ("1", "Full time"),
    ("2", "Part time"),
    ("3", "Internship"),
)


class Job(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    description = RichTextField()
    job_image =models.FileField(upload_to='jobs', null=True, blank=True)
    location = models.CharField(max_length=150)
    type = models.CharField(choices=JOB_TYPE, max_length=10)
    category = models.CharField(max_length=100)
    last_date = models.DateTimeField()
    
    created_at = models.DateTimeField(default=timezone.now)
    filled = models.BooleanField(default=False)
    
    salary = models.IntegerField(default=0, blank=True)
    tags = models.ManyToManyField(Tag,blank=True)
    skill = models.CharField(max_length=100,null=True,blank=True)
    job_poster = models.CharField(max_length=100,null=True,blank=True)
    #skill = models.ManyToManyField(Skillset, blank=True)
    is_active = models.BooleanField(default=False)
    objects = JobManager()

    class Meta:
        ordering = ["id"]

    def get_absolute_url(self):
        return reverse("jobs:jobs-detail", args=[self.id])

    def __str__(self):
        return self.title
    
class JobCategory(models.Model):
    name = models.CharField(max_length=100, blank=True,null=True)
    def __str__(self):
        return self.name
    

class Resume(models.Model):
    #category = models.ForeignKey(JobCategory,on_delete=models.CASCADE, blank=True,null=True)
    file = models.FileField(upload_to="resumes/%Y/%m/%d/", blank=True,null=True)
    def __str__(self):
        return "Cv-batch: "+ str(self.id) 
    
class Applicant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    upload_resume = models.FileField(upload_to='documents')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applicants")
    created_at = models.DateTimeField(default=timezone.now)
    comment = models.TextField(blank=True, null=True)
    status = models.SmallIntegerField(default=1)

    class Meta:
        ordering = ["id"]
        unique_together = ["user", "job"]

    def __str__(self):
        return self.user.get_full_name()

    @property
    def get_status(self):
        if self.status == 1:
            return "Pending"
        elif self.status == 2:
            return "Accepted"
        else:
            return "Rejected"


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="favorites")
    created_at = models.DateTimeField(default=timezone.now)
    soft_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.job.title()
     
class JobSkillset(models.Model):
    user = models.ForeignKey(Job, on_delete=models.CASCADE, blank=True, null=True)
    skill = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.user +  "- " + self.skill + '_' + self.id)
