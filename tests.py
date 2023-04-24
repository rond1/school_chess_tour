import datetime

from requests import get, post, put, delete

from salt import salt

# data = {
#     'name': '10Б',
#     'salt': salt
# }
# print(post(f'http://localhost:5000/api/group/', json=data).json())

# data = {
#     'fio': 'Саша Корепанова',
#     'email': 'sashka@kakashka',
#     'hashed_password': 'pbkdf2:sha256:260000$8QNQL7EEBqPJJ5o1$f003af919097bba8d0377a4e0fe0a14bcb4d771539acd29ddf6c17c46ded9c20',
#     'is_female': 1,
#     'group_id': 2,
#     'is_activated': True,
#     'salt': salt
# }
# print(put(f'http://localhost:5000/api/user/2', json=data).json())

# data = {
#     'name': '11В',
#     'salt': salt
# }
# print(put(f'http://localhost:5000/api/group/2', json=data).json())

# m_sname = ['Айтматов', 'Булгаков', 'Грибоедов', 'Достоевский', 'Лермонтов', 'Маяковский', 'Пушкин',
#            'Симонов', 'Твардовский']
# m_name = ['Александр', 'Богдан', 'Виктор', 'Евгений', 'Камиль', 'Мирослав', 'Олег', 'Руслан']
# m_mname = ['Александрович', 'Богданович', 'Викторович', 'Евгеньевич', 'Камилевич', 'Мирославович',
#            'Олегович', 'Русланович']
# f_sname = ['Айтматова', 'Булгакова', 'Грибоедова', 'Достоевская', 'Лермонтова', 'Маяковская',
#            'Пушкина', 'Симонова', 'Твардовская']
# f_name = ['Александра', 'Богдана', 'Виктория', 'Евгения', 'Камила', 'Мирослава', 'Ольга', 'Руслана']
# f_mname = ['Александровна', 'Богдановна', 'Викторовна', 'Евгеньевна', 'Камилевна', 'Мирославовна', 'Олеговна',
#            'Руслановна']
# first_letter_sname = ['a', 'b', 'g', 'd', 'l', 'm', 'p', 's', 't']
# first_letter_name = ['a', 'b', 'v', 'e', 'k', 'm', 'o', 'r']
# groups = []
# count = 0
# for i in range(1, 12):
#     for letter in ['А', 'Б', 'В', 'Г']:
#         post(f'http://localhost:5000/api/group/', json={'name': str(i) + letter, 'salt': salt})
#         count += 1
#         groups.append(count)
# post(f'http://localhost:5000/api/group/', json={'name': 'левые', 'salt': salt})
# post(f'http://localhost:5000/api/group/', json={'name': 'выпускники', 'salt': salt})
#
# group_id = 1
# user_id = 1
# for sname in range(9):
# 	for name in range(8):
# 		for mname in range(8):
# 			fio = f'{m_sname[sname]} {m_name[name]} {m_mname[mname]}'
# 			password = first_letter_sname[sname] + first_letter_name[name] + first_letter_name[mname]
# 			post(f'http://localhost:5000/api/user/',
# 				 json={'fio': fio, 'is_female': False, 'password': f'm{password}', 'email': f'm{password}@example.ru',
# 					   'salt': salt})
# 			user_id += 1
# 			put(f'http://localhost:5000/api/user/{user_id}',
# 				 json={'fio': fio, 'is_female': False, 'password': f'm{password}', 'email': f'm{password}@example.ru',
# 					   'salt': salt, 'is_activated': True, 'group_id': group_id})
# 			group_id += 1
# 			fio = f'{f_sname[sname]} {f_name[name]} {f_mname[mname]}'
# 			post(f'http://localhost:5000/api/user/',
# 				 json={'fio': fio, 'is_female': True, 'password': f'f{password}', 'email': f'f{password}@example.ru',
# 					   'salt': salt})
# 			user_id += 1
# 			put(f'http://localhost:5000/api/user/{user_id}',
# 				 json={'fio': fio, 'is_female': True, 'password': f'f{password}', 'email': f'f{password}@example.ru',
# 					   'salt': salt, 'is_activated': True, 'group_id': group_id})
# 			group_id = (group_id + 1) % 46

# put(f'http://localhost:5000/api/group/2', json={'id': 3, 'salt': salt})

# print(post(f'http://localhost:5000/api/tour/', json={'category_id': 1, 'start': '2023-05-01T15:00', 'salt': salt}).json())
# print(put(f'http://localhost:5000/api/category/1', json={'name': 'Мальчики', 'salt': salt}).json())
# delete(f'http://localhost:5000/api/tournament/1')
# print(post(f'http://localhost:5000/api/tournament/', json={'name': 'Весенний турнир', 'game_time': 10, 'move_time': 5,
#         №                                              'start': '2023-05-01T15:00', 'salt': salt}).json())
# print((post(f'http://localhost:5000/api/category/', json={'name': 'Девочки', 'gender': 1, 'tournament_id': 1,
#                                                           'salt': salt})))
# # print((get(f'http://localhost:5000/api/group/1')))
# print(put(f'http://localhost:5000/api/game/2', json={'result': 1, 'salt': salt}).json())
# print((get(f'http://localhost:5000/api/user/3')))
print((get(f'http://localhost:5000/api/game/1')))
