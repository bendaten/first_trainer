import argparse

from os.path import expanduser

import datetime

from first_data import FirstData
from first_plan import FirstPlan
from first_race import FirstRace
from first_runner import FirstRunner
from first_time import FirstTime

"""TODO: This program will run with command line args at first"""


def process_args():

    parser = argparse.ArgumentParser(description='FIRST Run Less Run Faster - generate training plans.',
                                     epilog='')

    parser.add_argument('-r', '--runner_name', default='John Doe', help='Runner\'s name')
    parser.add_argument('-k', '--keyrun_days', default='mon wed sat',
                        help='Select 3 week days from [mon, tue, wed, thu, fri, sat, sun]')
    parser.add_argument('-t', '--target_time', help='Target time in "H:MM:SS"', required=True)
    parser.add_argument('-e', '--ref_race_type', default=None,
                        help='Reference race type to calculate target time. Default is the same as race type')
    parser.add_argument('-y', '--race_type', default='Marathon',
                        help='One of 5K, 10K, HalfMarathon, Marathon. Default is Marathon')
    parser.add_argument('-n', '--race_name', default='My Race', help='Race name. Default is the race type')
    parser.add_argument('-d', '--race_date', help='Race date - MM/DD/YYYY', required=True)
    parser.add_argument('-o', '--output', default='both', help='One of "text", "tcx", or "both"')

    return parser.parse_args()


def get_keyrun_days(user_string):

    days = user_string.split()
    if len(days) != 3:
        raise ValueError('3 days expected')
    week = {'mon': 0, 'tue': 1, 'wed': 2, 'thu': 3, 'fri': 4, 'sat': 5, 'sun': 6}
    keyrun_days = []
    for day in days:
        day_low = day.lower()
        if day_low not in week:
            raise ValueError('days must be in [mon, tue, wed, thu, fri, sat, sun]')
        day_num = week[day_low]
        if day_num in keyrun_days:
            raise ValueError('3 different days are expected')
        keyrun_days.append(day_num)

    return keyrun_days


def main():

    args = process_args()

    if args.output not in ['text', 'tcx', 'both']:
        raise ValueError('output should be one of "text", "tcx", or "both"')

    data_file_path = expanduser('~') + '/PycharmProjects/first/database/FIRSTregularPlans.xml'
    data = FirstData(xml_path=data_file_path)

    runner = FirstRunner(name=args.runner_name)

    target_time = FirstTime.from_string(args.target_time)
    if args.ref_race_type is not None:
        target_time = data.equivalent_time(time_from=target_time,
                                           race_index_from=data.race_type_index_by_name(args.ref_race_type),
                                           race_index_to=data.race_type_index_by_name(args.race_type))
    if args.race_name is not None:
        race_name = args.race_name
    else:
        race_name = args.race_type

    race_date = datetime.datetime.strptime(args.race_date, '%m/%d/%Y').date()
    race = FirstRace(race_type=data.get_race_type_by_name(args.race_type),
                     name=race_name, race_date=race_date, target_time=target_time)
    ws = get_keyrun_days(args.keyrun_days)

    plan = FirstPlan(name=args.race_name, weekly_schedule=ws, race=race, runner=runner)
    plan.generate_workouts(data=data)

    base_file_name = str(race_date) + race_name
    if args.output == 'text' or args.output == 'both':
        file_name = expanduser('~/Downloads/') + base_file_name + '.txt'
        target = open(file_name, 'w')
        target.write(plan.details(level=3))
        target.close()

    if args.output == 'tcx' or args.output == 'both':
        file_name = expanduser('~/Downloads/') + base_file_name + '.tcx'
        target = open(file_name, 'w')
        target.write(plan.tcx())
        target.close()


# ----------------------------------------------------------
if __name__ == '__main__':
    main()
