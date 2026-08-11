import cv2
import numpy as np
import os
import tkinter as tk
from tkinter import simpledialog, messagebox
from PIL import Image, ImageTk
from collections import Counter

DATABASE_FILE = "face_database.yml"
NAMES_FILE = "registered_names.npy"
CONFIDENCE_THRESHOLD = 40
REQUIRED_MATCHES = 7
HISTORY_SIZE = 15
REQUIRED_SAMPLES = 30

face_detector = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)

recognizer = cv2.face.LBPHFaceRecognizer_create(
    radius=1,
    neighbors=8,
    grid_x=8,
    grid_y=8
)

registered_names = {}
next_id = 1

registering = False
registration_samples = []
sample_count = 0
current_name = ""
current_id = 0

prediction_history = []

last_result = "ready"
last_name = ""
last_confidence = 0

result_hold = 0


if os.path.exists(NAMES_FILE):

    try:
        registered_names = np.load(
            NAMES_FILE,
            allow_pickle=True
        ).item()

        if registered_names:
            next_id = max(
                registered_names.keys()
            ) + 1

    except:
        registered_names = {}


if (
    os.path.exists(DATABASE_FILE)
    and registered_names
):

    try:
        recognizer.read(
            DATABASE_FILE
        )
    except:
        pass


camera = cv2.VideoCapture(0)

camera.set(
    cv2.CAP_PROP_FRAME_WIDTH,
    640
)

camera.set(
    cv2.CAP_PROP_FRAME_HEIGHT,
    480
)

camera.set(
    cv2.CAP_PROP_FPS,
    30
)


if not camera.isOpened():

    print("Camera could not be opened.")
    exit()


root = tk.Tk()

root.title(
    "Biometric Facial Authentication"
)

root.geometry(
    "1150x680"
)

root.configure(
    bg="#101010"
)


left_frame = tk.Frame(
    root,
    bg="black"
)

left_frame.pack(
    side="left",
    padx=15,
    pady=15
)


camera_label = tk.Label(
    left_frame,
    bg="black"
)

camera_label.pack()


right_frame = tk.Frame(
    root,
    bg="#1b1b1b",
    width=300
)

right_frame.pack(
    side="right",
    fill="y",
    padx=15,
    pady=15
)

right_frame.pack_propagate(False)


title_label = tk.Label(
    right_frame,
    text="BIOMETRIC\nFACIAL AUTHENTICATION",
    font=("Arial", 19, "bold"),
    bg="#1b1b1b",
    fg="white",
    justify="center"
)

title_label.pack(
    pady=30
)


status_label = tk.Label(
    right_frame,
    text="READY",
    font=("Arial", 18, "bold"),
    bg="#1b1b1b",
    fg="#00ffff",
    justify="center"
)

status_label.pack(
    pady=20
)


user_label = tk.Label(
    right_frame,
    text="Registered Users: 0",
    font=("Arial", 12),
    bg="#1b1b1b",
    fg="white"
)

user_label.pack(
    pady=8
)


score_label = tk.Label(
    right_frame,
    text="Confidence: --",
    font=("Arial", 12),
    bg="#1b1b1b",
    fg="white"
)

score_label.pack(
    pady=8
)


register_button = tk.Button(
    right_frame,
    text="REGISTER FACE",
    font=("Arial", 13, "bold"),
    bg="#333333",
    fg="white",
    width=20,
    height=2
)

register_button.pack(
    pady=12
)


reset_button = tk.Button(
    right_frame,
    text="RESET DATABASE",
    font=("Arial", 13, "bold"),
    bg="#333333",
    fg="white",
    width=20,
    height=2
)

reset_button.pack(
    pady=12
)


exit_button = tk.Button(
    right_frame,
    text="EXIT",
    font=("Arial", 13, "bold"),
    bg="#333333",
    fg="white",
    width=20,
    height=2
)

exit_button.pack(
    pady=12
)


info_label = tk.Label(
    right_frame,
    text="Live camera authentication\n\nRegistered faces are stored\npermanently.\n\nUnknown faces are rejected.",
    font=("Arial", 10),
    bg="#1b1b1b",
    fg="#999999",
    justify="center"
)

info_label.pack(
    pady=20
)


def update_user_count():

    user_label.config(
        text=f"Registered Users: {len(registered_names)}"
    )


def save_names():

    np.save(
        NAMES_FILE,
        registered_names,
        allow_pickle=True
    )


def get_new_id():

    global next_id

    while next_id in registered_names:
        next_id += 1

    return next_id


