import calendar
from datetime import datetime, timedelta, date
from io import open as file

import pytz
import yaml
from yaml import Loader

from cal_setup import get_calendar_service

TIME_ZONE_NAME = 'Europe/Warsaw'
time_zone = pytz.timezone(TIME_ZONE_NAME)
CALENDAR_ID = '1l5manvl5d049idjb0dg5ilujo'
CURRENT_M = 12
CURRENT_Y = 2023


def create_single_event(name, dtstart, dtend, description):
    event = {
        'summary': name,
        'description': description,
        'start': {
            'dateTime': dtstart.strftime('%Y-%m-%dT%H:%M:00'),
            'timeZone': TIME_ZONE_NAME
        },
        'end': {
            'dateTime': dtend.strftime('%Y-%m-%dT%H:%M:00'),
            'timeZone': TIME_ZONE_NAME
        },
        'reminders': {
            'useDefault': False,
        },
        'transparency': "transparent",
    }
    return event


def create_all_day_event(name, d, description):
    event = {
        'summary': name,
        'description': description,
        'start': {
            'date': d.strftime('%Y-%m-%d'),
        },
        'end': {
            'date': d.strftime('%Y-%m-%d'),
        },
        'reminders': {
            'useDefault': False,
        },
        'transparency': "transparent",
    }
    return event


def insert_events_calendar(events):
    service = get_calendar_service()
    print('Events to insert: ' + str(len(events)))
    s = datetime.now()
    for event in events:
        print('Event to insert is: '+event['summary'])
        service.events().insert(calendarId= CALENDAR_ID + '@group.calendar.google.com', body=event).execute()
    e = datetime.now()
    print('Complete at: '+str((e-s) / 60))


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


def generate_all_day_events(stream):
    events = []
    plan = yaml.load(stream, Loader)
    for item in plan['entries']:
        should_be_business_day = item['business_day']
        d = date(CURRENT_Y, CURRENT_M, int(item['date']))
        if is_weekend(d) and should_be_business_day is True:
            d = get_business_day_before_weekend(d)
        description = ''
        if 'description' in item:
            description = item['description']
        events.append(create_all_day_event(item['name'], d, description))
    return events


def generate_single_events(stream, day_range):
    events = []
    plan = yaml.load(stream, Loader)
    for d in day_range:
        for item in plan['entries']:
            description = ''
            if 'description' in item:
                description = item['description']
            parsed_string = str(item['startAt']).split("-")
            start_hour = int(parsed_string[0])
            start_minute = 0 if len(parsed_string) == 1 else int(parsed_string[1])
            start = datetime(d.year, d.month, d.day, start_hour, start_minute, 0, tzinfo=time_zone)
            end = start + timedelta(minutes=item['duration'])
            events.append(create_single_event(item['name'], start, end, description))
    return events


def generate_b_days():
    print('generate b-days')


def main():
    events = []
    num_days = calendar.monthrange(CURRENT_Y, CURRENT_M)[1]
    days = [date(CURRENT_Y, CURRENT_M, day) for day in range(1, num_days + 1)]
    # 1. get range of all business and generate all events from business_day_plan.yaml
    business_day_plan = generate_single_events(stream=file('week_plan.yaml', 'r'),
                                               day_range=filter(lambda d: is_business_day(d), days))

    # 3. Generate events for month from month_plan.yaml
    month_plan = generate_all_day_events(stream=file('month_plan.yaml', 'r'))
    print('Generating events')
    # 4. b-days events is TBD, will be generated once a year!
    # 5. Insert all to the calendar
    print('Insert events to calendar')
    insert_events_calendar(events=business_day_plan)
    print('Done!')


if __name__ == '__main__':
    main()
