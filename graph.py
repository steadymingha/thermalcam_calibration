import csv
import matplotlib.pyplot as plt

device_temps = []
pixel_avgs = []
temp_avgs = []
pixel_all = [[] for _ in range(9)]

root_dir = './'

with open(root_dir+"/output.csv", newline='') as f:
    reader = csv.reader(f)
    next(reader)  # skip header

    for row in reader:
        if not row: continue
        device_temps.append(float(row[1]))
        pixels = list(map(int, row[2:11]))
        temps = list(map(float, row[11:20]))
        pixel_avgs.append(sum(pixels) / len(pixels))
        temp_avgs.append(sum(temps) / len(temps))
        for i in range(9):
            pixel_all[i].append(pixels[i])

x = list(range(len(device_temps)))

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 8), sharex=True)

# subplot 1: pixel avg
ax1.plot(x, pixel_avgs, marker='o')
ax1.set_ylabel("Pixel Value")
ax1.set_title("Average Pixel Value")
ax1.grid(True)

# subplot 2: each pixel value
for i in range(9):
    ax2.plot(x, pixel_all[i], label=f"Pixel {i}")
ax2.set_ylabel("Pixel Value")
ax2.set_title("Each Pixel Value")
ax2.legend()
ax2.grid(True)

# subplot 3: temp avg + device temp
ax3.plot(x, temp_avgs, marker='o', label="Avg Pixel Temp (°C)")
ax3.plot(x, device_temps, marker='x', label="Device Temp (°C)")
ax3.set_ylabel("Temperature (°C)")
ax3.set_xlabel("time line")
ax3.set_title("Temperature Over Time")
ax3.legend()
ax3.grid(True)

plt.tight_layout()
plt.savefig(root_dir + "/graph.png")
