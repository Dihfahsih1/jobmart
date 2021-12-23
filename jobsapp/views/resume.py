from django.views.generic.edit import FormView
from ..forms import MultipleCvUploadForm
from ..models import Resume
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, ListView, UpdateView, DetailView
from django.http import Http404, HttpResponseRedirect, JsonResponse

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
    
    paginate_by = 2
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.request.GET.get("q",)
        context['query'] = self.request.GET.get('q')
        context['nobjects'] = self.get_queryset().count()
        return context
    
    def get_queryset(self): # new
        query = self.request.GET.get('q')
        object_list = self.model.objects.filter(
            category__name__contains=query,
        )
        # if 'q':
        #     object_list = self.model.objects.filter(
        #     category__name__contains=query )
            
        return object_list

 

        
class ResumeListView(ListView):
    model = Resume
    template_name = "resume/resume_index.html"
    context_object_name = "resumes"
    
    
class ResumeDetailsView(DetailView):
    model = Resume
    template_name = "resume/details.html"
    context_object_name = "resume"
    pk_url_kwarg = "id"

    def get_object(self, queryset=None):
        obj = super(ResumeDetailsView, self).get_object(queryset=queryset)
        if obj is None:
            raise Http404("Job doesn't exists")
        return obj

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            # raise error
            raise Http404("Cv doesn't exists")
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)