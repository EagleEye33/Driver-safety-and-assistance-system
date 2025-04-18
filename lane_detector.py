import cv2
import numpy as np

def region_of_interest(img, vertices):
    mask = np.zeros_like(img)
    cv2.fillPoly(mask, [vertices], 255)
    masked = cv2.bitwise_and(img, mask)
    return masked

def make_coordinates(image, line_parameters):
    slope, intercept = line_parameters
    y1 = image.shape[0]  # bottom of the frame
    y2 = int(y1 * 0.7)
    if slope == 0:
        slope = 0.1   # a bit higher up
    x1 = int((y1 - intercept) / slope)
    x2 = int((y2 - intercept) / slope)

    x1 = max(0, min(x1, image.shape[1]))
    x2 = max(0, min(x2, image.shape[1]))
    return np.array([x1, y1, x2, y2])

def average_slope_intercept(image, lines):
    left_fit = []
    right_fit = []
    if lines is None:
        return []

    for line in lines:
        x1, y1, x2, y2 = line[0]
        if x2 == x1:
            continue  # avoid division by zero
        slope = (y2 - y1) / (x2 - x1)
        intercept = y1 - slope * x1
        if slope < -0.5:
            left_fit.append((slope, intercept))
        elif slope > 0.5:
            right_fit.append((slope, intercept))

    averaged_lines = []
    if left_fit:
        left_avg = np.mean(left_fit, axis=0)
        averaged_lines.append(make_coordinates(image, left_avg))
    if right_fit:
        right_avg = np.mean(right_fit, axis=0)
        averaged_lines.append(make_coordinates(image, right_avg))
    
    return np.array(averaged_lines)

def draw_lines(img, lines):
    if lines is None:
        return
    averaged = average_slope_intercept(img, lines)
    for x1, y1, x2, y2 in averaged:
        cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 8)


def process_frame(frame):
    height = frame.shape[0]
    width = frame.shape[1]

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 50, 150)

    # Focus on region where lanes are expected
    roi_vertices = np.array([
        (0, height),
        (width // 2, height // 2),
        (width, height)
    ])
    cropped = region_of_interest(edges, roi_vertices)

    lines = cv2.HoughLinesP(cropped, 1, np.pi/180, threshold=50, minLineLength=50, maxLineGap=150)

    line_image = np.zeros_like(frame)
    draw_lines(line_image, lines)
    
    # Combine with original frame
    combined = cv2.addWeighted(frame, 0.8, line_image, 1, 0)
    return combined

# Load a video or use webcam
cap = cv2.VideoCapture(r"C:\Users\pankp\OneDrive\Desktop\pyprojects\DriveAssist\test_video2.mp4")  # or 0 for webcam

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    processed = process_frame(frame)
    cv2.imshow("Lane Detection", processed)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
