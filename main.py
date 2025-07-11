"""
Real-time Audio Analysis Pipeline
Production-grade tool for system audio capture and visualization
"""
import argparse
import sys
import time
import numpy as np
from pathlib import Path
try:
    import soundfile as sf
    HAS_SOUNDFILE = True
except ImportError:
    HAS_SOUNDFILE = False
    print("Warning: soundfile not available - audio recording disabled")

from audio_engine import AudioEngine
from visualizer import AudioVisualizer


class AudioAnalyzer:
    def __init__(self, sample_rate: int = 44100, buffer_size: int = 1024):
        self.sample_rate = sample_rate
        self.buffer_size = buffer_size
        
        self.audio_engine = AudioEngine(sample_rate, buffer_size)
        self.visualizer = AudioVisualizer(sample_rate)
        
        # Optional recording
        self.recording = False
        self.recorded_data = []
        
    def list_devices(self):
        """List available audio devices"""
        print("\nAvailable Audio Devices:")
        print("-" * 50)
        devices = self.audio_engine.list_devices()
        
        for device_id, name, is_loopback in devices:
            marker = " [LOOPBACK]" if is_loopback else ""
            print(f"{device_id:2d}: {name}{marker}")
        
        print("-" * 50)
        return devices
    
    def start_analysis(self, device_id=None, save_audio=False):
        """Start real-time audio analysis"""
        print("Starting Real-time Audio Analysis...")
        print("Controls: w=waveform, f=FFT, s=spectrogram, Ctrl+C=quit")
        
        # Setup recording if requested
        if save_audio:
            self.recording = True
            self.recorded_data = []
            print("Audio recording enabled - will save to 'recorded_audio.wav'")
        
        # Start audio capture
        if not self.audio_engine.start_capture(device_id):
            print("Failed to start audio capture")
            return False
        
        # Setup data flow: audio_engine -> visualizer
        def data_callback(audio_chunk):
            # Update visualizer
            current_data = self.audio_engine.get_audio_data()
            self.visualizer.update_data(current_data)
            
            # Record if enabled
            if self.recording:
                self.recorded_data.extend(audio_chunk)
        
        self.audio_engine.set_data_callback(data_callback)
        
        try:
            # Start visualization (blocking)
            self.visualizer.start_visualization()
        except KeyboardInterrupt:
            print("\nShutting down...")
        finally:
            self.cleanup(save_audio)
        
        return True
    
    def cleanup(self, save_audio=False):
        """Clean shutdown"""
        self.audio_engine.stop_capture()
        self.visualizer.stop_visualization()
        
        # Save recorded audio if enabled
        if save_audio and self.recorded_data and HAS_SOUNDFILE:
            try:
                audio_array = np.array(self.recorded_data, dtype=np.float32)
                sf.write('recorded_audio.wav', audio_array, self.sample_rate)
                print(f"Saved {len(audio_array)/self.sample_rate:.1f}s of audio to 'recorded_audio.wav'")
            except Exception as e:
                print(f"Failed to save audio: {e}")
        elif save_audio and not HAS_SOUNDFILE:
            print("Cannot save audio: soundfile library not installed")


def main():
    parser = argparse.ArgumentParser(
        description="Real-time Audio Analysis Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                    # Auto-detect loopback device
  python main.py --list-devices     # List available devices
  python main.py --device 5         # Use specific device
  python main.py --save-audio       # Save audio to file
  python main.py --sample-rate 48000 # Custom sample rate

Controls during visualization:
  w = Switch to waveform view
  f = Switch to FFT spectrum view  
  s = Switch to spectrogram view
  Ctrl+C = Quit application
        """
    )
    
    parser.add_argument('--list-devices', action='store_true',
                       help='List available audio devices and exit')
    parser.add_argument('--device', type=int, metavar='ID',
                       help='Audio device ID to use (see --list-devices)')
    parser.add_argument('--sample-rate', type=int, default=44100,
                       help='Sample rate in Hz (default: 44100)')
    parser.add_argument('--buffer-size', type=int, default=1024,
                       help='Buffer size in samples (default: 1024)')
    parser.add_argument('--save-audio', action='store_true',
                       help='Save captured audio to recorded_audio.wav')
    
    args = parser.parse_args()
    
    # Create analyzer
    analyzer = AudioAnalyzer(args.sample_rate, args.buffer_size)
    
    # List devices and exit if requested
    if args.list_devices:
        analyzer.list_devices()
        return
    
    # Validate device if specified
    if args.device is not None:
        devices = analyzer.list_devices()
        device_ids = [d[0] for d in devices]
        if args.device not in device_ids:
            print(f"Error: Device ID {args.device} not found")
            return
    
    # Start analysis
    try:
        success = analyzer.start_analysis(args.device, args.save_audio)
        if not success:
            print("Failed to start audio analysis")
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()