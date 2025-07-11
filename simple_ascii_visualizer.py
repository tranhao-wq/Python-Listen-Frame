"""
Simple ASCII Visualizer - Instant Response to Music
"""
import numpy as np
import sounddevice as sd
import threading
import time
import os
import random

class SimpleASCIIVisualizer:
    def __init__(self):
        self.sample_rate = 22050
        self.buffer_size = 512
        self.energy = 0
        self.beat = False
        self.lock = threading.Lock()
        self.running = True
        
        # ASCII characters for different energy levels
        self.ascii_chars = {
            'low': ['░', '▒', '▓'],
            'mid': ['♪', '♫', '♬', '♩'],
            'high': ['★', '☆', '✦', '✧'],
            'beat': ['🔥', '⚡', '💥', '✨']
        }
        
        # Simple patterns
        self.patterns = [
            "    ♪♫♪♫♪♫♪♫    ",
            "  ★☆★☆★☆★☆★☆  ",
            "░▒▓█████████▓▒░",
            "♬♩♪♫♪♫♪♩♬♩♪♫",
            "✦✧✦✧✦✧✦✧✦✧✦✧"
        ]
    
    def audio_callback(self, indata, frames, time, status):
        """Process audio instantly"""
        mono = np.mean(indata, axis=1) if indata.shape[1] > 1 else indata[:, 0]
        
        # Quick energy calculation
        energy = np.mean(mono ** 2)
        beat = energy > 0.01  # Lower threshold for sensitivity
        
        with self.lock:
            self.energy = energy
            self.beat = beat
    
    def draw_ascii_art(self):
        """Draw ASCII art based on current audio"""
        with self.lock:
            energy = self.energy
            beat = self.beat
        
        # Clear screen
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("*** SIMPLE ASCII MUSIC VISUALIZER ***")
        print("=" * 50)
        
        # Energy bar
        bar_length = int(energy * 50)
        energy_bar = "#" * bar_length + "." * (50 - bar_length)
        print(f"Energy: [{energy_bar}] {energy:.4f}")
        
        # Beat indicator
        beat_indicator = "*** BEAT DETECTED! ***" if beat else "... Waiting for beat..."
        print(f"Status: {beat_indicator}")
        print()
        
        # ASCII Art based on energy level
        if beat and energy > 0.05:
            # Strong beat - explosive pattern
            pattern = random.choice([
                "***!!!***!!!***!!!***!!!",
                "+++===+++===+++===+++===",
                "###@@@###@@@###@@@###@@@"
            ])
        elif energy > 0.02:
            # Medium energy - musical notes
            pattern = random.choice([
                "~-~-~-~-~-~-~-~-~-~-~-~-",
                "o0o0o0o0o0o0o0o0o0o0o0o0",
                "^v^v^v^v^v^v^v^v^v^v^v^v"
            ])
        elif energy > 0.005:
            # Low energy - simple blocks
            pattern = ".,;:" * int(energy * 1000) + "." * (16 - int(energy * 1000))
        else:
            # Very low - dots
            pattern = "." * 16
        
        # Draw multiple lines of pattern
        for i in range(8):
            # Rotate pattern for animation effect
            rotated = pattern[i:] + pattern[:i]
            print(f"    {rotated}")
        
        print()
        print(f"[AUDIO] Listening... Energy: {energy:.6f}")
        print("Press Ctrl+C to stop")
    
    def start(self):
        """Start the visualizer"""
        print("Starting Simple ASCII Visualizer...")
        print("Make sure Stereo Mix is enabled!")
        
        try:
            # Find audio device
            devices = sd.query_devices()
            device_id = None
            
            for i, device in enumerate(devices):
                if 'stereo mix' in device['name'].lower():
                    device_id = i
                    print(f"Using device: {device['name']}")
                    break
            
            if device_id is None:
                print("Warning: Stereo Mix not found, using default device")
            
            # Start audio stream
            with sd.InputStream(device=device_id,
                              channels=1,
                              samplerate=self.sample_rate,
                              blocksize=self.buffer_size,
                              callback=self.audio_callback,
                              dtype=np.float32):
                
                # Main visualization loop
                while self.running:
                    self.draw_ascii_art()
                    time.sleep(0.1)  # Update 10 times per second
                    
        except KeyboardInterrupt:
            print("\nVisualizer stopped!")
            self.running = False
        except Exception as e:
            print(f"Error: {e}")

def main():
    visualizer = SimpleASCIIVisualizer()
    visualizer.start()

if __name__ == "__main__":
    main()