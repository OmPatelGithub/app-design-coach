# Figma Asset Maker - Video Frame Extractor

Extract sufficiently different frames from video files to create screenshots perfect for Figma. Ideal for converting screen recordings of app onboarding flows into individual screenshots.

## Features

- 🎬 **Universal Video Support** - Works with any video format supported by OpenCV (MP4, MOV, AVI, MKV, etc.)
- 🎯 **Smart Frame Detection** - Automatically detects and extracts only sufficiently different frames
- ⚡ **Fast Processing** - Optimized similarity detection using normalized cross-correlation
- 🎨 **High Quality Output** - Saves frames as PNG images with excellent quality
- ⚙️ **Configurable** - Adjust sensitivity, timing, and output settings
- 📊 **Progress Tracking** - Real-time progress updates during extraction

## Installation

1. Make sure you have Python 3.7+ installed
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Quick Start

Basic usage - extract frames from a video:

```bash
python extract_frames.py your_video.mp4
```

This will create a `figma` folder with all the extracted frames.

## Usage Examples

### Basic Usage
```bash
# Extract frames to default 'figma' folder
python extract_frames.py onboarding_recording.mp4
```

### Custom Output Directory
```bash
# Save frames to a custom folder
python extract_frames.py video.mp4 -o screenshots
```

### Adjust Sensitivity
```bash
# More sensitive (captures more frames, even small changes)
python extract_frames.py video.mp4 -s 0.90

# Less sensitive (only captures significant changes)
python extract_frames.py video.mp4 -s 0.98
```

### Control Capture Rate
```bash
# Wait at least 60 frames between captures (about 2 seconds at 30fps)
python extract_frames.py video.mp4 -i 60

# Capture more frequently (15 frames, about 0.5 seconds at 30fps)
python extract_frames.py video.mp4 -i 15
```

### Combine Options
```bash
# Custom settings for optimal onboarding screenshot extraction
python extract_frames.py onboarding.mp4 -o onboarding_screens -s 0.93 -i 45
```

## Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `video` | Path to input video file (required) | - |
| `-o, --output` | Output directory for frames | `figma` |
| `-s, --similarity` | Similarity threshold (0-1, higher = more selective) | `0.95` |
| `-i, --interval` | Minimum frames between captures | `30` |
| `-q, --quality` | Output image quality (0-100) | `95` |

## Understanding the Parameters

### Similarity Threshold (`-s`)
- **0.90-0.93**: Captures many frames, even subtle changes (good for detailed walkthroughs)
- **0.94-0.96**: Balanced - captures significant changes (recommended for most use cases)
- **0.97-0.99**: Very selective - only major scene changes (good for summarizing long videos)

### Frame Interval (`-i`)
- Prevents capturing too many similar frames in rapid succession
- For 30fps video:
  - `15` frames = 0.5 seconds minimum between captures
  - `30` frames = 1 second minimum (default)
  - `60` frames = 2 seconds minimum
  - `90` frames = 3 seconds minimum

## Output

The script creates PNG images with filenames like:
```
frame_0000_t0.00s.png
frame_0001_t2.45s.png
frame_0002_t5.12s.png
```

Where:
- `0000` is the sequence number
- `t2.45s` is the timestamp in the original video

## Tips for Best Results

### For Onboarding Flows
```bash
python extract_frames.py onboarding.mp4 -s 0.94 -i 45
```
This captures clear screen transitions without duplicates.

### For Tutorial Videos
```bash
python extract_frames.py tutorial.mp4 -s 0.92 -i 30
```
This captures more frames to show intermediate steps.

### For Demo Videos
```bash
python extract_frames.py demo.mp4 -s 0.96 -i 60
```
This only captures major scene changes.

## Troubleshooting

### "Could not open video file"
- Check that the video file exists and the path is correct
- Ensure the video format is supported by OpenCV
- Try converting the video to MP4 format

### Too many frames extracted
- Increase the similarity threshold: `-s 0.97`
- Increase the frame interval: `-i 60`

### Too few frames extracted
- Decrease the similarity threshold: `-s 0.92`
- Decrease the frame interval: `-i 15`

### Out of memory
- The script processes videos efficiently
- If you encounter issues with very large videos, try processing smaller segments

## Requirements

- Python 3.7 or higher
- OpenCV (opencv-python)
- NumPy

## License

MIT — see [LICENSE](./LICENSE).
