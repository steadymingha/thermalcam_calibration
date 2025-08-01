import csv
import matplotlib.pyplot as plt

device_temps = []
pixel_avgs = []
temp_avgs = []

root_dir = "./"
with open(root_dir+"output.csv", newline='') as f:
    reader = csv.reader(f)
    next(reader)  # skip header

    for row in reader:
        if not row: continue
        device_temps.append(float(row[1]))
        pixels = list(map(int, row[2:11]))
        temps = list(map(float, row[11:20]))
        pixel_avgs.append(sum(pixels) / len(pixels))
        temp_avgs.append(sum(temps) / len(temps))

x = list(range(len(device_temps)))  # timestamp 대신 인덱스 사용

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True)

# subplot 1: pixel avg
ax1.plot(x, pixel_avgs, marker='o')
ax1.set_ylabel("Pixel Value")
ax1.set_title("Average Pixel Value")
ax1.grid(True) 

# subplot 2: temp avg + device temp
ax2.plot(x, temp_avgs, marker='o', label="Avg Pixel Temp (°C)")
ax2.plot(x, device_temps, marker='x', label="Device Temp (°C)")
ax2.set_ylabel("Temperature (°C)")
ax2.set_xlabel("time line")
ax2.set_title("Temperature Over Time")
ax2.legend()

plt.tight_layout()
plt.grid(True)
plt.show()
