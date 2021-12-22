from django.views.generic.edit import FormView
from ..forms import MultipleCvUploadForm
from ..models import Resume
from django.contrib.messages.views import SuccessMessageMixin

class MultipleCvUploadView(SuccessMessageMixin,FormView):
    template_name = 'resume/Multiple_resume_form.html'
    form_class = MultipleCvUploadForm
    success_message = "All the cvs have been uploaded into the database!"
    success_url = '/'

    def form_valid(self, form):
        form_category=form.cleaned_data['category']
        for form_file in form.cleaned_data['cv_files']:
            Resume.objects.create(file=form_file,category=form_category)
        
        Resume.objects.create(file=form_file)
        return super(MultipleCvUploadView, self).form_valid(form)