import datetime
import time
import csv
import re
import string
import sys

def weekdayinterpratation(day_info, weekday):
	if '-' in day_info:
		posi = day_info.find('-')
		start = day_info[:posi]
		end = day_info[posi+1:]	
		if start == 'M':
			if end == 'F':
				return weekday <= 4
			elif end == 'SAT':
				return weekday <= 5
			elif end == 'SUN':
				return 1
			else:
				print ('error in function weekdayinterpratation1')
				sys.exit()
	else:
		if day_info == 'F':
			return weekday == 4
		elif day_info == 'SAT':
			return weekday == 5
		elif day_info == 'SUN':
			return weekday == 6
		else:
			return (1)

def intervalinterpratation(interval, time):
	mid_position = interval.find('-')
	start = interval[:mid_position]
	end = interval[mid_position+1:]
	start_hour_position = start.find(':')
	start_hour =  start[:start_hour_position]
	start_minu =  start[start_hour_position+1:]
	start_to_compare = int(start_hour) * 60 + int(start_minu)
	end_hour_position = end.find(':')
	end_hour = end[:end_hour_position]
	end_minu = end[end_hour_position+1:]
	end_to_compare = int(end_hour) * 60 + int(end_minu)
	time_hour_posi = time.find(':')
	time_hour = time[:time_hour_posi]
	time_minu = time[time_hour_posi+1:]
	time_to_compare = int(time_hour) * 60 + int(time_minu)
	result = []
	if time_to_compare >= start_to_compare and time_to_compare < end_to_compare:
		return (end_to_compare - time_to_compare, end, time_to_compare)
	else:
		return (0, '', 0)

def match_lat_long(bay):
	with open('la_long.csv', 'r') as f:
		reader = csv.reader(f)
		lat_long_row = list(reader)
	bay_row = 0
	for i in range(1, len(lat_long_row)):
		tab_position = lat_long_row[i][0].find('\t')
		bayid = lat_long_row[i][0][:tab_position]
		if len(bayid) > 3:
			bayid = bayid[:len(bayid)-3] + ',' + bayid[len(bayid)-3:]
		if bay == bayid:
			bay_row = i
			break
	if bay_row == 0:
		return (' ', ' ')
	lat_position = lat_long_row[bay_row][0].find('(') 
	lat = lat_long_row[bay_row][0][lat_position+1:]
	long_position = lat_long_row[bay_row][1].find(')')
	lon = lat_long_row[bay_row][1][:long_position]
	return (lat, lon)


bay = input('what\'s your bayid:	')
if len(bay) > 3:
	bay = bay[:len(bay)-3] + ',' + bay[len(bay)-3:]

time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
time = time[len(time) - 8: len(time) - 3]
weekday = datetime.datetime.today().weekday() #Monday as 0 and Sunday as 6

with open('bay_info.csv', 'r') as f:
	reader = csv.reader(f)
	csv_row = list(reader)

bay_num = ''
row = 0
for i in range(1,len(csv_row)):
	temp = csv_row[i][0].find('\t')
	bay_num = csv_row[i][0][0:temp]
	if bay_num == bay:
		row = i
		break

if row == 0:
	print ('Sorry, the bayid does not exist.')
	sys.exit()

tab_list = [m.start() for m in re.finditer('\t', csv_row[row][0])]
dur_index = []
for i in range(1, min(10, len(tab_list)-2)):
	if csv_row[row][0][tab_list[i]+1] >= '1' and csv_row[row][0][tab_list[i]+1] <= '9' and csv_row[row][0][tab_list[i]+2] == 'P':
		dur_index.append(tab_list[i] + 1)
		max = i
dur_index.append(tab_list[max+1] + 1)

sub_dur = []
for i in range(0, len(dur_index)-1):
	sub_dur.append(csv_row[row][0][dur_index[i]:dur_index[i+1]-1])

info_slice = []
flag = 0
for i in range(0, len(sub_dur)):
	info_slice = sub_dur[i].split()
	day_info = info_slice[len(info_slice) - 2]
	if not weekdayinterpratation(day_info, weekday):
		continue
	interval = info_slice[len(info_slice) - 1]
	available_minuts, end, now = intervalinterpratation(interval, time)
	if available_minuts == 0:
		continue
	minuts = int(sub_dur[i][0])* 60
	end_time_2 = minuts + now
	park_end_min = end_time_2 % 60
	part_end_hour = end_time_2 / 60
	if available_minuts <= minuts:
		print ('You can park here (bayid: %s) for %d minuts until %s' %(bay,available_minuts,end))
		print (sub_dur[i])
		if 'DIS' in sub_dur[i]:
			print ('Note: This bay is disabled only.')
		flag = 1
		break
	else:
		print ('You can park here (bayid: %s) for %d minuts until %d:%d' %(bay, minuts, part_end_hour, park_end_min))
		print (sub_dur[i])
		if 'DIS' in sub_dur[i]:
			print ('Note: This bay is disabled only.')
		flag = 1
		break
lat, lon = match_lat_long(bay)
if lat == ' ':
	print ('Sorry, the latitude and longitude infomation are not found.')
else:
	print ('The latitude and longitude of the bay are: (%s,%s)' %(lat, lon))


if flag == 0:
	print ('Parking at bay: %s is not available right now.' %(bay))