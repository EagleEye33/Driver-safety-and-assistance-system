# 🚘 Driver Safety System using Computer Vision

An advanced real-time Driver Assistance System that monitors lane discipline, detects driver drowsiness, and alerts for potential collisions or unsafe proximity to other vehicles and pedestrians using computer vision.

Built with ❤️ using OpenCV, Mediapipe, and deep learning.

---

## 📸 Features

- ✅ **Lane Detection & Lane Departure Warning**
- 😴 **Drowsiness Detection** using Eye Aspect Ratio (EAR)
- 🧠 **Face Mesh Monitoring** (yawning, face visibility, etc.)
- 🚗 **Vehicle & Object Detection Ahead**
- 📏 **Proximity Alert System** (warns if too close to another vehicle/person)
- 🔊 **Audio Alerts** to keep the driver aware
- 👨‍💻 **Real-time Processing** via Webcam or Video Feed

---

## 🛠 Installation

### 1. **Clone the Repository**
```bash
git clone https://github.com/your-username/driver-safety-system.git
cd driver-safety-system
```
### 2. **Install Requirements**
```bash
pip install -r requirements.txt
```

### 3.▶️ How to Run
1. **Lane and Curve Detection**
```bash
python lane_detector.py
```
2. **Drowsiness Detection & Face Mesh Monitoring**
```bash
python drowsiness_detector.py
```
**Note**
- Make sure to have a webcam or video feed available for real-time processing.
- Adjust the camera settings as needed for optimal performance.
- To test the sample video feed, replace `0` with the path to your video file in the respective script.

3. **(Upcoming) Vehicle/Object Detection and Proximity Alerts**
Will be added soon in proximity_detector.py


### 4.🧠 Technologies Used
1. **OpenCV** – Image processing and video stream

2. **Mediapipe** – Real-time facial mesh tracking

3. **NumPy** – Mathematical operations

4. **YOLOv8 / YOLOv5** – Object detection (for future modules)

5. **Python** – Glue for everything


**🤝 Contributing**
Want to help make this better? Found a bug or want to add a new feature?

1. Fork this repository

2. Create a new branch (git checkout -b feature-name)

3. Make your changes and commit (git commit -am 'Add new feature')

4. Push to your branch (git push origin feature-name)

5. Create a Pull Request

**📧 Contact**
Feel free to reach out if you're interested in collaborating or have questions.

**⭐️ Final Note**
This is a passion project to build smart safety systems using AI and computer vision.
Feel free to fork, star, and contribute. Let’s make driving safer together. ❤️

