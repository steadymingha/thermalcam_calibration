import cv2
import csv, os
import time
from temp_cam import find_real_video_devices, draw_symmetric_grid_points, measured_points
from thermistor import Thermistor
from datetime import datetime



# order of drawn points : channel number (0=0x48-CH0, 1=0x48-CH1, ..4=0x49-CH0 ..)
PTS_ORDER = [8, 7, 6, 4, 5, 3, 0, 1, 2]

if __name__ == "__main__":
    root_dir = "./"
    csvfile_dir = os.path.join(root_dir, "output.csv")
    img_dir = os.path.join(root_dir, "output")

    csvfile = open(csvfile_dir,"a")
    writer = csv.writer(csvfile)
    writer.writerow(["timestamp", "cam temp", "pixel0","pixel1","pixel2","pixel3","pixel4","pixel5","pixel6","pixel7","pixel8","temp0","temp1","temp2","temp3","temp4","temp5","temp6","temp7","temp8"])

    therm = Thermistor()

    target = "AFN_Cap video: AFN_Cap video"
    video_devices = find_real_video_devices(target)
    device_path = video_devices[0]

    cap = cv2.VideoCapture(device_path, cv2.CAP_V4L2)

    if not cap.isOpened():
        print("can't open camera")
        exit()

    stable_time = 1500
    idx = 0
    csvfile.close()
    
    while True:
        csvfile = open(csvfile_dir,"a")
        writer = csv.writer(csvfile)
        now = datetime.now()#.strftime('%H%M%S')
        ret, frame = cap.read()
        if not ret:
            print("can't read frame")
            break

        if idx <stable_time:
            idx += 1
            continue
        elif idx == (stable_time + 108000):
            break

        therm_out = therm.read()
        frame, thermistor_pts = draw_symmetric_grid_points(frame)
        measured_pixel = measured_points(frame, thermistor_pts, 50, 0)
        sorted_therm_out = [therm_out[:-1][i] for i in PTS_ORDER]

        device_temp = therm_out[-1]
        writer.writerow([now.strftime('%H:%M:%S'), device_temp, *measured_pixel, *sorted_therm_out])



        filename_out = os.path.join(img_dir, f"{now.strftime('%y%m%d_%H:%M:%S')}.jpg")
        # frame = cv2.applyColorMap(frame, cv2.COLORMAP_JET)
        cv2.imwrite(filename_out, frame)

        if cv2.waitKey(1) == 27:  # ESC
            break

        csvfile.close()

        time.sleep(10) # 1분
        idx += 1

    cap.release()   