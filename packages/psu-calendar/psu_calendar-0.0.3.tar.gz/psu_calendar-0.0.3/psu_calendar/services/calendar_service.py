from psu_base.classes.Log import Log
from psu_base.services import utility_service, message_service
from psu_calendar.classes.month import Month
from datetime import date

log = Log()


def get_month(request):
    """
    Get month to display, or False if redirect required
    """
    log.trace()

    # Default to current year and month
    today = date.today()
    yy = int(today.strftime('%Y'))
    mm = int(today.strftime('%m'))
    redirect_ind = False

    # Get current month/year selection
    year = utility_service.get_session_var('psu-calendar-year', yy)
    month = utility_service.get_session_var('psu-calendar-month', mm)

    # If new month/year was selected
    try:
        if request.GET.get('month'):
            new_month = request.GET.get('month')
            if new_month == 'prev':
                month -= 1
            elif new_month == 'next':
                month += 1
            else:
                month = int(new_month)

            if month == 13:
                year += 1
                month = 1
            elif month == 0:
                year -= 1
                month = 12

            # Redirect after saving to avoid page refresh from changing the month again
            redirect_ind = True
    except Exception as ee:
        message_service.post_error("Invalid month/year selection")
        log.debug(ee)

    # Remember current month/year selection
    utility_service.set_session_var('psu-calendar-year', year)
    utility_service.set_session_var('psu-calendar-month', month)

    if redirect_ind:
        return False
    else:
        return Month(year=year, month=month)

