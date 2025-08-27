# app.py - COMPLETE STREAMLIT APP WITH VIDEO FIX
import streamlit as st
import tempfile
import os
from pathlib import Path
import json
from cover_drive_analysis_realtime import CoverDriveAnalyzer
import cv2
import subprocess

st.set_page_config(
    page_title="AthleteRise - Cricket Analytics",
    page_icon="🏏",
    layout="wide"
)

def convert_video_for_browser(input_path):
    """Convert video to browser-compatible format"""
    if not os.path.exists(input_path):
        return None
        
    output_path = input_path.replace('.mp4', '_web.mp4')
    
    try:
        # Try to convert with ffmpeg if available
        cmd = [
            'ffmpeg', '-i', input_path,
            '-vcodec', 'libx264',
            '-preset', 'fast',
            '-crf', '22',
            '-movflags', '+faststart',  # Web optimization
            output_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0 and os.path.exists(output_path):
            return output_path
    except:
        pass
    
    # If ffmpeg fails, just return original
    return input_path

def main():
    st.title("🏏 AthleteRise - AI-Powered Cricket Analytics")
    st.subheader("Real-Time Cover Drive Analysis")
    
    # Add info about video preview
    st.info("💡 **Note**: If video preview shows black screen, use the Download button - the analysis still works perfectly!")
    
    # Sidebar
    st.sidebar.title("Analysis Options")
    
    # File upload
    uploaded_file = st.file_uploader(
        "Upload Cricket Video", 
        type=['mp4', 'avi', 'mov', 'mkv'],
        help="Upload a cricket video for cover drive analysis"
    )
    
    # URL input
    st.sidebar.subheader("Or analyze from URL")
    video_url = st.sidebar.text_input(
        "YouTube URL", 
        value="https://youtube.com/shorts/vSX3IRxGnNY",
        help="Enter YouTube video URL"
    )
    
    use_url = st.sidebar.checkbox("Use URL instead of upload")
    
    if st.button("🔍 Analyze Shot", type="primary"):
        if use_url and video_url:
            analyze_from_url(video_url)
        elif uploaded_file:
            analyze_uploaded_file(uploaded_file)
        else:
            st.error("Please upload a file or provide a URL")

def analyze_from_url(url):
    """Analyze video from URL"""
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    with st.spinner("🏏 Analyzing cricket shot..."):
        try:
            analyzer = CoverDriveAnalyzer()
            
            # Download and analyze
            status_text.text("📥 Downloading video...")
            progress_bar.progress(25)
            
            video_path = analyzer.download_video(url)
            
            if video_path:
                status_text.text("⚡ Processing video...")
                progress_bar.progress(50)
                
                results = analyzer.analyze_video(video_path)
                
                progress_bar.progress(75)
                status_text.text("🎯 Generating results...")
                
                display_results(results)
                
                progress_bar.progress(100)
                status_text.text("✅ Analysis complete!")
                
                # Cleanup
                if os.path.exists(video_path):
                    os.remove(video_path)
            else:
                st.error("Failed to download video. Please try a different URL or upload a file.")
                
        except Exception as e:
            st.error(f"Analysis failed: {str(e)}")
            st.info("💡 Try uploading a local video file instead!")

def analyze_uploaded_file(uploaded_file):
    """Analyze uploaded video file"""
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    with st.spinner("🏏 Analyzing cricket shot..."):
        try:
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
                tmp_file.write(uploaded_file.read())
                tmp_path = tmp_file.name
            
            progress_bar.progress(25)
            status_text.text("📹 Processing your video...")
            
            analyzer = CoverDriveAnalyzer()
            results = analyzer.analyze_video(tmp_path)
            
            progress_bar.progress(75)
            status_text.text("🎯 Analyzing technique...")
            
            display_results(results)
            
            progress_bar.progress(100)
            status_text.text("✅ Analysis complete!")
            
            # Cleanup
            os.unlink(tmp_path)
            
        except Exception as e:
            st.error(f"Analysis failed: {str(e)}")
            st.info("💡 Make sure your video shows a clear view of the cricket player!")

def display_results(results):
    """Display analysis results with fixed video preview"""
    st.success("✅ Analysis Complete!")
    
    # Display stats
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Frames Processed", results['stats']['total_frames'])
    
    with col2:
        st.metric("Processing Time", f"{results['stats']['processing_time']:.1f}s")
    
    with col3:
        st.metric("Average FPS", f"{results['stats']['avg_fps']:.1f}")
    
    # Display scores
    st.subheader("📊 Shot Analysis Scores")
    
    evaluation = results['evaluation']
    
    # Overall score
    overall_score = evaluation['overall_score']
    score_color = "green" if overall_score >= 7 else "orange" if overall_score >= 5 else "red"
    
    st.markdown(f"""
    <div style="text-align: center; padding: 20px; border-radius: 10px; background-color: {score_color}; color: white; margin: 10px 0;">
        <h2>Overall Score: {overall_score}/10</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Category scores
    scores_col1, scores_col2 = st.columns(2)
    
    categories = list(evaluation['scores'].items())
    
    with scores_col1:
        for category, data in categories[:3]:
            score = data['score']
            feedback = data['feedback']
            
            # Color based on score
            if score >= 8:
                color = "#4CAF50"  # Green
            elif score >= 6:
                color = "#FF9800"  # Orange
            else:
                color = "#F44336"  # Red
            
            st.markdown(f"""
            <div style="border: 2px solid {color}; padding: 15px; margin: 10px 0; border-radius: 10px; background-color: {color}20;">
                <h4 style="color: {color}; margin: 0;">{category.replace('_', ' ').title()}</h4>
                <p style="font-size: 18px; margin: 5px 0;"><strong>Score: {score}/10</strong></p>
                <p style="margin: 0; font-size: 14px;">{feedback}</p>
            </div>
            """, unsafe_allow_html=True)
    
    with scores_col2:
        for category, data in categories[3:]:
            score = data['score']
            feedback = data['feedback']
            
            # Color based on score
            if score >= 8:
                color = "#4CAF50"  # Green
            elif score >= 6:
                color = "#FF9800"  # Orange
            else:
                color = "#F44336"  # Red
            
            st.markdown(f"""
            <div style="border: 2px solid {color}; padding: 15px; margin: 10px 0; border-radius: 10px; background-color: {color}20;">
                <h4 style="color: {color}; margin: 0;">{category.replace('_', ' ').title()}</h4>
                <p style="font-size: 18px; margin: 5px 0;"><strong>Score: {score}/10</strong></p>
                <p style="margin: 0; font-size: 14px;">{feedback}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Recommendations
    st.subheader("💡 Coaching Recommendations")
    for i, rec in enumerate(evaluation['recommendations'], 1):
        st.write(f"{i}. {rec}")
    
    # Download options
    st.subheader("📥 Download Results")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if os.path.exists(results['output_video']):
            with open(results['output_video'], 'rb') as f:
                st.download_button(
                    "📹 Download Annotated Video",
                    f.read(),
                    file_name="annotated_cricket_analysis.mp4",
                    mime="video/mp4"
                )
    
    with col2:
        eval_json = json.dumps(evaluation, indent=2)
        st.download_button(
            "📄 Download Analysis Report",
            eval_json,
            file_name="cricket_analysis_report.json",
            mime="application/json"
        )
    
    # Video preview with better error handling
    st.subheader("🎬 Annotated Video Preview")
    
    if os.path.exists(results['output_video']):
        # Try to convert for browser compatibility
        web_video = convert_video_for_browser(results['output_video'])
        
        try:
            st.video(web_video)
        except Exception as e:
            st.warning("⚠️ Video preview unavailable (codec issue)")
            st.info("📹 **The analysis worked perfectly!** Use the Download button above to get your annotated video.")
            
            # Show video info instead
            cap = cv2.VideoCapture(results['output_video'])
            if cap.isOpened():
                fps = cap.get(cv2.CAP_PROP_FPS)
                frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
                duration = frame_count / fps
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                cap.release()
                
                st.info(f"📊 **Video Details:** {width}x{height}, {fps:.1f} FPS, {duration:.1f}s duration")
    else:
        st.error("Video file not found")

if __name__ == "__main__":
    main()
