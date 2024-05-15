# Face Recognition and Detection System

This project consists of two main scripts:

1. `face-db-recorder.py`: Records and stores a person's face into a database.
2. `main.py`: Runs real-time face detection based on the recorded database.

The project utilizes the [face_recognition](https://github.com/ageitgey/face_recognition/tree/master) library, a simple face recognition framework for Python. 

## Installation

### Prerequisites

- Python 3.3 or higher
- OpenCV
- face_recognition
- numpy

## Usage

### 1. Record and Store Faces

Run the `face-db-recorder.py` script to capture and store images of faces in the database.

```bash
python face-db-recorder.py
```

The script will prompt you to enter a name. After entering the name, it will start capturing images from the webcam and store them in the `database/{name}` directory. Press `Esc` to stop capturing photos.

### 2. Real-time Face Detection

Run the `main.py` script to perform real-time face detection using the recorded database.

```bash
python main.py
```

The script will access the stored faces in the database and perform real-time face recognition.

## Acknowledgements

- [face_recognition](https://github.com/ageitgey/face_recognition/tree/master), a face recognition framework for Python. 