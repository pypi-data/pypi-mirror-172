from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden
from psu_base.classes.Log import Log
from psu_base.services import utility_service, message_service
from psu_base.decorators import require_authority, require_authentication
from psu_calendar.classes.month import Month
from psu_calendar.services import calendar_service


log = Log()


@require_authentication()
def index(request):
    """
    Menu of ...
    """
    log.trace()

    month = calendar_service.get_month(request)

    # False month indicates need for redirect (to prevent page refresh from changing month again)
    if not month:
        return redirect("/")

    # Populate some sample day payloads
    sample_data = {
        1: "First day of the month!",
        2: {"heading": "Day Two...", "template": "psu_calendar/day.html", 'payload': "Hi!"},
        3: ["Red", "Orange", "Yellow", "Green", "Blue", "Purple"],
        5: ("Hello", "World", "Tuple"),
        8: list(range(1024, 1100)),
        13: {"heading": "Big Day!", "payload": str(list(range(1024, 1100)))},
    }
    month.populate_days(sample_data)

    # To use a different set of templates, you could do:
    # month.template_base_directory = "demo_calendar"

    # Set a day heading
    month.get_day(21).heading = "Someone's Birthday!"



    return render(request, "psu_calendar/sample.html", {"month": month})
