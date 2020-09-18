from collections import Counter
from random import choice

# weekly_list = ['hayden','hayden','adeel','alex','owain']

weekly_list = []
rota_day = 'Wednesday'
it_names = ['hayden', 'alex', 'adeel', 'owain']

# print(it_names)
full_set = set(it_names)
# print(full_set)
schedule_exceptions = {
    'Monday': None,
    'Tuesday': 'owain',
    'Wednesday': None,
    'Thursday': None,
    'Friday': None
}


def max_shifts(remove_from, how_many):
    # Ensures that no IT Member is placed on more than 2 shifts a week
    # https://stackoverflow.com/questions/38599066/removing-some-of-the-duplicates-from-a-list-in-python
    counts = Counter()
    for item in remove_from:
        counts[item] += 1
        if counts[item] > how_many:
            weekly_list.remove(item)


def min_shifts(schedule_list, how_many):
    counts = Counter(schedule_list)
    most_common_name = [most_common_member for most_common_member, number in counts.most_common(1)]

    for member in it_names:
        if len(schedule_list) == 5 and member not in schedule_list:
            schedule_list.remove(most_common_name[0])

    if len(schedule_list) == 5:
        for most_common_member, number in counts.most_common():
            if number < how_many:
                schedule_list.remove(most_common_name[0])


def member_day_exclusion(member_to_exclude, day):
    member_to_exclude = member_to_exclude.lower()
    day = day.title()
    assigned_member = ''

    if day == 'Monday':
        assigned_member = weekly_list[0]
    elif day == 'Tuesday':
        assigned_member = weekly_list[1]
    elif day == 'Wednesday':
        assigned_member = weekly_list[2]
    elif day == 'Thursday':
        assigned_member = weekly_list[3]
    elif day == 'Friday':
        assigned_member = weekly_list[4]
    else:
        print('Day entered is incorrect. Please enter a day from the week_dict keys.')

    if assigned_member == member_to_exclude:
        weekly_list.remove(member_to_exclude)


def fill_schedule(day):
    # Fills the weekly_list schedule and calls the max_shifts function to ensure
    # that no IT Member is placed on more than 2 shifts a week
    if day == rota_day:
        while len(weekly_list) != 5:
            # n += 1
            # print(n)
            weekly_list.append(choice(it_names))
            print(weekly_list)
            # n += 1
            # print(n)
            max_shifts(weekly_list, 2)
            print(weekly_list)
            # n += 1
            # print(n)
            min_shifts(weekly_list, 1)
            print(weekly_list)
            # n += 1
            # print(f'{n} hello')
            # member_day_exclusion('owain','tuesday')


# set_of_weekly_list = set(weekly_list)
print(weekly_list)
# print(set_of_weekly_list)
fill_schedule('Wednesday')
print(weekly_list)
# print(set_of_weekly_list)
# print(full_set)