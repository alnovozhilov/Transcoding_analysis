import matplotlib.pyplot as plt
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


user_time = []
system_time = []
elapsed_time = []

with open("./Parsed_results/release_results.txt", "r") as file:
	print("./Release_results/Chimera_DCI4k2398p_HDR_P3PQ.mp4_tc\n")
	for line in file:
		if (line[0] == "." or line == "end\n") and not user_time == []:
			print("Standard deviation tc_malloc (user time): ", np.std(user_time))
			print("Standard deviation tc_malloc (System time): ", np.std(system_time))
			print("Standard deviation tc_malloc (elapsed time): ", np.std(elapsed_time))
			user_time = []
			system_time = []
			elapsed_time = []
			if not line == "end\n":
				print("\n", line)
		if line == "tc_malloc\n":
			print("Standard deviation std (user time): ", np.std(user_time))
			print("Standard deviation std (System time): ", np.std(system_time))
			print("Standard deviation std (elapsed time): ", np.std(elapsed_time))
			user_time = []
			system_time = []
			elapsed_time = []
		if line[0] == 'U':
			user_time.append(float(line.replace("User time (seconds): ", "")))
		if line[0] == 'S':
			system_time.append(float(line.replace("System time (seconds): ", "")))
		if line[0] == 'E':
			elapsed_time.append(time_to_sec(line.replace("Elapsed (wall clock) time (h:mm:ss or m:ss): ", "")))