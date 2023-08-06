from django.conf import settings
from psu_base.classes.Log import Log

log = Log()

__version__ = "0.0.3"

__all__ = []

# Default settings
_DEFAULTS = {
    # Admin Menu Items
    "PSU_CALENDAR_ADMIN_LINKS": [
        # {
        #     'url': "psu_calendar:psu_calendar_index", 'label': "psu_calendar Feature", 'icon': "fa-whatever",
        #     'authorities': "admin"
        # },
    ]
}

# Assign default setting values
log.debug("Setting default settings for PSU_CALENDAR")
for key, value in list(_DEFAULTS.items()):
    try:
        getattr(settings, key)
    except AttributeError:
        setattr(settings, key, value)
    # Suppress errors from DJANGO_SETTINGS_MODULE not being set
    except ImportError as ee:
        log.debug(f"Error importing {key}: {ee}")
