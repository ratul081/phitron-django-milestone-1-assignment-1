from django import forms
from tasks.models import Event, Participant, Category
from django.utils import timezone


class StyleFormMixin:
    default_class = "w-full border-2 border-gray-300 p-12 rounded-md shadow-sm mb-5"

    def style_widgets(self):
        for field in self.fields.values():
            field.widget.attrs.update({"class": self.default_class})
            if isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({"rows": 5})
            elif isinstance(field.widget, forms.SelectDateWidget):
                field.widget.attrs.update({"class": "border-2 border-gray-300 p-1 rounded-md shadow-sm mb-5"})
            elif isinstance(field.widget, (forms.RadioSelect, forms.CheckboxSelectMultiple)):
                field.widget.attrs.update({"class": "space-y-4 text-xl"})


class EventModelForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Event
        fields = ["name", "description", "date", "location", "category"]
        widgets = {
            "description": forms.Textarea(),
            "date": forms.SelectDateWidget(),
            "category": forms.RadioSelect()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.style_widgets()

    def clean_date(self):
        date = self.cleaned_data.get("date")
        if date and date < timezone.now().date():
            raise forms.ValidationError("Event date cannot be in the past.")
        return date


class ParticipantModelForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Participant
        fields = ["name", "email", "event"]
        widgets = {
            "email": forms.EmailInput(),
            "event": forms.CheckboxSelectMultiple()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.style_widgets()


class CategoryModelForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "description"]
        widgets = {
            "description": forms.Textarea()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.style_widgets()
