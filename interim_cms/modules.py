from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType

from grappelli.dashboard.modules import DashboardModule

from interim_cms.views import ExampleTileView


class DashboardModuleViewBase(DashboardModule):

    column = 1

    def init_with_context(self, context):
        if self._initialized:
            return

        # Something utterly bizarre in Grappelli requires a non-empty children
        # queryset else the template doesn't render.
        self.children = ContentType.objects.all()

        # Hook to set more context. Subclasses can implement.
        self.on_init_with_context(context)

        # Render the view
        request = context["request"]
        # Forms in views posts are always handled via ajax. If the center
        # dashboard triggers a post these views cannot handle those posts.
        # Change request to a get.
        restore = False
        if request.method == "POST":
            restore = True
            request.method = "GET"
        if hasattr(self, "view_class"):
            view = self.view_class.as_view()(request)
            self.template = view.template_name[0]
            context["rendered"] = view.rendered_content
        if restore:
            request.method = "POST"

        self._initialized = True

    def on_init_with_context(self, context):
        return


class ExampleModule(DashboardModuleViewBase):
    title = _("Example Module")
    view_class = ExampleTileView


class StaticModule(DashboardModuleViewBase):
    """Render a static template"""
    pass