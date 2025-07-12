# Real-time Audio Analysis Pipeline

A production-grade Python tool for capturing system-level audio and rendering dynamic visualizations in real-time.
<img width="756" height="609" alt="Picture2" src="https://github.com/user-attachments/assets/1a9ff952-04b0-4f23-b5c5-feabb5496e59" />

------------
# 🎧 Live Audio Intelligence

This professional audio analysis pipeline captures system audio output (music, media, applications) and processes it in real-time to generate dynamic visualizations. Built with a modular architecture, it's designed for extensibility and future AI agent integration.

---

## 📺 Demo Video

Watch a full demonstration of the system in action on YouTube:

▶️ [Live Audio Intelligence – Real-Time Audio Visualization](https://www.youtube.com/watch?v=a_DosUgpz_o&list=PLi_I8xIMzFIChxZPtnJY48297-P7C0q0m)

Or explore the full playlist here:  
📂 [YouTube Playlist](https://www.youtube.com/playlist?list=PLi_I8xIMzFIChxZPtnJY48297-P7C0q0m)

---

## 🔖 Features

- 🎵 Capture system audio output in real-time  
- 📊 Live visual feedback with customizable graphs  
- ⚙️ Modular architecture for easy AI agent plug-ins  
- 🧠 Designed for integration with GPT and other AI models  
- ⏱ Ultra-low latency processing

---

## 📌 Hashtags



## Features

- **System Audio Capture**: Loopback audio capture across Windows, macOS, Linux
- **Real-time Visualizations**: 
  - Waveform display
  - FFT frequency spectrum
  - Spectrogram view
- **Device Management**: Auto-detection with manual device selection
- **Modular Architecture**: Ready for AI agent integration
- **Performance Optimized**: Low-latency streaming with efficient rendering

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# List available audio devices
python main.py --list-devices

# Start with auto-detection
python main.py

# Use specific device
python main.py --device 5

# Save audio while analyzing
python main.py --save-audio
```

## Controls

During visualization:
- `w` - Switch to waveform view
- `f` - Switch to FFT spectrum view
- `s` - Switch to spectrogram view
- `Ctrl+C` - Quit application

## Architecture

- `audio_engine.py` - Core audio capture and device management
- `visualizer.py` - Real-time visualization with mode switching
- `main.py` - CLI interface and application orchestration

## System Requirements

- Python 3.9+
- Audio loopback capability (Stereo Mix on Windows, Soundflower on macOS)

## Future Extensions

The modular design supports:
- Audio feature extraction (pitch, tempo, chroma)
- ML dataset generation
- AI agent triggers based on audio events
- Real-time onset/beat detection
- External API integrations
