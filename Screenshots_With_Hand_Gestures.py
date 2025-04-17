import cv2
import mediapipe as mp
import time
import pyautogui
import tkinter as tk
from threading import Thread
from PIL import Image, ImageTk
import os
import glob
import random
import winsound

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

# Track time for delay between screenshots
last_screenshot_time = 0
screenshot_delay = 3  # seconds
GESTURE_HOLD_TIME = 1.0  # seconds


# Gesture detection functions (same as before)
def is_open_palm(landmarks):
    fingers = []
    tip_ids = [8, 12, 16, 20]
    pip_ids = [6, 10, 14, 18]
    for tip_id, pip_id in zip(tip_ids, pip_ids):
        fingers.append(landmarks[tip_id].y < landmarks[pip_id].y)
    return sum(fingers) >= 3


def is_peace_sign(landmarks):
    index_open = landmarks[8].y < landmarks[6].y
    middle_open = landmarks[12].y < landmarks[10].y
    ring_closed = landmarks[16].y > landmarks[14].y
    pinky_closed = landmarks[20].y > landmarks[18].y
    thumb_closed = landmarks[4].x > landmarks[3].x if landmarks[4].x > landmarks[2].x else landmarks[4].x < landmarks[
        3].x
    return index_open and middle_open and ring_closed and pinky_closed and thumb_closed


# Sound effects
def play_sound_effect():
    winsound.Beep(1000, 300)


def play_camera_shutter_sound():
    winsound.PlaySound("camera_shutter.wav", winsound.SND_FILENAME)


def get_funny_feedback():
    messages = [
        "Snap! You've got the shot!",
        "Great gesture! Picture perfect!",
        "Your hand is a star!",
        "Wow, you're a pro!",
        "Screenshot taken with style!"
    ]
    return random.choice(messages)


class GestureScreenshotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gesture Screenshot App")
        self.root.geometry("900x900")  # Increased size for better layout
        self.root.config(bg="#f5f5f5")

        # Main application variables
        self.gesture_type = tk.StringVar(value="Open Palm")
        self.gesture_detected = False
        self.gesture_start_time = 0

        # Create main container
        self.main_container = tk.Frame(root, bg="#f5f5f5")
        self.main_container.pack(fill=tk.BOTH, expand=True)

        # Video display section
        self.video_frame = tk.Frame(self.main_container, bg="#2c3e50")
        self.video_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.video_label = tk.Label(self.video_frame, bg="#2c3e50")
        self.video_label.pack(pady=10)

        # Controls section
        self.controls_frame = tk.Frame(self.main_container, bg="#f5f5f5")
        self.controls_frame.pack(fill=tk.X, padx=10, pady=5)

        # Gesture selection
        gesture_select_frame = tk.Frame(self.controls_frame, bg="#34495e")
        gesture_select_frame.pack(side=tk.LEFT, padx=10)
        tk.Label(gesture_select_frame, text="Select Gesture:", font=("Arial", 12),
                 fg="#ecf0f1", bg="#34495e").pack(side=tk.LEFT, padx=5)
        tk.OptionMenu(gesture_select_frame, self.gesture_type,
                      "Open Palm", "Peace Sign").pack(side=tk.LEFT)

        # Status label
        self.status_label = tk.Label(self.controls_frame, text="Show a gesture to take a screenshot",
                                     font=("Arial", 12), bg="#f5f5f5")
        self.status_label.pack(side=tk.LEFT, expand=True, padx=20)

        # Gallery section
        self.gallery_frame = tk.Frame(self.main_container, bg="#ecf0f1", height=200)
        self.gallery_frame.pack(fill=tk.BOTH, expand=False, padx=10, pady=10)
        self.gallery_frame.pack_propagate(False)

        # Gallery header with refresh button
        gallery_header = tk.Frame(self.gallery_frame, bg="#ecf0f1")
        gallery_header.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(gallery_header, text="Recent Screenshots:", font=("Arial", 12, "bold"),
                 bg="#ecf0f1").pack(side=tk.LEFT)

        # Gallery refresh button
        self.refresh_btn = tk.Button(gallery_header, text="⟳ Refresh Gallery",
                                     command=self.update_gallery, font=("Arial", 10, "bold"),
                                     bg="#3498db", fg="white", relief=tk.RAISED)
        self.refresh_btn.pack(side=tk.RIGHT, padx=5)

        # Gallery images container with scrollbar
        self.gallery_canvas = tk.Canvas(self.gallery_frame, bg="#ecf0f1",
                                        highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.gallery_frame, orient=tk.HORIZONTAL,
                                      command=self.gallery_canvas.xview)
        self.gallery_canvas.configure(xscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.gallery_canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.gallery_images_frame = tk.Frame(self.gallery_canvas, bg="#ecf0f1")
        self.gallery_canvas.create_window((0, 0), window=self.gallery_images_frame, anchor="nw")

        # Visual feedback elements
        self.flash_label = tk.Label(self.video_label, bg="white")
        self.flash_label.place(relwidth=1, relheight=1)
        self.flash_label.lower()

        self.feedback_label = tk.Label(self.video_label, text="", font=("Arial", 20),
                                       bg="yellow", fg="black")
        self.feedback_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.feedback_label.lower()

        # Start video capture thread
        self.running = True
        self.capture_thread = Thread(target=self.capture_video)
        self.capture_thread.start()

        # Initial gallery update
        self.update_gallery()

        # Bind canvas configuration
        self.gallery_images_frame.bind("<Configure>", self.on_frame_configure)

    def on_frame_configure(self, event):
        """Update scroll region when gallery frame changes size"""
        self.gallery_canvas.configure(scrollregion=self.gallery_canvas.bbox("all"))

    def update_gallery(self):
        """Refresh the gallery display with latest screenshots"""
        # Clear existing thumbnails
        for widget in self.gallery_images_frame.winfo_children():
            widget.destroy()

        # Get latest screenshots (most recent first)
        image_files = sorted(glob.glob("screenshot_*.png"),
                             key=os.path.getmtime, reverse=True)[:10]

        if not image_files:
            empty_label = tk.Label(self.gallery_images_frame,
                                   text="No screenshots yet! Take some with gestures.",
                                   font=("Arial", 10), bg="#ecf0f1")
            empty_label.pack(pady=50)
            return

        # Create thumbnails
        thumbnail_size = (160, 120)  # Slightly larger thumbnails
        for img_path in image_files:
            try:
                img = Image.open(img_path)
                img.thumbnail(thumbnail_size)
                img_tk = ImageTk.PhotoImage(img)

                # Create thumbnail frame
                thumb_frame = tk.Frame(self.gallery_images_frame, bg="#ecf0f1",
                                       padx=5, pady=5)
                thumb_frame.pack(side=tk.LEFT, fill=tk.Y)

                # Display image
                img_label = tk.Label(thumb_frame, image=img_tk, bg="#ecf0f1")
                img_label.image = img_tk  # Keep reference
                img_label.pack()

                # Display filename (shortened)
                filename = os.path.basename(img_path)
                if len(filename) > 15:
                    filename = filename[:12] + "..."
                tk.Label(thumb_frame, text=filename, font=("Arial", 8),
                         bg="#ecf0f1").pack()

                # Add click to open functionality
                img_label.bind("<Button-1>", lambda e, path=img_path: self.open_full_image(path))
            except Exception as e:
                print(f"Error loading {img_path}: {str(e)}")

        # Update scroll region
        self.gallery_images_frame.update_idletasks()
        self.gallery_canvas.configure(scrollregion=self.gallery_canvas.bbox("all"))

    def open_full_image(self, image_path):
        """Open the full image in a new window"""
        top = tk.Toplevel(self.root)
        top.title(os.path.basename(image_path))

        img = Image.open(image_path)
        img_tk = ImageTk.PhotoImage(img)

        label = tk.Label(top, image=img_tk)
        label.image = img_tk  # Keep reference
        label.pack()

        tk.Button(top, text="Close", command=top.destroy).pack(pady=5)

    def detect_gesture(self, landmarks):
        gesture = self.gesture_type.get()
        if gesture == "Open Palm":
            return is_open_palm(landmarks)
        elif gesture == "Peace Sign":
            return is_peace_sign(landmarks)
        return False

    def show_flash_and_feedback(self, message):
        self.flash_label.lift()
        self.feedback_label.config(text=message)
        self.feedback_label.lift()
        self.root.after(300, self.flash_label.lower)
        self.root.after(2000, self.feedback_label.lower)
        self.update_gallery()  # Refresh gallery after new screenshot

    def show_thumbnail_preview(self, filepath):
        img = Image.open(filepath)
        img.thumbnail((120, 90))
        img_tk = ImageTk.PhotoImage(img)

        # Create a temporary preview in the corner
        preview = tk.Toplevel(self.root)
        preview.overrideredirect(True)
        preview.geometry(f"+{self.root.winfo_x() + self.root.winfo_width() - 150}+{self.root.winfo_y() + 50}")

        label = tk.Label(preview, image=img_tk, bg="white", relief="solid", borderwidth=1)
        label.image = img_tk
        label.pack()

        preview.after(2000, preview.destroy)

    def capture_video(self):
        global last_screenshot_time
        cap = cv2.VideoCapture(0)

        while self.running:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = hands.process(rgb_frame)

            current_gesture_detected = False

            if result.multi_hand_landmarks:
                for hand_landmarks in result.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                    if self.detect_gesture(hand_landmarks.landmark):
                        current_gesture_detected = True

                        if not self.gesture_detected:
                            self.gesture_detected = True
                            self.gesture_start_time = time.time()
                        else:
                            gesture_hold_time = time.time() - self.gesture_start_time

                            if gesture_hold_time >= GESTURE_HOLD_TIME:
                                current_time = time.time()
                                if current_time - last_screenshot_time > screenshot_delay:
                                    screenshot = pyautogui.screenshot()
                                    timestamp = int(current_time)
                                    filename = f"screenshot_{timestamp}.png"
                                    screenshot.save(filename)
                                    last_screenshot_time = current_time
                                    feedback_message = get_funny_feedback()
                                    self.status_label.config(text=f"Screenshot taken: {filename}")
                                    self.show_flash_and_feedback(feedback_message)
                                    play_camera_shutter_sound()
                                    play_sound_effect()
                                    self.gesture_detected = False
                    else:
                        self.gesture_detected = False
            else:
                self.gesture_detected = False
                self.status_label.config(text="No hand detected, please show your hand.")

            img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)

        cap.release()
        cv2.destroyAllWindows()

    def on_close(self):
        self.running = False
        self.capture_thread.join()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = GestureScreenshotApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()