def start_registration():

    global registering
    global registration_samples
    global sample_count
    global current_name
    global current_id
    global prediction_history
    global last_result

    if registering:
        return

    name = simpledialog.askstring(
        "Register Face",
        "Enter user's name:",
        parent=root
    )

    if name is None:
        return

    name = name.strip()

    if not name:
        messagebox.showwarning(
            "Invalid Name",
            "Please enter a valid name."
        )
        return

    current_name = name

    current_id = get_new_id()

    registering = True

    registration_samples = []

    sample_count = 0

    prediction_history = []

    last_result = "ready"

    status_label.config(
        text=f"REGISTERING\n{current_name}",
        fg="yellow"
    )

    score_label.config(
        text="Samples: 0/30"
    )


def finish_registration():

    global registering
    global registration_samples
    global sample_count
    global registered_names
    global next_id
    global last_result
    global prediction_history

    if len(registration_samples) < REQUIRED_SAMPLES:
        return

    labels = np.full(
        len(registration_samples),
        current_id,
        dtype=np.int32
    )

    try:

        if os.path.exists(DATABASE_FILE):

            recognizer.update(
                registration_samples,
                labels
            )

        else:

            recognizer.train(
                registration_samples,
                labels
            )

        recognizer.write(
            DATABASE_FILE
        )

    except Exception as e:

        messagebox.showerror(
            "Registration Error",
            str(e)
        )

        registering = False

        return

    registered_names[
        current_id
    ] = current_name

    save_names()

    next_id += 1

    registering = False

    registration_samples = []

    sample_count = 0

    prediction_history = []

    last_result = "ready"

    status_label.config(
        text=f"{current_name}\nREGISTERED",
        fg="#00ffff"
    )

    score_label.config(
        text="Registration Complete"
    )

    update_user_count()


def reset_database():

    global registered_names
    global next_id
    global registering
    global registration_samples
    global sample_count
    global prediction_history
    global last_result
    global last_name
    global last_confidence

    answer = messagebox.askyesno(
        "Reset Database",
        "Delete ALL registered users?"
    )

    if not answer:
        return

    registered_names = {}

    next_id = 1

    registering = False

    registration_samples = []

    sample_count = 0

    prediction_history = []

    last_result = "ready"

    last_name = ""

    last_confidence = 0

    if os.path.exists(
        DATABASE_FILE
    ):
        os.remove(
            DATABASE_FILE
        )

    if os.path.exists(
        NAMES_FILE
    ):
        os.remove(
            NAMES_FILE
        )

    status_label.config(
        text="NO USERS\nREGISTERED",
        fg="orange"
    )

    score_label.config(
        text="Confidence: --"
    )

    update_user_count()


def close_program():

    camera.release()

    cv2.destroyAllWindows()

    root.destroy()


register_button.config(
    command=start_registration
)

reset_button.config(
    command=reset_database
)

exit_button.config(
    command=close_program
)

update_user_count()


def process_authentication(face):

    global prediction_history
    global last_result
    global last_name
    global last_confidence
    global result_hold

    label, confidence = recognizer.predict(
        face
    )

    if (
        label in registered_names
        and confidence < CONFIDENCE_THRESHOLD
    ):

        prediction_history.append(
            (
                "success",
                label,
                confidence
            )
        )

    else:

        prediction_history.append(
            (
                "failed",
                -1,
                confidence
            )
        )

    if len(prediction_history) > HISTORY_SIZE:

        prediction_history.pop(0)

    if len(prediction_history) < 8:
        return

    successful_people = [
        item
        for item in prediction_history
        if item[0] == "success"
    ]

    failed_people = [
        item
        for item in prediction_history
        if item[0] == "failed"
    ]

    if len(successful_people) >= REQUIRED_MATCHES:

        person_ids = [
            item[1]
            for item in successful_people
        ]

        most_common = Counter(
            person_ids
        ).most_common(1)[0]

        person_id = most_common[0]

        person_votes = most_common[1]

        if person_votes >= REQUIRED_MATCHES:

            person_name = registered_names[
                person_id
            ]

            confidence_values = [
                item[2]
                for item in successful_people
                if item[1] == person_id
            ]

            average_confidence = (
                sum(confidence_values)
                /
                len(confidence_values)
            )

            last_result = "success"

            last_name = person_name

            last_confidence = (
                average_confidence
            )

            result_hold = 15

            prediction_history.clear()

            return

    if len(failed_people) >= REQUIRED_MATCHES:

        confidence_values = [
            item[2]
            for item in failed_people
        ]

        average_confidence = (
            sum(confidence_values)
            /
            len(confidence_values)
        )

        last_result = "failed"

        last_name = ""

        last_confidence = (
            average_confidence
        )

        result_hold = 15

        prediction_history.clear()


