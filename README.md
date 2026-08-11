# Facial Biometric Authentication System

A Python-based facial biometric authentication system that uses a **live camera** to detect, register, and authenticate users through facial recognition.

## 📌 Overview

This project implements a basic biometric authentication system using **OpenCV** and **Python**. A user can register their face using the webcam, after which the system stores the facial data and uses it to authenticate the user during subsequent camera sessions.

The system can recognize registered users and reject unknown faces with an **Authentication Failed** message.

## ✨ Features

* 📷 Live webcam-based face detection
* 👤 Face registration
* 🔐 Real-time facial authentication
* ✅ Authentication Successful for registered users
* ❌ Authentication Failed for unknown users
* 💾 Persistent storage of registered facial data
* 🖥️ Simple graphical user interface
* 🔄 Continuous live-camera authentication

## 🛠️ Technologies Used

* **Python 3.x**
* **OpenCV**
* **NumPy**
* **Tkinter**
* **Pillow**

## 📂 Project Structure

```text
facial-biometric-authentication/
│
├── app.py
├── users/
├── trainer/
├── requirements.txt
└── README.md
```

The folders used for storing registered facial data may be created automatically when the application is run.

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/your-username/facial-biometric-authentication.git
```

Go to the project directory:

```bash
cd facial-biometric-authentication
```

Install the required libraries:

```bash
pip install opencv-contrib-python numpy pillow
```

## ▶️ Running the Project

Run:

```bash
python app.py
```

The application will open the webcam and provide options to register a face and authenticate users.

## 🔐 How It Works

### 1. Register Face

Click **Register Face** and enter the user's name.

The webcam captures multiple images of the user's face and stores the facial information.

### 2. Authentication

After registration, the live camera continuously checks the detected face against the registered facial data.

```text
Live Camera
     ↓
Face Detection
     ↓
Face Recognition
     ↓
Compare with Registered Data
     ↓
 ┌───────────────┐
 │               │
Match          No Match
 ↓                ↓
SUCCESS         FAILED
```

### 3. Authentication Result

For a registered user:

```text
Authentication Successful
User: Sam
```

For an unknown user:

```text
Authentication Failed
Unknown User
```

## 🎯 Objective

The objective of this project is to understand and implement the basic concepts of **biometric authentication and facial recognition**, including face detection, face registration, facial feature comparison, and authentication decisions.

## 🔮 Future Improvements

The current version is the initial implementation. Future versions can include:

* Multi-user management
* Authentication history and logs
* Liveness detection
* Anti-spoofing
* Unknown-face snapshots
* Failed-attempt alerts
* Admin dashboard
* Database integration
* Additional AI-based face features

## ⚠️ Disclaimer

This project is developed for **educational purposes** to demonstrate the working of facial biometric authentication. It should not be considered a production-ready security system.

## 👩‍💻 Author

**Samruddhi Jain**
B.Tech – Artificial Intelligence & Data Science
