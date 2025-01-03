# Generated by Django 5.0.2 on 2024-04-10 15:35

import ckeditor.fields
import cloudinary.models
import django.db.models.deletion
import OpportunityHub.core.validators
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('jobs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyProfile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='company', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('name', models.CharField(max_length=40, validators=[OpportunityHub.core.validators.validate_start_with_upper])),
                ('description', ckeditor.fields.RichTextField()),
                ('location', models.CharField(max_length=40)),
                ('phone', models.CharField(blank=True, max_length=20, null=True, validators=[OpportunityHub.core.validators.validate_phone_number])),
                ('address', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254)),
                ('image', cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='image')),
                ('website_url', models.URLField(blank=True, null=True)),
                ('linkedin_url', models.URLField(blank=True, null=True)),
                ('facebook_url', models.URLField(blank=True, null=True)),
                ('employees', models.PositiveIntegerField(default=0)),
                ('foundation_year', models.PositiveIntegerField(default=0)),
                ('activated', models.BooleanField(default=False)),
                ('skills', models.ManyToManyField(related_name='technologies', to='jobs.skills', verbose_name='Technologies')),
            ],
            options={
                'ordering': ['-pk'],
            },
        ),
    ]
