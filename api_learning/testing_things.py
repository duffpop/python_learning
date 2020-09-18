# # # creating a new dictionary
# # it_dict = {
# #     'hayden': '123',
# #     'adeel': '456',
# #     'alex': '789'
# # }
#
# it_dict = {
#     'hayden':'UEPH6G519',
#     'adeel': 'UEPH6G519',
#     'alex': 'UEPH6G519'
# }
#
# # clone_list = []
# #
# # # list out keys and values separately
# key_list = list(it_dict.keys())
# # # weekly_list.append(it_dict.values())
# weekly_list = list(it_dict.values())
# # clone_list.append(weekly_list)
# #
# print(weekly_list)
# print(key_list)
# print(key_list[key_list.index('hayden')])
# # print(key_list[weekly_list.index('adeel')])
# print(key_list)
#
# # test_list = []
# #
# # schedule_file = 'weekly_schedule.txt'
# #
# # with open(schedule_file) as file_object:
# #     lines = file_object.readlines()
# #     for line in lines:
# #         test_list.append(line.rstrip())
# #     print(test_list)
#
# # with open(schedule_file) as file_object:
# #     for name in test_list:
# #         test_list.append(name)
# #     print(test_list)
#
#

schedule_exceptions = {
    'Monday': None,
    'Tuesday': 'owain',
    'Wednesday': None,
    'Thursday': None,
    'Friday': None
}

weekly_list = ['hayden','hayden','adeel','alex','owain']

week_dict = {
    'Monday': weekly_list[0],
    'Tuesday': weekly_list[1],
    'Wednesday': weekly_list[2],
    'Thursday': weekly_list[3],
    'Friday': weekly_list[4]
}

for key, value in schedule_exceptions.items():
    if value is not None:
        day_off_member = f'[{key}, {value}]'

# for k, v in schedule_exceptions.items():

# def member_day_off(day, member):
#     """
#     week_dict exists with all of the filled schedule in
#     I'm saying that when the weekly_list is filled, if member_day_off(tuesday, owain)
#     then remove member's entry from the respective day in in weekly_list using member_day_off(day, member)
#     so what do I need?
#     I need to check weekly_list[1] (which is Tuesday), read the entry for weekly_list[1], comparing it against
#     the schedule_exceptions dict (maybe `schedule_expections['Tuesday']` ?)
#     for name in weekly_list:
#     if the name also matches the schedule_exceptions[day] value, weekly_list.remove[name]
#     """
#     day = day.title()
#     member = member.lower()
#
#     for key, value in schedule_exceptions:
#         if value is not None:
#             day_off_member = f'[{key},{value}]'
#
#
#         for k, v in week_dict:
#             if k and key == day:
#                 if v and value == member:
#                     weekly_list.remove(member)
#                 else:
#                     continue
#             else:
#                 continue


def member_day_exclusion(member, day):
    member = member.lower()
    day = day.title()

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
        print('Day entered is incorrect. Please enter a day from the week_dict.')

    print(f'\n{day}\nAssigned member: {assigned_member}\nMember excluded: {member}\n')

    if assigned_member == member:
        weekly_list.remove(assigned_member)


# print(day_off_member)
# print(week_dict['Tuesday'])
print(weekly_list)
member_day_exclusion('Owain','Tuesday')
print(weekly_list)