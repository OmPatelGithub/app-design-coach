#!/usr/bin/env python3
"""
Video Frame Extractor for Figma Assets

This script extracts sufficiently different frames from a video file.
Perfect for converting screen recordings into Figma-ready screenshots.
"""

import argparse
import cv2
import numpy as np
import os
from pathlib import Path
from datetime import datetime


class FrameExtractor:
    def __init__(self, video_path, output_dir='figma', similarity_threshold=0.95, 
                 min_frame_interval=30, quality=95):
        """
        Initialize the frame extractor.
        
        Args:
            video_path: Path to the input video file
            output_dir: Directory to save extracted frames
            similarity_threshold: Threshold for frame similarity (0-1, higher = more similar)
            min_frame_interval: Minimum frames between extractions (prevents rapid captures)
            quality: PNG output quality (0-100, higher = better quality)
        """
        self.video_path = video_path
        self.output_dir = Path(output_dir)
        self.similarity_threshold = similarity_threshold
        self.min_frame_interval = min_frame_interval
        self.quality = quality
        self.frame_count = 0
        self.saved_count = 0
        
    def calculate_similarity(self, frame1, frame2):
        """
        Calculate similarity between two frames using structural similarity.
        
        Returns a value between 0 (completely different) and 1 (identical).
        """
        # Resize frames to a smaller size for faster comparison
        size = (320, 180)
        frame1_small = cv2.resize(frame1, size)
        frame2_small = cv2.resize(frame2, size)
        
        # Convert to grayscale
        gray1 = cv2.cvtColor(frame1_small, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(frame2_small, cv2.COLOR_BGR2GRAY)
        
        # Calculate normalized cross-correlation
        # This is faster than SSIM and works well for screen recordings
        result = cv2.matchTemplate(gray1, gray2, cv2.TM_CCOEFF_NORMED)
        similarity = result[0][0]
        
        return similarity
    
    def extract_frames(self):
        """
        Extract frames from the video file.
        """
        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Open video file
        cap = cv2.VideoCapture(str(self.video_path))
        
        if not cap.isOpened():
            raise ValueError(f"Could not open video file: {self.video_path}")
        
        # Get video properties
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total_frames / fps if fps > 0 else 0
        
        print(f"Video properties:")
        print(f"  FPS: {fps:.2f}")
        print(f"  Total frames: {total_frames}")
        print(f"  Duration: {duration:.2f} seconds")
        print(f"  Output directory: {self.output_dir.absolute()}")
        print(f"\nExtracting frames with similarity threshold: {self.similarity_threshold}")
        print(f"Minimum frame interval: {self.min_frame_interval} frames ({self.min_frame_interval/fps:.2f} seconds)\n")
        
        previous_frame = None
        frames_since_last_save = 0
        
        while True:
            ret, frame = cap.read()
            
            if not ret:
                break
            
            self.frame_count += 1
            frames_since_last_save += 1
            
            # Check if we should consider this frame
            should_save = False
            
            if previous_frame is None:
                # Always save the first frame
                should_save = True
                reason = "first frame"
            elif frames_since_last_save < self.min_frame_interval:
                # Skip frames that are too close to the last saved frame
                should_save = False
            else:
                # Calculate similarity with the previous saved frame
                similarity = self.calculate_similarity(frame, previous_frame)
                
                if similarity < self.similarity_threshold:
                    should_save = True
                    reason = f"different (similarity: {similarity:.3f})"
                else:
                    should_save = False
            
            if should_save:
                # Save the frame
                timestamp = self.frame_count / fps if fps > 0 else self.frame_count
                filename = f"frame_{self.saved_count:04d}_t{timestamp:.2f}s.png"
                filepath = self.output_dir / filename
                
                cv2.imwrite(str(filepath), frame, [cv2.IMWRITE_PNG_COMPRESSION, 3])
                
                print(f"Saved: {filename} ({reason})")
                
                previous_frame = frame.copy()
                self.saved_count += 1
                frames_since_last_save = 0
            
            # Show progress
            if self.frame_count % 100 == 0:
                progress = (self.frame_count / total_frames) * 100
                print(f"Progress: {progress:.1f}% ({self.frame_count}/{total_frames} frames processed)")
        
        cap.release()
        
        print(f"\n✓ Extraction complete!")
        print(f"  Processed: {self.frame_count} frames")
        print(f"  Saved: {self.saved_count} unique frames")
        print(f"  Output directory: {self.output_dir.absolute()}")


def main():
    parser = argparse.ArgumentParser(
        description='Extract sufficiently different frames from a video file.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage (extract frames to 'figma' folder)
  python extract_frames.py video.mp4
  
  # Custom output directory
  python extract_frames.py video.mp4 -o screenshots
  
  # More sensitive to changes (captures more frames)
  python extract_frames.py video.mp4 -s 0.90
  
  # Less sensitive to changes (captures fewer frames)
  python extract_frames.py video.mp4 -s 0.98
  
  # Adjust minimum time between captures (in frames)
  python extract_frames.py video.mp4 -i 60
        """
    )
    
    parser.add_argument('video', help='Path to the input video file')
    parser.add_argument('-o', '--output', default='figma', 
                        help='Output directory (default: figma)')
    parser.add_argument('-s', '--similarity', type=float, default=0.95,
                        help='Similarity threshold 0-1 (default: 0.95, higher = more selective)')
    parser.add_argument('-i', '--interval', type=int, default=30,
                        help='Minimum frames between captures (default: 30)')
    parser.add_argument('-q', '--quality', type=int, default=95,
                        help='Output image quality 0-100 (default: 95)')
    
    args = parser.parse_args()
    
    # Validate inputs
    if not os.path.exists(args.video):
        print(f"Error: Video file not found: {args.video}")
        return 1
    
    if not 0 <= args.similarity <= 1:
        print("Error: Similarity threshold must be between 0 and 1")
        return 1
    
    if args.interval < 0:
        print("Error: Frame interval must be non-negative")
        return 1
    
    # Extract frames
    try:
        extractor = FrameExtractor(
            video_path=args.video,
            output_dir=args.output,
            similarity_threshold=args.similarity,
            min_frame_interval=args.interval,
            quality=args.quality
        )
        extractor.extract_frames()
        return 0
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    exit(main())
