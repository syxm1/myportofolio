from django.forms import ModelForm, TextInput, Textarea, URLInput, Select

from main.models import Education, Experience


class ExperienceForm(ModelForm):
    class Meta:
        model = Experience

        # `started_at` is left out: the model sets it with auto_now_add=True,
        # which makes it non-editable — listing it here would raise a
        # FieldError when Django builds the form.
        fields = [
            "title",
            "description",
            "category",
            "thumbnail",
            "ended_at",
        ]

        labels = {
            "title": "Title",
            "description": "Description",
            "category": "Category",
            "thumbnail": "Thumbnail Link",
            "ended_at": "End Date",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "e.g. Competitive Programming Teacher",
                }
            ),
            "description": Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "What did you do in this role?",
                }
            ),
            "category": Select(),
            "thumbnail": URLInput(
                attrs={
                    "placeholder": "https://...",
                }
            ),
        }


class EducationForm(ModelForm):
    class Meta:
        model = Education

        # `started_at` is left out for the same reason as in ExperienceForm:
        # auto_now_add=True makes it non-editable.
        fields = [
            "institution",
            "program",
            "level",
            "description",
            "thumbnail",
            "ended_at",
        ]

        labels = {
            "institution": "Institution Name",
            "program": "Program",
            "level": "Level",
            "description": "Description",
            "thumbnail": "Thumbnail Link",
            "ended_at": "End Date",
        }

        widgets = {
            "institution": TextInput(
                attrs={
                    "placeholder": "e.g. University of Indonesia",
                }
            ),
            "program": TextInput(
                attrs={
                    "placeholder": "e.g. Computer Science",
                }
            ),
            "level": Select(),
            "description": Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "What did you focus on or do here?",
                }
            ),
            "thumbnail": URLInput(
                attrs={
                    "placeholder": "https://...",
                }
            ),
        }