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

    file_info = []

    
    for row in reader:
        while '' in row:
            row.remove('')
        if row[0] == "Url":
            continue
        if row[0][0] == 'h':
            print(row[0] + "\n")
            file_info.append(row[0] + ", " + row[1] + ", " + row[2] + ", " + row[3] + ", " + row[4].split(" pixels")[0] + "x" + row[5].split(" pixels")[0] + ", " + row[6])
            for i in range(0, 7):
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
            print(str(average_elapsed_time_std) + "\n") 
            average_user_time_std = average_user_time_std / experiments_count
            average_system_time_std = average_system_time_std / experiments_count
            average_elapsed_time_std = average_elapsed_time_std / experiments_count
            average_user_time_array_std.append(average_user_time_std)
            average_system_time_array_std.append(average_system_time_std)
            average_elapsed_time_array_std.append(average_elapsed_time_std)
            average_user_time_std = 0
            average_system_time_std = 0
            average_elapsed_time_std = 0

        if count_tc == experiments_count:
            average_user_time_tc = average_user_time_tc / experiments_count
            average_system_time_tc = average_system_time_tc / experiments_count
            average_elapsed_time_tc = average_elapsed_time_tc / experiments_count
            average_user_time_array_tc.append(average_user_time_tc)
            average_system_time_array_tc.append(average_system_time_tc)
            average_elapsed_time_array_tc.append(average_elapsed_time_tc)
            average_user_time_tc = 0
            average_system_time_tc = 0
            average_elapsed_time_tc = 0


    calculate_coefficientes(file_info,
                            average_user_time_array_std, average_user_time_array_tc, 
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
def calculate_coefficientes(file_info,
                            average_user_time_array_std, average_user_time_array_tc, 
                            average_system_time_array_std, average_system_time_array_tc,
                            average_elapsed_time_array_std, average_elapsed_time_array_tc,):

    coefficientes_user_time = {}
    coefficientes_system_time = {}
    coefficientes_elapsed_time = {}

    list_user_time = []
    list_system_time = []
    list_elapsed_time = []
    
    for i in range(len(file_info)):
        coefficientes_user_time[file_info[i]]=average_user_time_array_std[i] / average_user_time_array_tc[i]
        coefficientes_system_time[file_info[i]]=average_system_time_array_std[i] / average_system_time_array_tc[i]
        coefficientes_elapsed_time[file_info[i]]=average_elapsed_time_array_std[i] / average_elapsed_time_array_tc[i]
   
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

    f = open('best_bad_results_info.txt', 'a')

    print("\nUser Time\n")
    f.write("----------USER TIME----------\n")
    print_result(f, output_count, list_user_time, list(reversed(list_user_time)))
    print("\nSystem Time\n")
    f.write("----------SYSTEM TIME----------\n")
    print_result(f, output_count, list_system_time, list(reversed(list_elapsed_time)))
    print("\nElapsed Time\n")
    f.write("----------ELAPSED TIME----------\n")
    print_result(f, output_count, list_elapsed_time, list(reversed(list_elapsed_time)))
   
"""
    Вывод результата в консоль
"""
def print_result(f, output_count, best_results, bad_results):
    print(output_count, " best results")
    f.write("----------Best results----------\n\n")
    for i in range(0, output_count):
        save_results(f, bad_results[i])
        print(bad_results[i][0], ':', bad_results[i][1])
    print(output_count, " bad results")
    f.write("----------Bad results----------\n\n")
    for i in range(0, output_count):
        save_results(f, best_results[i])
        print(best_results[i][0], ':', best_results[i][1])

"""
    Запись результатов в файл
"""
def save_results(f, results):
    file_info = results[0].split(',')
    f.write("URL:" + file_info[0] + "\n")
    f.write("Codec:" + file_info[1] + "\n")
    f.write("Duration:" + file_info[2] + "\n")
    f.write("Bit_rate:" + file_info[3] + "\n")
    f.write("Resolution:" + file_info[4] + "\n")
    f.write("FPS:" + file_info[5] + "\n")
    f.write("Result: " + str(results[1]) + "\n\n")

if __name__ == "__main__":
    csv_path = "Results.csv"
    with open(csv_path, "r") as f_obj:
        csv_reader(f_obj)
