# # creating a new dictionary
# it_dict = {
#     'hayden': '123',
#     'adeel': '456',
#     'alex': '789'
# }

it_dict = {
    'hayden':'UEPH6G519',
    'adeel': 'UEPH6G519',
    'alex': 'UEPH6G519'
}

# clone_list = []
#
# # list out keys and values separately
key_list = list(it_dict.keys())
# # weekly_list.append(it_dict.values())
weekly_list = list(it_dict.values())
# clone_list.append(weekly_list)
#
print(weekly_list)
print(key_list)
print(key_list[key_list.index('hayden')])
# print(key_list[weekly_list.index('adeel')])
print(key_list)

# test_list = []
#
# schedule_file = 'weekly_schedule.txt'
#
# with open(schedule_file) as file_object:
#     lines = file_object.readlines()
#     for line in lines:
#         test_list.append(line.rstrip())
#     print(test_list)

# with open(schedule_file) as file_object:
#     for name in test_list:
#         test_list.append(name)
#     print(test_list)

