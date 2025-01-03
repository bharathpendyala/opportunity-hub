from ckeditor.widgets import CKEditorWidget
from django.forms import ModelForm, ModelMultipleChoiceField, CheckboxSelectMultiple, CharField, DateInput

from OpportunityHub.jobs.models import Skills
from OpportunityHub.candidates.models import Candidate, Education, Experience


class EditProfileFrom(ModelForm):
    required_css_class = 'required'

    class Meta:
        model = Candidate
        exclude = ["user"]

        widgets = {
            'about': CharField(widget=CKEditorWidget())
            # 'is_published': CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    skills = ModelMultipleChoiceField(
        queryset=Skills.objects.all(),

        widget=CheckboxSelectMultiple,
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        self.fields["skills"].widget.attrs['class'] = "form-check"


class EducationForm(ModelForm):
    required_css_class = 'required'


    class Meta:
        model = Education
        exclude = ["candidate"]

        widgets = {
            'start_date': DateInput(attrs={'type': 'date'}),
            'end_date': DateInput(attrs={'type': 'date'}),
        }


class WrokExperienceForm(ModelForm):
    required_css_class = 'required'


    class Meta:
        model = Experience
        exclude = ["candidate"]

        widgets = {
            'start_date': DateInput(attrs={'type': 'date'}),
            'end_date': DateInput(attrs={'type': 'date'}),
        }
