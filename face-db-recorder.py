import cv2
import os
from pathlib import Path


def count_files_in_folder(folder_path: str) -> int:
    """Count the number of files inside a folder."""
    path = Path(folder_path)
    num_files = sum(1 for item in path.iterdir() if item.is_file())
    return num_files


def capture_photo(savepath: str) -> bool:
    """Capture a photo, save it in savepath, then return bool indicating if a photo is taken."""

    # Initialize the webcam
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return False

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Display the resulting frame
        cv2.imshow("Press Space to Capture Photo or Esc to Exit", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord(" "):  # Space key to capture photo
            cv2.imwrite(savepath, frame)
            print(f"Photo saved to {savepath}")
            cap.release()
            cv2.destroyAllWindows()
            return True
        elif key == 27:  # Escape key to exit
            cap.release()
            cv2.destroyAllWindows()
            return False


def main():

    while True:
        name = input("Please enter your name (or type 'q' to quit): ")

        # Check if the user wants to quit
        if name.lower() == "q":
            print("Goodbye!")
            break

        name = name.title()
        print(f"Hello, {name}!")

        # Capture and save the user's photo
        parent_folder = os.path.join("database", name)
        Path(parent_folder).mkdir(parents=True, exist_ok=True)

        # Check the number of photo currently in folder so do not overwrite
        i = count_files_in_folder(parent_folder) + 1

        while True:
            filepath = os.path.join(parent_folder, f"{name}{i}.jpg")
            success = capture_photo(filepath)
            if not success:  # If the user press escape during the photo
                print(f"Finished taking photo of {name}")
                break  # Exit the photo-taking loop
            i += 1


if __name__ == "__main__":
    main()
