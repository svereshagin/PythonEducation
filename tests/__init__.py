# def track_test_result(module, test_n, quest, result, filename):
#     def decorator(func):
#         @functools.wraps(func)
#         def wrapper(*args, **kwargs):
#             result_value = func(*args, **kwargs)
#             date = datetime.datetime.now()
#             with open(file.path.joinpath('secret_key.json'), 'r') as secret_key:
#                 data = json.load(secret_key)
#                 print(data)
#                 if data[module][test_n] is None and result_value:
#                     file.change_test_result(module=module, test_n=test_n)
#                     log.insert_quest_data(
#                         quest=quest,
#                         filename=filename,
#                         result=result,
#                         time=date,
#                         time_mod='first_quest_final_time'
#                     )
#                 else:
#                     log.insert_quest_data(
#                         quest=quest,
#                         filename=filename,
#                         result=0,
#                         time=date,
#                         time_mod='first_quest_start_time'
#                     )
#             return result_value  # Возврат результата
#         return wrapper
#     return decorator