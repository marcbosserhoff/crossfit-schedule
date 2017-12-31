#!/usr/bin/python

from ics import Calendar, Event
import argparse
import yaml
import sys
import datetime


def load_workouts():
    with open("workouts.yml", 'r') as stream:
        try:
            return yaml.load(stream)
        except yaml.YAMLError as exc:
            print("Error parsing yaml:")
            print(exc)
    return None


def parse_german_date(date_to_parse):
    try:
        return datetime.datetime.strptime(date_to_parse, "%d.%m.%Y")
    except ValueError as e:
        print "Error parsing date format: %s - Dateformat must be like 01.01.2018" % date_to_parse
        sys.exit(1)


def generate_weekly_workouts(workout_titles, start_workout, week_count, direction=1):
    """
    >>> workout_titles = ['a', 'b', 'c', 'd']
    >>> generate_weekly_workouts(workout_titles, 4, 0)
    Traceback (most recent call last):
        ...
    ValueError: startworkout value is greater that number of workouts
    >>> generate_weekly_workouts(workout_titles, 0, 0)
    ['a', 'b', 'c', 'd']
    >>> generate_weekly_workouts(workout_titles, 0, 1)
    ['b', 'c', 'd', 'a']
    >>> generate_weekly_workouts(workout_titles, 2, 0)
    ['c', 'd', 'a', 'b']
    """
    if start_workout > len(workout_titles) - 1:
        raise ValueError("startworkout value is greater that number of workouts")
    processed = len(workout_titles)
    pos = (start_workout + direction * week_count) % len(workout_titles)
    result = []
    while processed > 0:
        result += [workout_titles[pos]]
        pos = (pos + 1) % len(workout_titles)
        processed -= 1
    return result


def create_event(day, title, location):
    e = Event()
    e.name = title
    e.location = location
    e.begin = day.strftime("%y%m%d 00:00:00")
    e.make_all_day()
    return e


def create_title(workout):
    return "/".join(workout)


def get_week_of_year(date):
    return int(date.strftime("%V"))


def get_day_of_week(date):
    return int(date.strftime("%V"))


def calculate_calendar(workouts, start_workout, start_date, end_date):
    workout_titles = workout_title_array(workouts)
    week_count = 0
    one_day = datetime.timedelta(days=1)
    location = workouts["location"]
    c = Calendar()

    current_titles = generate_weekly_workouts(workout_titles, start_workout, week_count)
    current_date = start_date
    current_week_of_year = get_week_of_year(current_date)
    while current_date <= end_date:
        local_week_of_year = get_week_of_year(current_date)
        if local_week_of_year > current_week_of_year:
            current_week_of_year = local_week_of_year
            week_count += 1
            current_titles = generate_weekly_workouts(workout_titles, start_workout, week_count)

        e = create_event(current_date, current_titles[current_date.weekday()], location)
        c.events.append(e)
        current_date += one_day

    return c


def print_workouts(workouts):
    counter = 1
    for workout in workouts:
        print "%s: %s" % (counter, create_title(workout["contents"]))
        counter += 1


def workout_title_array(workouts):
    result = []
    for workout in workouts["workouts"]:
        result += [create_title(workout["contents"])]
    return result


def main():
    parser = argparse.ArgumentParser(description='Calculate crosssfit cologne workout calendar')
    parser.add_argument('startworkout', type=str, nargs='?',
                        help='Start plan with this workout number, show number with --list')
    parser.add_argument('startdate', type=str, nargs='?',
                        help='Start calendar at given date, dateformat is dd.mm.yyyy, example: 08.02.2018 is 8. of Febuary in '
                             '2018')
    parser.add_argument('enddate', type=str, nargs='?',
                        help='End calendar at given date, dateformat is dd.mm.yyyy, example: 08.02.2018 is 8. of Febuary in '
                             '2018')
    parser.add_argument('--list', dest='list', action='store_true',
                        help='List available workouts, do this first to have the number for startworkout')

    args = parser.parse_args()
    workouts = load_workouts()
    if args.list:
        print_workouts(workouts["workouts"])
        sys.exit(0)

    if not args.startworkout or not args.startdate or not args.enddate:
        parser.print_help()
        sys.exit(1)

    startdate = parse_german_date(args.startdate)
    enddate = parse_german_date(args.enddate)
    startworkout = int(args.startworkout)-1

    calendar = calculate_calendar(workouts, startworkout, startdate, enddate)
    open('crossfit.ics', 'w').writelines(calendar)


if __name__ == "__main__":
    main()
