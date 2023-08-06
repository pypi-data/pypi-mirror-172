from django.shortcuts import render, redirect
from psu_base.classes.Log import Log
from psu_calendar.services import calendar_service


log = Log()


def sample_calendar(request):
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
        2: {"heading": "Day TWO..."},
        3: ["Red", "Orange", "Yellow", "Green", "Blue", "Purple"],
        5: ("Hello", "World", "Tuple"),
        8: list(range(1024, 1100)),
        13: {"heading": "Big Day!", "payload": str(list(range(1024, 1100)))},
    }
    month.populate_days(sample_data)

    # Set a day heading
    month.get_day(21).heading = "Someone's Birthday!"

    return render(request, "psu_calendar/sample.html", {"month": month})
