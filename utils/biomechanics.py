# utils/biomechanics.py - COMPLETE FILE
import numpy as np
import math

class BiomechanicsAnalyzer:
    def __init__(self):
        self.previous_metrics = None
        
    def analyze_frame(self, pose_results, frame_number):
        """Analyze biomechanics for current frame"""
        landmarks = pose_results['landmarks']
        
        metrics = {
            'frame': frame_number,
            'timestamp': frame_number / 30.0,
            'elbow_angle': self.calculate_elbow_angle(landmarks),
            'spine_lean': self.calculate_spine_lean(landmarks),
            'head_knee_alignment': self.calculate_head_knee_alignment(landmarks),
            'foot_direction': self.calculate_foot_direction(landmarks),
            'balance_score': self.calculate_balance(landmarks),
            'smoothness': self.calculate_smoothness(landmarks)
        }
        
        self.previous_metrics = metrics
        return metrics
    
    def calculate_elbow_angle(self, landmarks):
        """Calculate front elbow angle"""
        try:
            shoulder = landmarks[12]  # right_shoulder
            elbow = landmarks[14]    # right_elbow
            wrist = landmarks[16]    # right_wrist
            
            if all(point['visibility'] > 0.5 for point in [shoulder, elbow, wrist]):
                vec1 = np.array([shoulder['x'] - elbow['x'], shoulder['y'] - elbow['y']])
                vec2 = np.array([wrist['x'] - elbow['x'], wrist['y'] - elbow['y']])
                
                cos_angle = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
                angle = math.degrees(math.acos(np.clip(cos_angle, -1.0, 1.0)))
                
                return angle
        except:
            pass
        return None
    
    def calculate_spine_lean(self, landmarks):
        """Calculate spine lean angle"""
        try:
            left_hip = landmarks[23]
            right_hip = landmarks[24]
            left_shoulder = landmarks[11]
            right_shoulder = landmarks[12]
            
            if all(point['visibility'] > 0.5 for point in [left_hip, right_hip, left_shoulder, right_shoulder]):
                hip_mid = {'x': (left_hip['x'] + right_hip['x']) / 2, 'y': (left_hip['y'] + right_hip['y']) / 2}
                shoulder_mid = {'x': (left_shoulder['x'] + right_shoulder['x']) / 2, 'y': (left_shoulder['y'] + right_shoulder['y']) / 2}
                
                spine_vector = np.array([shoulder_mid['x'] - hip_mid['x'], shoulder_mid['y'] - hip_mid['y']])
                vertical = np.array([0, -1])
                
                cos_angle = np.dot(spine_vector, vertical) / np.linalg.norm(spine_vector)
                angle = math.degrees(math.acos(np.clip(cos_angle, -1.0, 1.0)))
                
                return angle
        except:
            pass
        return None
    
    def calculate_head_knee_alignment(self, landmarks):
        """Calculate head-knee alignment"""
        try:
            nose = landmarks[0]
            left_knee = landmarks[25]
            
            if all(point['visibility'] > 0.5 for point in [nose, left_knee]):
                return abs(nose['x'] - left_knee['x'])
        except:
            pass
        return None
    
    def calculate_foot_direction(self, landmarks):
        """Calculate foot direction"""
        try:
            left_ankle = landmarks[27]
            left_knee = landmarks[25]
            
            if all(point['visibility'] > 0.5 for point in [left_ankle, left_knee]):
                foot_vector = np.array([left_ankle['x'] - left_knee['x'], left_ankle['y'] - left_knee['y']])
                horizontal = np.array([1, 0])
                
                cos_angle = np.dot(foot_vector, horizontal) / np.linalg.norm(foot_vector)
                angle = math.degrees(math.acos(np.clip(cos_angle, -1.0, 1.0)))
                
                return angle
        except:
            pass
        return None
    
    def calculate_balance(self, landmarks):
        """Calculate balance score"""
        try:
            left_ankle = landmarks[27]
            right_ankle = landmarks[28]
            left_hip = landmarks[23]
            right_hip = landmarks[24]
            
            if all(point['visibility'] > 0.5 for point in [left_ankle, right_ankle, left_hip, right_hip]):
                com_x = (left_hip['x'] + right_hip['x']) / 2
                support_center = (left_ankle['x'] + right_ankle['x']) / 2
                balance_distance = abs(com_x - support_center)
                balance_score = max(0, 1 - balance_distance * 10)
                
                return balance_score
        except:
            pass
        return None
    
    def calculate_smoothness(self, landmarks):
        """Calculate movement smoothness"""
        return 0.8  # Simplified
