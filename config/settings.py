# config/settings.py - COMPLETE FILE
class Config:
    # Directories
    OUTPUT_DIR = "output"
    
    # Video processing
    TARGET_FPS = 30
    MAX_RESOLUTION = (1280, 720)
    
    # Pose detection
    MIN_DETECTION_CONFIDENCE = 0.5
    MIN_TRACKING_CONFIDENCE = 0.5
    
    # Biomechanics thresholds
    OPTIMAL_ELBOW_ANGLE_MIN = 110
    OPTIMAL_ELBOW_ANGLE_MAX = 140
    MAX_SPINE_LEAN = 20
    MAX_HEAD_KNEE_DISTANCE = 0.05
    MIN_BALANCE_SCORE = 0.7
