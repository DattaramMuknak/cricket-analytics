# cover_drive_analysis_realtime.py - COMPLETE UPDATED VERSION
import cv2
import json
import time
import numpy as np
from pathlib import Path
from utils.pose_detector import PoseDetector
from utils.biomechanics import BiomechanicsAnalyzer
from utils.video_processor import VideoProcessor
from utils.evaluator import ShotEvaluator
from config.settings import Config
import yt_dlp
import os

class CoverDriveAnalyzer:
    def __init__(self):
        self.config = Config()
        self.pose_detector = PoseDetector()
        self.biomechanics = BiomechanicsAnalyzer()
        self.video_processor = VideoProcessor()
        self.evaluator = ShotEvaluator()
        
        # Create output directory
        Path(self.config.OUTPUT_DIR).mkdir(exist_ok=True)
        
    def download_video(self, url):
        """Download video from YouTube with latest fixes"""
        try:
            ydl_opts = {
                'format': 'best[height<=720]',
                'outtmpl': 'input_video.%(ext)s',
                
                # Latest user agent and headers
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
                },
                
                # Updated extractor args for 2025
                'extractor_args': {
                    'youtube': {
                        'player_client': ['android', 'web', 'ios'],
                        'skip': ['dash', 'hls'],
                        'player_skip': ['configs'],
                    }
                },
                
                # Enhanced retry settings
                'retries': 10,
                'fragment_retries': 10,
                'extract_flat': False,
                'writesubtitles': False,
                'writeautomaticsub': False,
                
                # Additional fixes for 403 errors
                'cookiefile': None,
                'source_address': '0.0.0.0',
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                
            # Find downloaded file
            for ext in ['mp4', 'webm', 'mkv', 'flv']:
                if os.path.exists(f'input_video.{ext}'):
                    return f'input_video.{ext}'
            
            raise FileNotFoundError("Downloaded video not found")
            
        except Exception as e:
            print(f"Error downloading video: {e}")
            return None
    
    def analyze_video(self, video_path):
        """Main analysis function with browser-compatible video output"""
        print("🏏 Starting Cricket Cover Drive Analysis...")
        
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError(f"Cannot open video: {video_path}")
        
        # Get video properties
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        # Setup output video writer with H.264 codec (browser-compatible)
        fourcc = cv2.VideoWriter_fourcc(*'H264')
        output_path = os.path.join(self.config.OUTPUT_DIR, 'annotated_video.mp4')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        # If H.264 doesn't work, try MJPG
        if not out.isOpened():
            fourcc = cv2.VideoWriter_fourcc(*'MJPG')
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        # If MJPG doesn't work, try XVID
        if not out.isOpened():
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        # Initialize tracking variables
        frame_metrics = []
        frame_count = 0
        start_time = time.time()
        
        print(f"📹 Processing {total_frames} frames at {fps} FPS...")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_count += 1
            
            # Pose detection
            pose_results = self.pose_detector.detect(frame)
            
            if pose_results:
                # Biomechanical analysis
                metrics = self.biomechanics.analyze_frame(pose_results, frame_count)
                frame_metrics.append(metrics)
                
                # Add overlays
                frame = self.video_processor.add_overlays(
                    frame, pose_results, metrics, frame_count
                )
            else:
                # Handle missing detection
                frame = self.video_processor.add_no_detection_overlay(frame)
            
            # Write frame
            out.write(frame)
            
            # Progress update
            if frame_count % 30 == 0:  # Every second at 30fps
                progress = (frame_count / total_frames) * 100
                print(f"⚡ Progress: {progress:.1f}%")
        
        # Cleanup
        cap.release()
        out.release()
        
        # Calculate processing stats
        end_time = time.time()
        processing_time = end_time - start_time
        avg_fps = frame_count / processing_time
        
        print(f"✅ Processing complete!")
        print(f"📊 Processed {frame_count} frames in {processing_time:.2f}s")
        print(f"🚀 Average FPS: {avg_fps:.2f}")
        
        # Generate evaluation
        evaluation = self.evaluator.evaluate_shot(frame_metrics)
        
        # Save evaluation
        eval_path = os.path.join(self.config.OUTPUT_DIR, 'evaluation.json')
        with open(eval_path, 'w') as f:
            json.dump(evaluation, f, indent=2)
        
        return {
            'output_video': output_path,
            'evaluation': evaluation,
            'stats': {
                'total_frames': frame_count,
                'processing_time': processing_time,
                'avg_fps': avg_fps
            }
        }

def main():
    # Video URL to analyze
    video_url = "https://youtube.com/shorts/vSX3IRxGnNY"
    
    analyzer = CoverDriveAnalyzer()
    
    # Download video
    print("📥 Downloading video...")
    video_path = analyzer.download_video(video_url)
    
    if video_path:
        # Analyze video
        results = analyzer.analyze_video(video_path)
        
        print("\n🎯 Analysis Results:")
        print(f"📄 Evaluation saved to: output/evaluation.json")
        print(f"🎬 Annotated video saved to: {results['output_video']}")
        
        # Print summary scores
        evaluation = results['evaluation']
        print(f"\n📊 Shot Scores:")
        for category, data in evaluation['scores'].items():
            print(f"  {category}: {data['score']}/10 - {data['feedback']}")
        
        # Cleanup
        if os.path.exists(video_path):
            os.remove(video_path)
    else:
        print("❌ Failed to download video")

if __name__ == "__main__":
    main()
