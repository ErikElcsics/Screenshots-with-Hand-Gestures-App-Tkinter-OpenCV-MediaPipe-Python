# 🖐️ Take Screenshots with Hand Gestures App

Take screenshots with your hand gestures using just a webcam! This app is built using OpenCV, MediaPipe, and a slick Tkinter interface, this app detects "Open Palm" or "Peace Sign" gestures and snaps screenshots with sound effects and a built-in gallery.



## 🚀 Features

- ✋ Gesture detection for screenshots (Open Palm, Peace Sign)
- 🎞️ Live webcam feed with real-time hand tracking
- 📸 Sound effects and flash feedback on capture
- 🖼️ Screenshot gallery with scrollable thumbnails
- 🔁 Refresh button and image preview popups
- 🖥️ Fully local — no internet or cloud needed
- 🧠 Gesture holding logic to prevent accidental shots



## 🎮 How It Works

1. Show a supported gesture (Open Palm or Peace Sign)
2. Hold it steady for 1 second
3. Screenshot is taken with sound, flash & funny feedback
4. Image is saved and appears in the built-in gallery



## 🧰 Developed With

- [Python 3](https://www.python.org/)
- [OpenCV](https://opencv.org/) – Video capture & processing
- [MediaPipe](https://google.github.io/mediapipe/) – Hand gesture recognition
- [Tkinter](https://docs.python.org/3/library/tkinter.html) – GUI framework
- [PyAutoGUI](https://pyautogui.readthedocs.io/) – Screenshot automation
- [Pillow](https://python-pillow.org/) – Image handling
- [winsound](https://docs.python.org/3/library/winsound.html) – Sound effects on Windows



## 📸 Gestures Supported

✋ Open Palm - To take a screenshot 
✌️ Peace Sign - To take a screenshot with style 

NOTE: More gestures can be added easily in code.



## 🛠️ Installation


git clone https://github.com/your-username/gesture-screenshot-app.git
cd gesture-screenshot-app
python Screenshots_With_Hand_Gestures.py


NOTE: Make sure you have a working webcam and run it on Windows (for sound support).


### 📦 Libraries Used

- [OpenCV (cv2)](https://pypi.org/project/opencv-python/) – For webcam access and frame processing  
- [MediaPipe](https://pypi.org/project/mediapipe/) – For real-time hand gesture detection  
- [PyAutoGUI](https://pypi.org/project/pyautogui/) – To take screenshots of the desktop  
- [Tkinter](https://docs.python.org/3/library/tkinter.html) – To build the GUI interface  
- [Pillow (PIL)](https://pypi.org/project/Pillow/) – For image handling and thumbnail generation  
- [Threading](https://docs.python.org/3/library/threading.html) – To keep video capture running without freezing the UI  
- [winsound](https://docs.python.org/3/library/winsound.html) – To play sound effects (Windows only)  
- [glob](https://docs.python.org/3/library/glob.html) – To search for screenshot files  
- [os](https://docs.python.org/3/library/os.html) – For file and path handling  
- [random](https://docs.python.org/3/library/random.html) – To display fun feedback messages  
- [time](https://docs.python.org/3/library/time.html) – For gesture timing and screenshot delays  


## 🔊 Customization

- Replace `camera_shutter.wav` with your own sound.
- Modify gesture detection logic in `is_open_palm()` or `is_peace_sign()`.
- Add new gestures and map them to actions!



## 📂 Screenshots Saved As

- screenshot_<timestamp>.png


They’re saved in the app’s root folder and displayed in the gallery.



## 📜 License

MIT License 

![image](https://github.com/user-attachments/assets/ace1c4f9-f61a-4aa8-a5a1-107445e8918b)

![image](https://github.com/user-attachments/assets/9b332fde-bda6-49fe-a834-6c973eccafb1)

