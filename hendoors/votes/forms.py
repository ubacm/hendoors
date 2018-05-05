from django import forms
from django.core.exceptions import ObjectDoesNotExist

from hendoors.categories.models import Category
from hendoors.entries.models import Entry
from . import utils


class VoteCastForm(forms.Form):
    category = forms.ModelChoiceField(Category.objects.all())
    entry = forms.ModelChoiceField(Entry.objects.all())
    weight = forms.IntegerField(max_value=1, min_value=0, initial=1)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def clean_category(self):
        category = self.cleaned_data['category']
        if not category.is_accepting_votes():
            raise forms.ValidationError(
                'The category is not currently accepting votes.')
        return category

    def clean(self):
        category = self.cleaned_data.get('category')
        entry = self.cleaned_data.get('entry')
        if category and entry:
            if not entry.categories.filter(pk=category.pk).exists():
                self.add_error('entry', 'The entry is not in the specified category.')
        if self.user is None:
            raise forms.ValidationError('User not found.')
        if category.marks_required > 0:
            try:
                slack_id = self.user.extras['user']['id']
            except KeyError:
                raise forms.ValidationError('Slack user ID not found.')
            user_marks = utils.get_marks_by_id(slack_id)
            if user_marks < category.marks_required:
                self.add_error(
                    'category',
                    'This category requires {} marks to vote (you have {}).'
                        .format(category.marks_required, user_marks)
                )
