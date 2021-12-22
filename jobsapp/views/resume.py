from django.views.generic.edit import FormView
from ..forms import MultipleCvUploadForm
from ..models import Resume

class MultipleCvUploadView(FormView):
    template_name = 'resume/Multiple_resume_form.html'
    form_class = MultipleCvUploadForm
    success_url = '/'

    def form_valid(self, form):
        for each in form.cleaned_data['cv_files']:
            Resume.objects.create(file=each)
        return super(MultipleCvUploadView, self).form_valid(form)