def update_camera():

    global registering
    global registration_samples
    global sample_count
    global result_hold
    global last_result

    ret, frame = camera.read()

    if not ret:

        root.after(
            30,
            update_camera
        )

        return

    frame = cv2.flip(
        frame,
        1
    )

    gray = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2GRAY
    )

    gray = cv2.equalizeHist(
        gray
    )

    faces = face_detector.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=7,
        minSize=(110, 110)
    )

    if registering:

        prediction_history.clear()

        last_result = "ready"

        if len(faces) == 1:

            x, y, w, h = faces[0]

            face = gray[
                y:y+h,
                x:x+w
            ]

            face = cv2.resize(
                face,
                (200, 200)
            )

            if sample_count < REQUIRED_SAMPLES:

                registration_samples.append(
                    face.copy()
                )

                sample_count += 1

            cv2.rectangle(
                frame,
                (x, y),
                (x+w, y+h),
                (0, 255, 255),
                3
            )

            cv2.putText(
                frame,
                f"REGISTERING {sample_count}/30",
                (x, y - 15),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 255),
                2
            )

            status_label.config(
                text=f"REGISTERING\n{current_name}",
                fg="yellow"
            )

            score_label.config(
                text=f"Samples: {sample_count}/30"
            )

            if sample_count >= REQUIRED_SAMPLES:

                finish_registration()

        elif len(faces) > 1:

            status_label.config(
                text="ONLY ONE FACE\nALLOWED",
                fg="orange"
            )

            score_label.config(
                text="Registration paused"
            )

        else:

            status_label.config(
                text="LOOK AT CAMERA",
                fg="yellow"
            )

            score_label.config(
                text=f"Samples: {sample_count}/30"
            )

    else:

        if len(registered_names) == 0:

            status_label.config(
                text="NO USERS\nREGISTERED",
                fg="orange"
            )

            score_label.config(
                text="Confidence: --"
            )

            last_result = "ready"

        elif len(faces) == 0:

            prediction_history.clear()

            if result_hold > 0:

                result_hold -= 1

            else:

                last_result = "ready"

                status_label.config(
                    text="NO FACE\nDETECTED",
                    fg="yellow"
                )

                score_label.config(
                    text="Confidence: --"
                )

        elif len(faces) > 1:

            prediction_history.clear()

            last_result = "ready"

            status_label.config(
                text="MULTIPLE FACES\nDETECTED",
                fg="orange"
            )

            score_label.config(
                text="Authentication paused"
            )

        else:

            x, y, w, h = faces[0]

            face = gray[
                y:y+h,
                x:x+w
            ]

            face = cv2.resize(
                face,
                (200, 200)
            )

            process_authentication(
                face
            )

            if result_hold > 0:

                result_hold -= 1

            if last_result == "success":

                color = (
                    0,
                    255,
                    0
                )

                status_label.config(
                    text=f"AUTHENTICATION\nSUCCESSFUL\n{last_name}",
                    fg="#00ff66"
                )

                score_label.config(
                    text=f"Confidence: {last_confidence:.1f}"
                )

                cv2.rectangle(
                    frame,
                    (x, y),
                    (x+w, y+h),
                    color,
                    3
                )

                cv2.putText(
                    frame,
                    "AUTHENTICATED",
                    (x, y - 15),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    color,
                    2
                )

                cv2.putText(
                    frame,
                    last_name,
                    (x, y+h+25),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    color,
                    2
                )

            elif last_result == "failed":

                color = (
                    0,
                    0,
                    255
                )

                status_label.config(
                    text="AUTHENTICATION\nFAILED",
                    fg="#ff3333"
                )

                score_label.config(
                    text=f"Confidence: {last_confidence:.1f}"
                )

                cv2.rectangle(
                    frame,
                    (x, y),
                    (x+w, y+h),
                    color,
                    3
                )

                cv2.putText(
                    frame,
                    "UNKNOWN FACE",
                    (x, y - 15),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    color,
                    2
                )

            else:

                color = (
                    0,
                    255,
                    255
                )

                status_label.config(
                    text="VERIFYING...",
                    fg="yellow"
                )

                score_label.config(
                    text="Checking identity..."
                )

                cv2.rectangle(
                    frame,
                    (x, y),
                    (x+w, y+h),
                    color,
                    3
                )

                cv2.putText(
                    frame,
                    "VERIFYING",
                    (x, y - 15),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    color,
                    2
                )

    frame = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    frame = cv2.resize(
        frame,
        (800, 600)
    )

    image = Image.fromarray(
        frame
    )

    photo = ImageTk.PhotoImage(
        image=image
    )

    camera_label.config(
        image=photo
    )

    camera_label.image = photo

    root.after(
        20,
        update_camera
    )


update_camera()

root.protocol(
    "WM_DELETE_WINDOW",
    close_program
)

root.mainloop()
