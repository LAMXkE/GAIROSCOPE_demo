import matplotlib.pyplot as plt
import csv
import json
import os

if not os.path.exists('./magnitude.csv'):
    os.system('adb pull /sdcard/Android/Data/com.example.gyroscope/files/magnitude.csv')

f = open('./magnitude.csv', 'r')
t = open('./timetable', 'r')

hz_values = []
x_values = []
y_values = []
time_to_hz = {}

with t:
    time_to_hz = json.loads(t.read())

with f:
    reader = csv.reader(f)
    current_timestamp = 0
    x_sum = 0
    y_sum = 0
    cnt = 0
    first = True
    next(reader) # skip the header row if present
    for row in reader:
        if row[0] == current_timestamp or first :
            x_sum += float(row[1])
            y_sum += float(row[2])
            cnt += 1
            first = False
        else:
            try:
                hz_values.append(time_to_hz[row[0]])
                #hz_values.append(int(row[0]))
            except KeyError:
                continue
            x_values.append(x_sum/cnt)
            y_values.append(y_sum/cnt)
            x_sum = 0
            y_sum = 0
            cnt = 0

        current_timestamp = row[0]
            
        # x_values.append(float(row[1]))
        # y_values.append(float(row[2]))

# Plot the first graph x-axis magnitude per Hz
plt.figure(1)
plt.plot(hz_values, x_values)
plt.xlabel('hz')
plt.ylabel('X-axis magnitude')
plt.title('X-axis magnitude according to hz')

# Plot the second graph y-axis magnitude per Hz
plt.figure(2)
plt.plot(hz_values, y_values)
plt.xlabel('hz')
plt.ylabel('Y-axis magnitude')
plt.title('Y-axis magnitude according to hz')

# Show the plots
plt.show()

