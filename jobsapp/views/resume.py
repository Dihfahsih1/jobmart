from django.views.generic.edit import FormView
from ..forms import MultipleCvUploadForm
from ..models import Resume
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, ListView, UpdateView, DetailView

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
    
    #search for candidate
class ResumeSearchView(ListView):
    model = Resume
    template_name = "resume/resume_search.html"
    context_object_name = "resumes"

    def get_queryset(self):
        # q = JobDocument.search().query("match", title=self.request.GET['position']).to_queryset()
        # print(q)
        # return q
        return self.model.objects.filter(
            category__contains=self.request.GET.get("category", ),
        )
        
class ResumeListView(ListView):
    model = Resume
    template_name = "resume/resume_search.html"
    context_object_name = "resumes"
    paginate_by = 5