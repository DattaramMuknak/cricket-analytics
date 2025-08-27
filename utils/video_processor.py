# utils/video_processor.py - COMPLETE FILE
import cv2
import numpy as np
from utils.pose_detector import PoseDetector

class VideoProcessor:
    def __init__(self):
        self.pose_detector = PoseDetector()
        
    def add_overlays(self, frame, pose_results, metrics, frame_number):
        """Add all overlays to frame"""
        # Draw pose skeleton
        frame = self.pose_detector.draw_landmarks(frame, pose_results['pose_landmarks'])
        
        # Add metrics overlay
        frame = self.add_metrics_overlay(frame, metrics)
        
        # Add feedback overlay
        frame = self.add_feedback_overlay(frame, metrics)
        
        # Add frame info
        frame = self.add_frame_info(frame, frame_number)
        
        return frame
    
    def add_metrics_overlay(self, frame, metrics):
        """Add real-time metrics display"""
        overlay_y = 30
        
        # Background for metrics
        cv2.rectangle(frame, (10, 10), (400, 200), (0, 0, 0), -1)
        cv2.rectangle(frame, (10, 10), (400, 200), (255, 255, 255), 2)
        
        # Title
        cv2.putText(frame, "LIVE METRICS", (20, overlay_y), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        overlay_y += 35
        
        # Display metrics
        if metrics['elbow_angle'] is not None:
            cv2.putText(frame, f"Elbow Angle: {metrics['elbow_angle']:.1f}°", 
                       (20, overlay_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            overlay_y += 25
        
        if metrics['spine_lean'] is not None:
            cv2.putText(frame, f"Spine Lean: {metrics['spine_lean']:.1f}°", 
                       (20, overlay_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            overlay_y += 25
        
        if metrics['head_knee_alignment'] is not None:
            cv2.putText(frame, f"Head-Knee Dist: {metrics['head_knee_alignment']:.3f}", 
                       (20, overlay_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            overlay_y += 25
        
        if metrics['balance_score'] is not None:
            cv2.putText(frame, f"Balance: {metrics['balance_score']:.2f}", 
                       (20, overlay_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        return frame
    
    def add_feedback_overlay(self, frame, metrics):
        """Add real-time feedback"""
        feedback_y = 250
        
        if metrics['elbow_angle'] is not None:
            if 110 <= metrics['elbow_angle'] <= 140:
                cv2.putText(frame, "✅ Good elbow elevation", 
                           (20, feedback_y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            else:
                cv2.putText(frame, "❌ Check elbow position", 
                           (20, feedback_y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            feedback_y += 30
        
        if metrics['head_knee_alignment'] is not None:
            if metrics['head_knee_alignment'] < 0.05:
                cv2.putText(frame, "✅ Head over front knee", 
                           (20, feedback_y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            else:
                cv2.putText(frame, "❌ Head not over front knee", 
                           (20, feedback_y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        
        return frame
    
    def add_frame_info(self, frame, frame_number):
        """Add frame info"""
        timestamp = frame_number / 30.0
        cv2.putText(frame, f"Frame: {frame_number} | Time: {timestamp:.2f}s", 
                   (frame.shape[1] - 300, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
        return frame
    
    def add_no_detection_overlay(self, frame):
        """Add overlay when no pose detected"""
        cv2.putText(frame, "No pose detected", 
                   (frame.shape[1]//2 - 100, frame.shape[0]//2), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        return frame
