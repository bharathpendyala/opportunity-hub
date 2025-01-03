from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, UpdateView, CreateView, DeleteView, View
from OpportunityHub.core.accounts_mixins import CandidateRequiredMixin, CandidateOwnerRequiredMixin, JobEditMixin
from OpportunityHub.jobs.models import FavoriteJob, Applicant, Skills
from OpportunityHub.candidates.forms import EditProfileFrom, EducationForm, WrokExperienceForm
from OpportunityHub.candidates.models import Candidate, Education, Experience
from OpportunityHub.notifications.models import NotificationCandidate
from rest_framework import viewsets, permissions
from .models import Candidate
from .serializers import CandidateSerializer

userModel = get_user_model()
# Create your views here.


class CandidateDashboard(LoginRequiredMixin, CandidateRequiredMixin, TemplateView):
    template_name = "candidates/candidate_dashboard.html"

    def get_context_data(self, **kwargs):

        all_favourite = FavoriteJob.objects.filter(user_id=self.request.user.pk).count()
        all_jobs_apply = Applicant.objects.filter(user_id=self.request.user.pk).count()
        all_jobs_pending = Applicant.objects.filter(user_id=self.request.user.pk).filter(status=1).count()
        all_jobs_accepted = Applicant.objects.filter(user_id=self.request.user.pk).filter(status=2).count()
        all_jobs_rejected = Applicant.objects.filter(user_id=self.request.user.pk).filter(status=3).count()


#         job_creator_jobs = Job.objects.filter(user=self.request.user)
#         all_favourite = FavoriteJob.objects.filter(job__in=job_creator_jobs).count()
#         user_jobs = Job.objects.filter(user=self.request.user)
#
#         job_count = FavoriteJob.objects.filter(job__in=job_creator_jobs).count()
#
#         job_for_this_user = Job.objects.filter(user=self.request.user, is_published=True)
#
#
# #   get all applicant for current logged user
#         all_applicant = (
#             Applicant.objects.filter(job__user=self.request.user, job__is_published=True)
#             .values('user')
#             .count()
#         )
#
        context = super().get_context_data(**kwargs)
#         context['user_jobs'] = user_jobs
#         context['job_count'] = job_count
        context['all_favourite'] = all_favourite
        context['all_jobs_apply'] = all_jobs_apply
        context['all_jobs_pending'] = all_jobs_pending
        context['all_jobs_rejected'] = all_jobs_rejected
        context['all_jobs_accepted'] = all_jobs_accepted
        return context


class AllEmployees(ListView):
    model = Candidate
    template_name = "candidates/all_candidates.html"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(activated=True)
        city = self.request.GET.get('city')
        if city:
            queryset = queryset.filter(city__icontains=city)
        skill_name = self.request.GET.get('skill')
        if skill_name:
            queryset = queryset.filter(skills__name=skill_name)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['skills'] = Skills.objects.all()
        return context

    # def get_queryset(self):
    #     # Use prefetch_related to fetch all related languages for each Candidate
    #     print(Candidate.objects.prefetch_related('languages').all())
    #     return Candidate.objects.prefetch_related('languages').all()


class CandidateDetails(DetailView):
    model = Candidate
    template_name = "candidates/candidates_details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['skills'] = Skills.objects.all()
        return context


class EditProfile(LoginRequiredMixin, UpdateView):
    model = Candidate
    template_name = "candidates/edit_profile.html"
    form_class = EditProfileFrom
    success_url = reverse_lazy("job seeker dashboard")

    def get_object(self, queryset=None):
        # Get the Candidate instance associated with the current logged-in user
        return self.request.user.candidate


class FavouriteJobs(LoginRequiredMixin, CandidateRequiredMixin, ListView):
    template_name = "candidates/favourite_jobs.html"

    def get_queryset(self):
        return FavoriteJob.objects.filter(user=self.request.user).select_related('job')


class ApplyJobs(LoginRequiredMixin, CandidateRequiredMixin, ListView):
    template_name = "candidates/apply-jobs.html"

    def get_queryset(self):
        return Applicant.objects.filter(user_id=self.request.user.pk).all()


class AddEducation(CreateView):
    model = Education
    template_name = "candidates/add_education.html"
    form_class = EducationForm
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        candidate_pk = self.kwargs['pk']
        candidate = get_object_or_404(Candidate, pk=candidate_pk)
        # Set the candidate field and save the form
        form.instance.candidate = candidate
        return super().form_valid(form)

    def get_success_url(self):
        # return reverse_lazy('edit-profile', kwargs={'pk': self.kwargs['pk']})
        return reverse_lazy('job seeker dashboard')


class EditEducation(LoginRequiredMixin, CandidateRequiredMixin, JobEditMixin, UpdateView):
    model = Education
    template_name = "candidates/edit_education.html"
    form_class = EducationForm

    def get_success_url(self):
        # return reverse_lazy('edit-profile', kwargs={'pk': self.kwargs['pk']})
        return reverse_lazy('job seeker dashboard')


class DeleteEducation(LoginRequiredMixin, CandidateRequiredMixin, JobEditMixin, DeleteView):
    model = Education
    template_name = "candidates/delete_education.html"
    success_url = reverse_lazy('job seeker dashboard')


class AddWorkExperience(CreateView):
    # model = Experience
    template_name = "candidates/add_work_experience.html"
    form_class = WrokExperienceForm

    def form_valid(self, form):
        candidate_pk = self.kwargs['pk']
        candidate = get_object_or_404(Candidate, pk=candidate_pk)
        # Set the candidate field and save the form
        form.instance.candidate = candidate
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('job seeker dashboard')


class EditWorkExperience(CandidateRequiredMixin, JobEditMixin, UpdateView):
    model = Experience
    template_name = "candidates/edit_edit_work_experience.html"
    form_class = WrokExperienceForm

    def get_success_url(self):
        # return reverse_lazy('edit-profile', kwargs={'pk': self.kwargs['pk']})
        return reverse_lazy('job seeker dashboard')


class DeleteWorkExperience(LoginRequiredMixin, CandidateRequiredMixin, JobEditMixin, DeleteView):
    model = Experience
    template_name = "candidates/delete_experience.html"
    success_url = reverse_lazy('job seeker dashboard')


class CandidateDeleteView(LoginRequiredMixin, CandidateRequiredMixin, DeleteView):
    model = userModel
    template_name = "candidates/delete_profile.html"
    success_url = reverse_lazy('deleted_success')

    def get_object(self, queryset=None):
        return self.request.user


class ProfileDeletedView(TemplateView):
    template_name = "candidates/profile_deleted.html"


class CandidateViewSet(viewsets.ModelViewSet):
    queryset = Candidate.objects.filter(activated=True)
    serializer_class = CandidateSerializer
    permission_classes = permissions.AllowAny,
    pagination_class = None  # Disable pagination

    def get_queryset(self):
        queryset = Candidate.objects.filter(activated=True)
        city = self.request.query_params.get('city', None)
        if city:
            queryset = queryset.filter(city=city)
        return queryset

