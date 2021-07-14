import numpy as np

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


std_user_time = []
std_system_time = []
std_elapsed_time = []

tc_user_time = []
tc_system_time = []
tc_elapsed_time = []

std_flag = True

with open("./Parsed_results/release_results.txt", "r") as file:
	print("./Release_results/Chimera_DCI4k2398p_HDR_P3PQ.mp4_tc\n")
	for line in file:
		if (line[0] == "." or line == "end\n") and not tc_user_time == []:
			print("AVERAGE tc_malloc (user time): ", np.average(tc_user_time))
			print("AVERAGE tc_malloc (System time): ", np.average(tc_system_time))
			print("AVERAGE tc_malloc (elapsed time): ", np.average(tc_elapsed_time))
			print("STDEV tc_malloc (user time): ", np.std(tc_user_time))
			print("STDEV tc_malloc (System time): ", np.std(tc_system_time))
			print("STDEV tc_malloc (elapsed time): ", np.std(tc_elapsed_time))
			print("Соотношение AVERAGE std/tc (user time): ", np.average(std_user_time) / np.average(tc_user_time))
			print("Соотношение AVERAGE std/tc (system time): ", np.average(std_system_time) / np.average(tc_system_time))
			print("Соотношение AVERAGE std/tc (elapsed time): ", np.average(std_elapsed_time) / np.average(tc_elapsed_time))
			std_user_time = []
			std_system_time = []
			std_elapsed_time = []
			if not line == "end\n":
				print("\n", line)
		if line == "std\n":
			std_flag = True
		if line == "tc_malloc\n":
			std_flag = False
			print("AVERAGE std (user time): ", np.average(std_user_time))
			print("AVERAGE std (System time): ", np.average(std_system_time))
			print("AVERAGE std (elapsed time): ", np.average(std_elapsed_time))
			print("STDEV std (user time): ", np.std(std_user_time))
			print("STDEV std (System time): ", np.std(std_system_time))
			print("STDEV std (elapsed time): ", np.std(std_elapsed_time))
			tc_user_time = []
			tc_system_time = []
			tc_elapsed_time = []
		if line[0] == 'U':
			if std_flag == True:
				std_user_time.append(float(line.replace("User time (seconds): ", "")))
			else:
				tc_user_time.append(float(line.replace("User time (seconds): ", "")))
		if line[0] == 'S':
			if std_flag == True:
				std_system_time.append(float(line.replace("System time (seconds): ", "")))
			else:
				tc_system_time.append(float(line.replace("System time (seconds): ", "")))
		if line[0] == 'E':
			if std_flag == True:
				std_elapsed_time.append(time_to_sec(line.replace("Elapsed (wall clock) time (h:mm:ss or m:ss): ", "")))
			else:
				tc_elapsed_time.append(time_to_sec(line.replace("Elapsed (wall clock) time (h:mm:ss or m:ss): ", "")))