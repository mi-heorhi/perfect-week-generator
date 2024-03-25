import calendar
from datetime import datetime, timedelta, date
from io import open as file

from datetime import datetime
import time
from dateutil.tz import tzlocal
from tzlocal import get_localzone
import pytz
import yaml
import argparse
from yaml import Loader

from cal_setup import get_calendar_service


def create_single_event(name, dt_start, dt_end, description, time_zone):
    event = {
        'summary': name,
        'description': description,
        'start': {
            'dateTime': dt_start.strftime('%Y-%m-%dT%H:%M:00'),
            'timeZone': time_zone
        },
        'end': {
            'dateTime': dt_end.strftime('%Y-%m-%dT%H:%M:00'),
            'timeZone': time_zone
        },
        'reminders': {
            'useDefault': False,
        },
        'transparency': "transparent",
        'status': "confirmed"
    }
    return event


def create_all_day_event(name, date, description):
    event = {
        'summary': name,
        'description': description,
        'start': {
            'date': date.strftime('%Y-%m-%d'),
        },
        'end': {
            'date': date.strftime('%Y-%m-%d'),
        },
        'reminders': {
            'useDefault': False,
        },
        'transparency': "transparent",
        'status': "confirmed",
    }
    return event


def insert_events_calendar(calendar_id, events):
    service = get_calendar_service()
    for event in events:
        service.events().insert(calendarId=calendar_id +
                                '@group.calendar.google.com', body=event).execute()
    e = datetime.now()


def get_business_day_before_weekend(d):
    if d.weekday() == 5:
        return d - timedelta(days=1)
    if d.weekday() == 6:
        return d - timedelta(days=2)
    return d


def is_business_day(d):
    return d.weekday() != 5 and d.weekday() != 6


def is_weekend(d):
    return d.weekday() == 5 or d.weekday() == 6


def generate_all_day_events(template, day_range):
    events = []
    if template.get('entries') is not None:
        entries = template['entries']
        if entries is not None:
            day_numbers = [d.day for d in day_range]
            matching_entries = [e for e in entries if any(
                d == e['date'] for d in day_numbers)]
            for item in matching_entries:
                event = {}
                name = ''
                description = ''
                day = None
                if 'name' in item:
                    name = item['name']
                if 'description' in item:
                    description = item['description']
                if item['business_day'] is not None:
                    if item['business_day']:
                        day = get_business_day_before_weekend(
                            day_range[day_numbers.index(item['date'])])
                    else:
                        day = day_range[day_numbers.index(item['date'])]
                event = create_all_day_event(name, day, description)
                events.append(event)
    return events


def generate_single_events(template, day_range):
    events = []
    time_zone = get_current_timezone()
    week_plan = template['week']
    if template.get('week') is not None:
        for d in day_range:
            day_plan = week_plan[d.weekday()+1]
            if day_plan is not None:
                for item in day_plan:
                    description = ''
                    if 'description' in item:
                        description = item['description']
                    parsed_string = str(item['startAt']).split("-")
                    start_hour = int(parsed_string[0])
                    start_minute = 0 if len(
                        parsed_string) == 1 else int(parsed_string[1])
                    start = datetime(
                        d.year, d.month, d.day, start_hour, start_minute, 0, tzinfo=time_zone)
                    end = start + timedelta(minutes=item['duration'])
                    events.append(create_single_event(
                        item['name'], start, end, description, time_zone.key))
    return events


def get_current_timezone():
    current_timezone = get_localzone()
    return current_timezone


def get_date_range_next_week():
    next_week_start = date.today() + timedelta(days=(0 - date.today().weekday()) % 7)
    date_range = [next_week_start + timedelta(days=i) for i in range(7)]
    return date_range


def get_date_range_this_week():
    this_week_start = date.today() + timedelta(days=(0 - date.today().weekday()) % 7)
    date_range = [this_week_start + timedelta(days=i) for i in range(7)]
    return date_range


def get_date_range_this_month():
    this_month = date.today().replace(day=1)
    this_month_days = calendar.monthrange(this_month.year, this_month.month)[1]
    date_range = [this_month.replace(day=i)
                  for i in range(1, this_month_days+1)]
    return date_range


def get_date_range_next_month():
    next_month = date.today().replace(day=1) + timedelta(days=32)
    next_month_days = calendar.monthrange(next_month.year, next_month.month)[1]
    date_range = [next_month.replace(day=i)
                  for i in range(1, next_month_days+1)]
    return date_range


def generate_events_from_template(template, date_range):
    calendar_id = template['calendar-id']
    type = template['type']
    if type == 'single':
        events = generate_single_events(template, date_range)
        insert_events_calendar(calendar_id, events)
    elif type == 'all-day':
        events = generate_all_day_events(template, date_range)
        insert_events_calendar(calendar_id, events)


def generate_from_template(stream, frame):
    template = yaml.load(stream, Loader)
    date_range = []
    if frame == 'next-week':
        date_range = get_date_range_next_week()
    elif frame == 'next-month':
        date_range = get_date_range_next_month()
    elif frame == 'this-month':
        date_range = get_date_range_this_month()
    elif frame == 'this-week':
        date_range = get_date_range_this_week()
    generate_events_from_template(template, date_range)


def main():
    try:
        s = datetime.now()
        parser = argparse.ArgumentParser(prog='perfect-week-generator')
        parser.add_argument('--ls-cal', action='store_true',
                            help='List all the available calendars')
        parser.add_argument(
            '--frame', choices=['this-week', 'this-month', 'next-week', 'next-month'], help='Frame of the plan')
        parser.add_argument(
            '--template', type=argparse.FileType('r'), help='YAML file with plan')
        args = parser.parse_args()

        if args.ls_cal:
            service = get_calendar_service()
            calendars = service.calendarList().list().execute()
            for calendar in calendars['items']:
                print(f"Calendar: {calendar['summary']}, ID: {calendar['id']}")
        elif args.frame and args.template:
            frame = args.frame
            template = args.template
            stream = file(template.name, 'r')
            generate_from_template(stream, frame)
        else:
            print(
                "Invalid arguments. Please provide either --ls-cal or both --frame and --template.")

        e = datetime.now()
        print('Complete at: '+str((e-s) / 60))
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    main()
