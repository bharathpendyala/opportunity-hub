from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, UpdateView, DetailView, DeleteView
from rest_framework.response import Response

from OpportunityHub.company.forms import EditCompanyFrom
from OpportunityHub.company.models import CompanyProfile
from OpportunityHub.company.serializers import CompanyProfileSerializer
from OpportunityHub.core.accounts_mixins import CompanyRoleRequiredMixin, ApplicantOwnerRequiredMixin
from OpportunityHub.jobs.models import Job, Applicant, FavoriteJob
from OpportunityHub.main.models import CompanySubscription
from rest_framework import viewsets, generics, permissions

userModel = get_user_model()


class CompanyDashboard(LoginRequiredMixin, CompanyRoleRequiredMixin, TemplateView):
    template_name = "company/company_dashboard.html"

    def get_context_data(self, **kwargs):
        job_creator_jobs = Job.objects.filter(user=self.request.user)
        all_favourite = FavoriteJob.objects.filter(job__in=job_creator_jobs).count()
        user_jobs = Job.objects.filter(user=self.request.user)
        job_count = FavoriteJob.objects.filter(job__in=job_creator_jobs).count()


 
        all_applicant = (
            Applicant.objects.filter(job__user=self.request.user, job__is_published=True)
            .values('user')
            .count()
        )

        context = super().get_context_data(**kwargs)
        context['user_jobs'] = user_jobs
        context['job_count'] = job_count
        context['all_favourite'] = all_favourite
        context['all_applicant'] = all_applicant
        return context


class CreatedJobs(LoginRequiredMixin, CompanyRoleRequiredMixin, ListView):
    template_name = "company/created-jobs.html"

    def get_queryset(self):
        jobs = Job.objects.filter(user__id=self.request.user.pk).order_by('-id')
        return jobs


class EditCompany(LoginRequiredMixin, CompanyRoleRequiredMixin, UpdateView):
    model = CompanyProfile
    form_class = EditCompanyFrom
    success_url = reverse_lazy("company-dashboard")
    template_name = "company/edit_company.html"

    def get_object(self, queryset=None):
        return self.request.user.company


class CompanyApplicant(LoginRequiredMixin, CompanyRoleRequiredMixin, ListView):
    model = Job
    template_name = 'company/jobs_list_aplicant.html'  # Create this template if needed
    context_object_name = 'jobs'

    def get_queryset(self):
        user = self.request.user
     
        return Job.objects.filter(user=user, is_published=True).annotate(num_applicants=Count('applicants')).filter(num_applicants__gt=0)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job_applicants_count = {}
        for job in context['jobs']:
            applicants_count = Applicant.objects.filter(job=job).count()
            job_applicants_count[job.id] = applicants_count
        context['job_applicants_count'] = job_applicants_count
        return context


class ApplicantList(LoginRequiredMixin, CompanyRoleRequiredMixin, ApplicantOwnerRequiredMixin, ListView):
    model = Applicant
    template_name = 'company/applicant_list.html'  # Create this template if needed

    def get_queryset(self):
        job_pk = self.kwargs['pk']
        job = get_object_or_404(Job, pk=job_pk)
        return job.applicants.all()


class CompanyDetails(DetailView):
    model = CompanyProfile
    template_name = "company/company_details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company = self.get_object()
        if self.request.user.is_authenticated:
            is_subscribed = CompanySubscription.objects.filter(
                candidate=self.request.user,
                company=company.user
            ).exists()
        else:
            is_subscribed = False

        jobs_published = Job.objects.filter(user=company.user)
        context['jobs_published'] = jobs_published
        context['is_subscribed'] = is_subscribed
        return context


class AllCompany(ListView):
    model = CompanyProfile
    paginate_by = 10
    template_name = "company/company.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(activated=True)

        return queryset


class CompanyDeleteView(LoginRequiredMixin, CompanyRoleRequiredMixin, DeleteView):
    model = userModel
    template_name = "company/delete_profile.html"
    success_url = reverse_lazy('deleted_success_company')

    def get_object(self, queryset=None):
        # Return the Candidate instance for the current logged-in user
        return self.request.user


class CompanyDeletedView(TemplateView):
    template_name = "company/profile_deleted.html"




# class CompanyProfileViewSet(generics.ListCreateAPIView):
#     queryset = CompanyProfile.objects.filter(activated=True)
#     serializer_class = CompanyProfileSerializer
#     pagination_class = None  # Disable pagination


class CompanyProfileViewSet(viewsets.ModelViewSet):
    queryset = CompanyProfile.objects.filter(activated=True)
    serializer_class = CompanyProfileSerializer
    pagination_class = None  # Disable pagination
    permission_classes = permissions.AllowAny,

    # New method to retrieve details of a specific company by ID
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
