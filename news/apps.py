from django.apps import AppConfig


class NewsConfig(AppConfig):
    """
    Configuration class for the 'news' app.
    Handles app-specific settings and initialization.
    """
    name = "news"

    def ready(self):
        """
        Imports signal handlers for the 'news' app when the app is ready.
        """
        import news.signals
