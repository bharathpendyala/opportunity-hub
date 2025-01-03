from django.contrib import admin
from .models import Candidate, Education, Experience


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'city', 'nationality', 'occupation', 'activated')
    list_filter = ('city', 'nationality', 'occupation', 'activated')
    search_fields = ('user__username', 'first_name', 'last_name', 'city', 'nationality', 'occupation')
    readonly_fields = ('get_user_all_applicant', 'user')


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'institution', 'start_date', 'end_date')
    list_filter = ('institution', 'start_date', 'end_date')
    search_fields = ('candidate__user__username', 'institution', 'description')
    readonly_fields = ['candidate']


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'company', 'start_date', 'end_date')
    list_filter = ('company', 'start_date', 'end_date')
    search_fields = ('candidate__user__username', 'company', 'description')
    readonly_fields = ['candidate']
