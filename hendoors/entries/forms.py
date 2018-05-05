from django import forms

from .models import Entry


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        exclude = ()

    def clean_categories(self):
        categories = self.cleaned_data['categories']
        for category in categories:
            if not category.is_accepting_entries:
                self.add_error(
                    'categories',
                    'Category "{}" is not currently accepting entries.'
                        .format(category.name)
                )
        return categories


class EntryImageForm(forms.Form):
    images = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}))
