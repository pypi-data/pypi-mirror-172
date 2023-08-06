from cms.forms.fields import PageSmartLinkField
from cms.utils.i18n import get_language_tuple
from django import forms
from django.forms.widgets import HiddenInput
from django.utils.translation import get_language

from giant_plugins.page_card.models import PageCard


class SmartLinkForm(forms.ModelForm):

    internal_link = PageSmartLinkField(
        placeholder_text="Select a page", 
        ajax_view="admin:cms_page_get_published_pagelist"
    )
    language = forms.ChoiceField(
        label="Language",
        choices=get_language_tuple(),
        help_text="The current language of the content fields.",
    )

    class Meta:
        model = PageCard
        fields = ["internal_link"]
        exclude = ("language",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["language"].widget = HiddenInput()

        if not self.fields["language"].initial:
            self.fields["language"].initial = get_language()

        if "internal_link" in self.fields:
            self.fields["internal_link"].widget.language = self.fields["language"].initial
