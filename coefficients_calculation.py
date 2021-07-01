import csv


"""
    Функция чтения CSV файла
"""
def csv_reader(file_obj):
    reader = csv.reader(file_obj)
    rows_processing(reader)
    
"""
    Функция обработки строк таблицы
"""
def rows_processing(reader):
    
    experiments_count = 3

    average_user_time_std = 0
    average_system_time_std = 0
    average_elapsed_time_std = 0

    average_user_time_tc = 0
    average_system_time_tc = 0
    average_elapsed_time_tc = 0

    count_std = 0
    count_tc = 0

    average_user_time_array_std = []
    average_system_time_array_std = []
    average_elapsed_time_array_std = []

    average_user_time_array_tc = []
    average_system_time_array_tc = []
    average_elapsed_time_array_tc = []

    urls = []
    
    for row in reader:
        while '' in row:
            row.remove('')
        if row[0] == "Url":
            continue
        if row[0][0] == 'h':
            for i in range(1, 7):
                row.pop(1)
            urls.append(row[0])
            row.pop(0)

        if row[0][0] == 's':
            average_user_time_std += float(row[1])
            average_system_time_std += float(row[2])
            average_elapsed_time_std += time_to_sec(row[4])
    
            count_std += 1
            count_tc = 0
        else:
            average_user_time_tc += float(row[1])
            average_system_time_tc += float(row[2])
            average_elapsed_time_tc += time_to_sec(row[4])

            count_tc += 1
            count_std = 0

        if count_std == experiments_count: 
            average_user_time_std = average_user_time_std / experiments_count
            average_system_time_std = average_system_time_std / experiments_count
            average_elapsed_time_std = average_elapsed_time_std / experiments_count
            average_user_time_array_std.append(average_user_time_std)
            average_system_time_array_std.append(average_system_time_std)
            average_elapsed_time_array_std.append(average_elapsed_time_std)
            average_user_time_std = 0
            average_system_time_std = 0

        if count_tc == experiments_count:
            average_user_time_tc = average_user_time_tc / experiments_count
            average_system_time_tc = average_system_time_tc / experiments_count
            average_elapsed_time_tc = average_elapsed_time_tc / experiments_count
            average_user_time_array_tc.append(average_user_time_tc)
            average_system_time_array_tc.append(average_system_time_tc)
            average_elapsed_time_array_tc.append(average_elapsed_time_tc)
            average_user_time_tc = 0
            average_system_time_tc = 0

    calculate_coefficientes(urls, average_user_time_array_std, average_user_time_array_tc, 
                                  average_system_time_array_std, average_system_time_array_tc,
                                  average_elapsed_time_array_std, average_elapsed_time_array_tc,)

"""
    Функция конвертирования формата hh:mm:ss или mm:ss в секунды
"""
def time_to_sec(nc_time):
    sec_in_min = 60
    sec_in_h = 3600
    result = 0
    if nc_time.count(':') == 1:
        time_array = nc_time.split(':')
        result += float(time_array[0]) * sec_in_min
        result += float(time_array[1])
    else:
        time_array = nc_time.split(':')
        result += float(time_array[0]) * sec_in_h
        result += float(time_array[1]) * sec_in_min
        result += float(time_array[2])

    return result


"""
    Функция расчета коэффициентов
"""
def calculate_coefficientes(urls, average_user_time_array_std, average_user_time_array_tc, 
                                  average_system_time_array_std, average_system_time_array_tc,
                                  average_elapsed_time_array_std, average_elapsed_time_array_tc,):

    coefficientes_user_time = {}
    coefficientes_system_time = {}
    coefficientes_elapsed_time = {}

    list_user_time = []
    list_system_time = []
    list_elapsed_time = []
    
    for i in range(len(urls)):
        coefficientes_user_time[urls[i]]=average_user_time_array_std[i] / average_user_time_array_tc[i]
        coefficientes_system_time[urls[i]]=average_system_time_array_std[i] / average_system_time_array_tc[i]
        coefficientes_elapsed_time[urls[i]]=average_elapsed_time_array_std[i] / average_elapsed_time_array_tc[i]
   
    list_user_time = list(coefficientes_user_time.items())
    list_system_time = list(coefficientes_system_time.items())
    list_elapsed_time = list(coefficientes_elapsed_time.items())


    list_user_time.sort(key=lambda k: k[1])
    list_system_time.sort(key=lambda k: k[1])
    list_elapsed_time.sort(key=lambda k: k[1])

    prepare_outputs(list_user_time, list_system_time, list_elapsed_time)

"""
    Подготовка результатов к выводу
"""
def prepare_outputs(list_user_time, list_system_time, list_elapsed_time):

    output_count = 30

    if len(list_user_time) < output_count:
        count = len(list_user_time)
    else:
        count = output_count

    print("\nUser Time\n")
    print_result(output_count, list_user_time, list(reversed(list_user_time)))
    print("\nSystem Time\n")
    print_result(output_count, list_system_time, list(reversed(list_elapsed_time)))
    print("\nElapsed Time\n")
    print_result(output_count, list_elapsed_time, list(reversed(list_elapsed_time)))
   
"""
    Вывод результата в консоль
"""
def print_result(output_count, best_results, bad_results):
    print(output_count, " best results")
    for i in range(0, output_count):
        print(bad_results[i][0], ':', bad_results[i][1])
    print(output_count, " bad results")
    for i in range(0, output_count):
        print(best_results[i][0], ':', best_results[i][1])
    

if __name__ == "__main__":
    csv_path = "Results.csv"
    with open(csv_path, "r") as f_obj:
        csv_reader(f_obj)
