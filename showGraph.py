import matplotlib.pyplot as plt
import csv
import json

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
    next(reader) # skip the header row if present
    for row in reader:
        try:
            hz_values.append(time_to_hz[row[0]])
        except KeyError:
            continue

        x_values.append(float(row[1]))
        y_values.append(float(row[2]))

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

