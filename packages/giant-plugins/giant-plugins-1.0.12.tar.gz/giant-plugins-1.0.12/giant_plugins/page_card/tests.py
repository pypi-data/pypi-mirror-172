import pytest
from cms.api import create_page

from . import cms_plugins, models


@pytest.fixture
def page_obj():
    return create_page("Some Page Title", "base.html", "en-gb", published=True)
    

@pytest.fixture
def page_card(page_obj):
    return models.PageCard.objects.create(internal_link=page_obj)
    
class TestPageCardPlugin:
    """
    Test case for the PageCard Plugin
    """

    def test_template(self):
        """
        Test that the template of the plugin is correct
        """
        plugin = cms_plugins.PageCardPlugin()
        assert plugin.render_template == "plugins/page_card/item.html"

    def test_block_template(self):
        """
        Test that the template of the plugin block is correct
        """
        plugin = cms_plugins.PageCardBlockPlugin()
        assert plugin.render_template == "plugins/page_card/container.html"


@pytest.mark.django_db
class TestPageCardModel:
    """
    Test case for the PageCard Model
    """

    def test_str_page_title(self, page_card):
        assert str(page_card) == "Page Card for Some Page Title"

    def test_str_title(self):
        page_card = models.PageCard(title="Title")
        assert str(page_card) == "Page Card for Title"

    def test_str_pk(self):
        page_card = models.PageCard(pk=1)
        assert str(page_card) == "Page Card for #1"

    def test_is_published(self, page_card, page_obj):
        assert page_card.internal_link

    def test_is_published_no_page(self):
        obj = models.PageCard()

        assert obj.internal_link is None
        assert obj._page is None
        assert obj.is_page_published is False

    def test_is_published_page_published(self, page_card, page_obj):
        assert page_card._page == page_obj
        assert page_card.is_page_published is True

    def test_is_published_page_not_published(self, page_card, page_obj, mocker):
        mocker.patch.object(page_obj, "languages", "fr")

        assert page_card._page == page_obj
        assert page_card.is_page_published is False