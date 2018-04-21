from django import forms

from hendoors.categories.models import Category
from hendoors.entries.models import Entry


class VoteCastForm(forms.Form):
    category = forms.ModelChoiceField(Category.objects.all())
    entry = forms.ModelChoiceField(Entry.objects.all())
    weight = forms.IntegerField(max_value=1, min_value=0)

    def clean_category(self):
        category = self.cleaned_data['category']
        if not category.is_accepting_votes():
            raise forms.ValidationError('The category is not currently accepting votes.')
        return category

    def clean(self):
        category = self.cleaned_data.get('category')
        entry = self.cleaned_data.get('entry')
        if category and entry:
            if not entry.categories.filter(pk=category.pk).exists():
                self.add_error('entry', 'The entry is not in the specified category.')
