import cv2
import subprocess

def is_video_capture_device(dev_path):
    result = subprocess.run(
        ["v4l2-ctl", f"--device={dev_path}", "--all"],
        capture_output=True, text=True
    )
    output = result.stdout

    if "Capabilities" in output and "Video Capture" in output:
        if "Pixel Format" in output and "'YUYV'" in output:
            return True
    return False

def find_real_video_devices(target_name):
    result = subprocess.run(["v4l2-ctl", "--list-devices"], capture_output=True, text=True)
    lines = result.stdout.splitlines()

    devices = []
    capture = False

    for line in lines:
        if not line.startswith("\t"):
            capture = target_name in line
        elif capture:
            dev = line.strip()
            if dev.startswith("/dev/video") and is_video_capture_device(dev):
                devices.append(dev)

    return devices

def draw_symmetric_grid_points(frame, spacing_x=220, spacing_y=170):
    h, w = frame.shape[:2]
    center_x = w // 2
    center_y = h // 2
    measure_points = []

    offset_y = [-spacing_y, 0, spacing_y]
    offset_x = [-spacing_x, 0, spacing_x]
    
    idx = 0
    for dy in offset_y:
        for dx in offset_x:
            cx = center_x + dx
            cy = center_y + dy
            cv2.circle(frame, (cx, cy), radius=8, color=(255, 255, 255), thickness=-1)
            cv2.putText(frame, str(idx), (cx + 10, cy - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            measure_points.append((cx, cy))
            idx += 1
    return frame, measure_points

def draw_measure_points(frame, points, offset_x=5, offset_y=5):
    for (x, y) in points:
        ox = x + offset_x
        oy = y - offset_y
        cv2.circle(frame, (ox, oy), radius=5, color=(0, 255, 0), thickness=-1)
    return frame

def measured_points(frame, points, offset_x=50, offset_y=0):
    pts = []
    for (x, y) in points:
        ox = x + offset_x
        oy = y - offset_y
        pixel = frame[oy, ox]
        pts.append(int(pixel[0]))
    return pts

if __name__ == "__main__":
    target = "AFN_Cap video: AFN_Cap video"
    video_devices = find_real_video_devices(target)
    device_path = video_devices[0]

    cap = cv2.VideoCapture(device_path, cv2.CAP_V4L2)

    if not cap.isOpened():
        print("카메라를 열 수 없음")
        exit()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("프레임을 읽을 수 없음")
            break

        frame = cv2.applyColorMap(frame, cv2.COLORMAP_JET)
        frame, measure_points = draw_symmetric_grid_points(frame)
        frame = draw_measure_points(frame, measure_points, 50, 0)

        cv2.imshow('FPV Camera', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
