# Generated by Django 5.0.2 on 2024-04-10 15:35

import ckeditor.fields
import cloudinary.models
import django.db.models.deletion
import OpportunityHub.jobs.validators
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(allow_unicode=True, max_length=100, unique=True)),
                ('description', models.TextField(blank=True, max_length=300, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Skills',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('slug', models.SlugField(allow_unicode=True, max_length=100, unique=True)),
                ('description', ckeditor.fields.RichTextField()),
                ('responsibilities', ckeditor.fields.RichTextField()),
                ('benefits', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('job_image', cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='image')),
                ('vacancy', models.IntegerField(blank=True, null=True)),
                ('location', models.CharField(max_length=300)),
                ('job_type', models.CharField(choices=[('fulltime', 'Full time'), ('parttime', 'Part time'), ('remote', 'Remote'), ('internship', 'Internship')], max_length=10)),
                ('salary', models.CharField(blank=True, max_length=30)),
                ('deadline', models.DateField(validators=[OpportunityHub.jobs.validators.validate_deadline_after_today])),
                ('is_published', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs.category')),
                ('seniority', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.seniority')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('needed_skills', models.ManyToManyField(related_name='needed_skills', to='jobs.skills')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='FavoriteJob',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs.job')),
            ],
            options={
                'unique_together': {('user', 'job')},
            },
        ),
        migrations.CreateModel(
            name='Applicant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('comment', models.TextField(blank=True, null=True)),
                ('status', models.SmallIntegerField(default=1)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applicants', to='jobs.job')),
            ],
            options={
                'ordering': ['id'],
                'unique_together': {('user', 'job')},
            },
        ),
    ]
