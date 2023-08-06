from psu_base.classes.Log import Log
from psu_base.services import error_service
from datetime import date
import calendar
import os

log = Log()


class Month:
    year = None
    month = None
    month_name = None
    first_day = None
    last_day = None
    first_dow = None
    last_dow = None
    num_days = None
    pre_days = None
    days = None
    post_days = None

    # Multiple calendars in the same app may require different templates
    # This allows multiple overridden templates in the same app.
    # Each template (nav_header.html, month.html, day.html, style.css) must exist in the specified directory
    template_base_directory = "psu_calendar"

    def get_day(self, day_number):
        try:
            ii = day_number - 1
            return self.days[ii]
        except Exception as ee:
            error_service.record(ee)
            return None

    def set_day_payload(self, day_number, payload):
        """
        Payload may be anything.  To set heading and/or template along with payload, include a dict:
            {"heading": "Bla bla bla", "payload": <whatever>, "template": "bla/bla/bla.html"}
        """
        try:
            ii = day_number - 1
            # Allow setting heading and payload via dict
            if type(payload) is dict and ("heading" in payload or "template" in payload):
                self.days[ii].heading = payload.get("heading")
                self.days[ii].payload = payload.get("payload")
                self.days[ii].day_template = payload.get("template")
            else:
                self.days[ii].payload = payload
            return True
        except Exception as ee:
            error_service.record(ee)
            return False

    def populate_days(self, day_info):
        """
        Given a list or map of day data, populate the date into the associated days

            List: Each list element contains data for 1 day (indexes 0-30 are days 1-31).
                  An entry must exist for every day (days cannot be skipped)

            Dict/Map: {1: {payload}, 2: {payload}, ..., 31: {payload}}
                  Days can be skipped if no data is associated with that day
        """
        if type(day_info) is list:
            day_no = 0
            for payload in day_info:
                day_no += 1
                self.set_day_payload(day_no, payload)

        elif type(day_info) is dict:
            for day_no, payload in day_info.items():
                self.set_day_payload(day_no, payload)
        else:
            log.error("Invalid parameter: day_info")

    def header_template(self):
        return os.path.join(self.template_base_directory, "nav_header.html")

    def month_template(self):
        return os.path.join(self.template_base_directory, "month.html")

    def day_template(self):
        return os.path.join(self.template_base_directory, "day.html")

    def style_template(self):
        return os.path.join(self.template_base_directory, "style.css")

    def __init__(self, year, month):
        log.trace([year, month])
        self.year = int(year)
        self.month = int(month)

        # The returned first day-of-week does not match datetime's day-of-week numbering
        junk, self.num_days = calendar.monthrange(self.year, self.month)

        self.first_day = date(self.year, self.month, 1)
        self.first_dow = int(self.first_day.strftime("%w"))  # Sunday == 0
        self.month_name = self.first_day.strftime("%B")

        self.last_day = date(self.year, self.month, self.num_days)
        self.last_dow = int(self.last_day.strftime("%w"))  # Sunday == 0

        # Initialize each day of the month
        self.days = [Day(date(self.year, self.month, ii)) for ii in range(1, self.num_days + 1)]

        # Get spacers for days before/after this month
        self.pre_days = [x for x in list(range(0, self.first_dow))]
        self.post_days = [x for x in list(range(self.last_dow, 6))]


class Day:
    date = None
    number = None  # 1 - 31
    day_of_week = None  # 0 - 6
    name = None  # Monday, Tuesday, etc
    category = None  # past, today, future
    heading = None  # Text displayed at top of day, next to number
    payload = None  # App-specific content (model)
    day_template = None  # If using non-standard template for this day

    def is_today(self):
        return self.category == "today"

    def is_weekend(self):
        return self.name in ["Saturday", "Sunday"]

    def is_weekday(self):
        return not self.is_weekend()

    def is_past(self):
        return self.category == "past"

    def is_future(self):
        return self.category == "future"

    def payload_type(self):
        # <class 'NoneType'>
        return str(type(self.payload)).replace("<class '", "").replace("'>", "")

    def container_classes(self):
        pre = "psu_calendar"
        ll = [f"{pre}-day"]

        if self.is_weekend():
            ll.append(f"{pre}-weekend")
        else:
            ll.append(f"{pre}-weekday")

        if self.is_past():
            ll.append(f"{pre}-past")
        elif self.is_future():
            ll.append(f"{pre}-future")
        else:
            ll.append(f"{pre}-today")

        return " ".join(ll)

    def template(self):
        if self.day_template:
            return self.day_template
        else:
            return None  # Will default to month-level day_template function

    def __init__(self, this_date):
        self.date = this_date
        self.number = int(this_date.day)
        self.day_of_week = int(this_date.strftime("%w"))
        self.name = this_date.strftime("%A")

        today = date.today()
        if this_date < today:
            self.category = "past"
        elif this_date == today:
            self.category = "today"
        elif this_date > today:
            self.category = "future"
