import cv2
import numpy as np
import json
import os
from pathlib import Path

class JuggleTracker:
    def __init__(self):
        self.camera = None
        self.calibration_data = None
        self.config_dir = self._get_config_dir()
        
    def _get_config_dir(self):
        """Set up configuration directory based on OS"""
        if os.name == 'posix':  # macOS or Linux
            if 'darwin' in os.sys.platform:  # macOS
                config_dir = Path.home() / "Library/Application Support/JuggleTracker"
            else:  # Linux
                config_dir = Path.home() / ".config/JuggleTracker"
        else:
            raise NotImplementedError("Currently only supported on macOS and Linux")
        
        config_dir.mkdir(parents=True, exist_ok=True)
        return config_dir

    def init_camera(self):
        """Initialize the camera"""
        self.camera = cv2.VideoCapture(0)
        if not self.camera.isOpened():
            raise RuntimeError("Could not initialize camera")
        
        # Set camera properties
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        return True

    def load_calibration(self):
        """Load calibration data if it exists"""
        calibration_file = self.config_dir / "calibration.json"
        if calibration_file.exists():
            with open(calibration_file, 'r') as f:
                self.calibration_data = json.load(f)
            return True
        return False

    def needs_calibration(self):
        """Check if calibration is needed"""
        return self.calibration_data is None

    def release_camera(self):
        """Release the camera resource"""
        if self.camera is not None:
            self.camera.release()
            cv2.destroyAllWindows()

    def run(self):
        """Main run loop"""
        if not self.init_camera():
            return
        
        try:
            # Load existing calibration
            if not self.load_calibration():
                print("No calibration data found. Calibration needed.")
                # TODO: Run calibration process
                return

            while True:
                ret, frame = self.camera.read()
                if not ret:
                    print("Failed to grab frame")
                    break

                # Show the frame
                cv2.imshow('JuggleTracker', frame)

                # Break loop on 'q' press
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        finally:
            self.release_camera()

if __name__ == "__main__":
    tracker = JuggleTracker()
    tracker.run()