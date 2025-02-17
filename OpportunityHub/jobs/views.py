from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, View, DeleteView
from rest_framework import permissions
from rest_framework.generics import ListAPIView

from OpportunityHub.company.models import CompanyProfile
from OpportunityHub.core.accounts_mixins import CompanyRoleRequiredMixin, JobByCompanyMixin, CompanyProfileActivationMixin, \
    ApplicantCompanyMixin
from OpportunityHub.core.decorators import candidate_activated_required
from OpportunityHub.jobs.forms import CreateJobForms, EditeJobForm, ApplyForJobForms, ChangeStatusForm
from OpportunityHub.jobs.models import Job, Category, Applicant, FavoriteJob
from OpportunityHub.jobs.serializers import JobSerializer
from OpportunityHub.main.models import Seniority, CompanySubscription

userModel = get_user_model()

class JobCreateView(LoginRequiredMixin, CompanyRoleRequiredMixin, CompanyProfileActivationMixin, CreateView):
    template_name = "jobs/create_job.html"
    form_class = CreateJobForms
    extra_context = {"title": "Post New Job"}
    success_url = reverse_lazy("company-dashboard")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(JobCreateView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class AllJobsView(ListView):
    model = Job
    template_name = "jobs/jobs_list.html"
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        seniority_filter = self.request.GET.get('seniority')
        queryset = Job.objects.filter(is_published=True)

        if seniority_filter:
            queryset = queryset.filter(seniority__name=seniority_filter)

        if query:
            # If a search query is present, filter the queryset by job title
            queryset = queryset.filter(title__icontains=query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = Category.objects.all()
        context["seniorities"] = Seniority.objects.all()
        context['search_query'] = self.request.GET.get('q', '')
        return context


class JobDetails(DetailView):
    template_name = "jobs/job-details.html"
    model = Job

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_anonymous:
            return context

        job = context['object']
        context["already_in_favourite"] = FavoriteJob.objects.filter(user=self.request.user, job=job).exists()
        context["already_apply"] = Applicant.objects.filter(user=self.request.user, job=job).exists()
        context["status"] = Applicant.objects.filter(user=self.request.user, job=job)
        # Access the CompanyProfile through the user's ID
        company_profile = CompanyProfile.objects.get(user_id=job.user_id)
        context['company'] = company_profile
        return context


class EditJob(LoginRequiredMixin, CompanyRoleRequiredMixin, JobByCompanyMixin, UpdateView):
    model = Job
    form_class = EditeJobForm
    template_name = "jobs/edit-job.html"

    def get_success_url(self):
        return reverse_lazy("job_details",  kwargs={"pk": self.object.pk})


# class AddToFavoritesView(LoginRequiredMixin, View):
#     # @login_required
#     def post(self, request, pk):
#         job = get_object_or_404(Job, id=pk)
#
#         # Check if the job is already in favorites for the current user
#         if FavoriteJob.objects.filter(user=request.user, job=job).exists():
#             # Job is already in favorites, handle this case (e.g., display a message)
#             pass
#         else:
#             # Job is not in favorites, add it to the favorites
#             FavoriteJob.objects.create(user=request.user, job=job)
#
#         return redirect('job_details', pk)

# class AddToFavoritesView(LoginRequiredMixin, CreateView):
#     model = FavoriteJob
#     template_name = 'add_to_favorites.html'
#     fields = []
#
#     def form_valid(self, form):
#         job = get_object_or_404(Job, pk=self.kwargs['pk'])
#         form.instance.user = self.request.user
#         form.instance.job = job
#         return super().form_valid(form)
#
#     def get_success_url(self):
#         job = get_object_or_404(Job, pk=self.kwargs['pk'])
#         return reverse_lazy("job_details",  kwargs={"pk": job.pk})


class RemoveFromFavoritesView(LoginRequiredMixin, View):

    def post(self, request, pk):
        job = get_object_or_404(Job, id=pk)

        # Check if the job is in favorites for the current user
        favorite_job = FavoriteJob.objects.filter(user=request.user, job=job).first()

        if favorite_job:
            # Job is in favorites, remove it
            favorite_job.delete()

        return redirect('job_details', pk)


@login_required
@candidate_activated_required
def apply_for_job(request, pk):
    job = get_object_or_404(Job, id=pk)

    if request.user.is_authenticated and request.user.role == 'candidate':

        # Check if the user has already applied for this job
        if not Applicant.objects.filter(user=request.user, job=job).exists():
            # Create an Applicant instance and save it to the database
            Applicant.objects.create(user=request.user, job=job)
            # You can also use a form to save additional data if needed
            form = ApplyForJobForms(request.POST or None)
            if form.is_valid():
                applicant = form.save(commit=False)
                applicant.user = request.user
                applicant.job = job
                applicant.save()

    return redirect('job_details', pk=job.id)


@login_required
def add_to_favorites(request, pk):
    if request.user.role != 'candidate':
        return redirect('job_details', pk=pk)

    job = get_object_or_404(Job, pk=pk)

    # Check if the job is not already in favorites
    if not FavoriteJob.objects.filter(user=request.user, job=job).exists():
        FavoriteJob.objects.create(user=request.user, job=job)

    return redirect('job_details', pk=pk)


class ChangeStatus(LoginRequiredMixin, CompanyRoleRequiredMixin, ApplicantCompanyMixin, UpdateView):
    model = Applicant
    template_name = "jobs/change_status.html"
    form_class = ChangeStatusForm

    def get_success_url(self):
        return reverse_lazy("applicant_list", kwargs={"pk": self.object.job_id})


class DeleteJob(LoginRequiredMixin, CompanyRoleRequiredMixin, JobByCompanyMixin, DeleteView):
    model = Job
    template_name = "company/delete_job.html"
    success_url = reverse_lazy('company-dashboard')


@login_required
def subscribe_to_company(request, pk):
    company = get_object_or_404(userModel, pk=pk)
    is_subscribed = CompanySubscription.objects.filter(
        candidate=request.user,
        company=company
    ).exists()
    if request.method == 'POST':
        if is_subscribed:
            CompanySubscription.objects.filter(
                candidate=request.user,
                company=company
            ).delete()
        else:
            CompanySubscription.objects.create(
                candidate=request.user,
                company=company
            )
    return redirect('company-details', pk=pk)


class AllJobsViewApi(ListAPIView):
    serializer_class = JobSerializer
    pagination_class = None  # Disable pagination
    permission_classes = permissions.AllowAny,

    def get_queryset(self):
        queryset = Job.objects.filter(is_published=True)
        query = self.request.GET.get('q')
        seniority_filter = self.request.GET.get('seniority')

        if query:
            queryset = queryset.filter(title__icontains=query)

        if seniority_filter:
            queryset = queryset.filter(seniority=seniority_filter)

        return queryset