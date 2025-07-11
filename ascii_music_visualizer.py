"""
ASCII Music Visualizer - AI-Powered Visual Art Generator
Creates ASCII art and images that react to music
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sounddevice as sd
import threading
import random
import time
from matplotlib.patches import Rectangle
import matplotlib.image as mpimg

class ASCIIMusicVisualizer:
    def __init__(self):
        self.sample_rate = 22050
        self.buffer_size = 512
        self.audio_data = np.zeros(1024)
        self.lock = threading.Lock()
        
        # Audio analysis
        self.energy = 0
        self.beat = False
        self.frequency_bands = np.zeros(8)  # 8 frequency bands
        
        # ASCII art patterns
        self.ascii_patterns = {
            'low': [
                "░░░░░░░░░░",
                "▒▒▒▒▒▒▒▒▒▒", 
                "▓▓▓▓▓▓▓▓▓▓",
                "██████████"
            ],
            'mid': [
                "◆◇◆◇◆◇◆◇",
                "♪♫♪♫♪♫♪♫",
                "▲▼▲▼▲▼▲▼",
                "●○●○●○●○"
            ],
            'high': [
                "★☆★☆★☆★☆",
                "♦♢♦♢♦♢♦♢",
                "▣▢▣▢▣▢▣▢",
                "◉◎◉◎◉◎◉◎"
            ],
            'beat': [
                "🎵🎶🎵🎶🎵🎶",
                "♪♫♪♫♪♫♪♫",
                "🔥⚡🔥⚡🔥⚡",
                "💥✨💥✨💥✨"
            ]
        }
        
        # AI-generated image patterns (simulated)
        self.ai_images = {
            'calm': self.generate_calm_pattern(),
            'energetic': self.generate_energetic_pattern(),
            'bass': self.generate_bass_pattern(),
            'treble': self.generate_treble_pattern()
        }
        
        # Setup visualization
        plt.style.use('dark_background')
        self.fig = plt.figure(figsize=(16, 10))
        
        # Create subplots
        gs = self.fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
        self.ax_main = self.fig.add_subplot(gs[0:2, 0:2])  # Main ASCII display
        self.ax_waveform = self.fig.add_subplot(gs[2, :])   # Waveform
        self.ax_image = self.fig.add_subplot(gs[0:2, 2])    # AI image
        
        self.setup_plots()
        
    def generate_calm_pattern(self):
        """Generate calm AI pattern"""
        pattern = np.zeros((50, 50, 3))
        for i in range(50):
            for j in range(50):
                # Soft blue gradient
                pattern[i, j] = [0.2 + 0.3*np.sin(i/10), 0.4 + 0.3*np.cos(j/10), 0.8]
        return pattern
    
    def generate_energetic_pattern(self):
        """Generate energetic AI pattern"""
        pattern = np.zeros((50, 50, 3))
        for i in range(50):
            for j in range(50):
                # Dynamic red-yellow pattern
                pattern[i, j] = [0.8 + 0.2*np.sin(i/5), 0.6 + 0.4*np.cos(j/5), 0.2]
        return pattern
    
    def generate_bass_pattern(self):
        """Generate bass-heavy pattern"""
        pattern = np.zeros((50, 50, 3))
        for i in range(50):
            for j in range(50):
                # Deep purple waves
                pattern[i, j] = [0.5 + 0.3*np.sin(i/8), 0.2, 0.7 + 0.3*np.cos(j/8)]
        return pattern
    
    def generate_treble_pattern(self):
        """Generate treble pattern"""
        pattern = np.zeros((50, 50, 3))
        for i in range(50):
            for j in range(50):
                # Bright cyan sparkles
                pattern[i, j] = [0.2, 0.8 + 0.2*np.sin(i/3), 0.9 + 0.1*np.cos(j/3)]
        return pattern
    
    def setup_plots(self):
        """Setup all plot areas"""
        # Main ASCII area
        self.ax_main.set_xlim(0, 10)
        self.ax_main.set_ylim(0, 10)
        self.ax_main.set_facecolor('black')
        self.ax_main.axis('off')
        self.ax_main.set_title('🎨 AI ASCII Music Art', color='white', fontsize=16, weight='bold')
        
        # Waveform area
        self.ax_waveform.set_xlim(0, 1024)
        self.ax_waveform.set_ylim(-1, 1)
        self.ax_waveform.set_facecolor('black')
        self.ax_waveform.set_title('🎵 Audio Waveform', color='cyan', fontsize=12)
        
        # AI image area
        self.ax_image.set_xlim(0, 1)
        self.ax_image.set_ylim(0, 1)
        self.ax_image.axis('off')
        self.ax_image.set_title('🤖 AI Generated Art', color='lime', fontsize=12)
    
    def audio_callback(self, indata, frames, time, status):
        """Process audio and extract features"""
        mono = np.mean(indata, axis=1) if indata.shape[1] > 1 else indata[:, 0]
        
        # Energy calculation
        energy = np.mean(mono ** 2)
        
        # Beat detection
        beat = energy > 0.02
        
        # Frequency analysis (simplified)
        fft = np.fft.rfft(mono)
        freqs = np.fft.rfftfreq(len(mono), 1/self.sample_rate)
        magnitude = np.abs(fft)
        
        # Split into frequency bands
        bands = np.zeros(8)
        band_size = len(magnitude) // 8
        for i in range(8):
            start = i * band_size
            end = (i + 1) * band_size
            bands[i] = np.mean(magnitude[start:end])
        
        with self.lock:
            self.audio_data = mono[-1024:] if len(mono) >= 1024 else np.pad(mono, (0, 1024-len(mono)))
            self.energy = energy
            self.beat = beat
            self.frequency_bands = bands
    
    def select_ascii_pattern(self):
        """AI-powered ASCII pattern selection"""
        # Analyze frequency content
        low_energy = np.mean(self.frequency_bands[:2])
        mid_energy = np.mean(self.frequency_bands[2:6])
        high_energy = np.mean(self.frequency_bands[6:])
        
        if self.beat and self.energy > 0.05:
            return random.choice(self.ascii_patterns['beat'])
        elif high_energy > mid_energy and high_energy > low_energy:
            return random.choice(self.ascii_patterns['high'])
        elif mid_energy > low_energy:
            return random.choice(self.ascii_patterns['mid'])
        else:
            return random.choice(self.ascii_patterns['low'])
    
    def select_ai_image(self):
        """Select AI image based on music analysis"""
        low_energy = np.mean(self.frequency_bands[:2])
        high_energy = np.mean(self.frequency_bands[6:])
        
        if self.energy > 0.1:
            return self.ai_images['energetic']
        elif high_energy > low_energy * 2:
            return self.ai_images['treble']
        elif low_energy > high_energy * 2:
            return self.ai_images['bass']
        else:
            return self.ai_images['calm']
    
    def update_frame(self, frame):
        """Update visualization"""
        with self.lock:
            audio = self.audio_data.copy()
            energy = self.energy
            beat = self.beat
            bands = self.frequency_bands.copy()
        
        # Clear all plots
        self.ax_main.clear()
        self.ax_waveform.clear()
        self.ax_image.clear()
        
        # Setup plots again
        self.setup_plots()
        
        # Draw ASCII art
        ascii_pattern = self.select_ascii_pattern()
        
        # Create ASCII grid
        rows = 8
        cols = 10
        for row in range(rows):
            for col in range(cols):
                # Vary intensity based on frequency bands
                band_idx = col % 8
                intensity = min(1.0, bands[band_idx] * 1000)
                
                # Color based on frequency
                if band_idx < 2:  # Low freq - red
                    color = (1, intensity * 0.5, 0)
                elif band_idx < 6:  # Mid freq - green
                    color = (0, 1, intensity * 0.5)
                else:  # High freq - blue
                    color = (intensity * 0.5, 0.5, 1)
                
                # Draw character
                char_idx = (row + col + frame//10) % len(ascii_pattern)
                if char_idx < len(ascii_pattern):
                    char = ascii_pattern[char_idx] if char_idx < len(ascii_pattern) else '█'
                    self.ax_main.text(col, rows-row, char, 
                                    color=color, fontsize=20, 
                                    ha='center', va='center',
                                    weight='bold')
        
        # Draw waveform
        if len(audio) > 0:
            self.ax_waveform.plot(audio, color='cyan', linewidth=1)
            self.ax_waveform.fill_between(range(len(audio)), audio, alpha=0.3, color='cyan')
        
        # Draw frequency bars
        bar_width = len(audio) // 8
        for i, band in enumerate(bands):
            height = min(1.0, band * 500)
            color = plt.cm.plasma(i / 8)
            self.ax_waveform.bar(i * bar_width, height, bar_width, 
                               alpha=0.7, color=color, bottom=-1)
        
        # Display AI image
        ai_image = self.select_ai_image()
        self.ax_image.imshow(ai_image, aspect='auto')
        
        # Add status text
        self.ax_main.text(0.5, 9.5, f'Energy: {energy:.3f} | Beat: {"🔥" if beat else "💤"}', 
                         color='white', fontsize=12, ha='left')
        
        # Band display
        band_text = " | ".join([f"B{i+1}:{bands[i]:.2f}" for i in range(4)])
        self.ax_waveform.text(10, 0.8, band_text, color='yellow', fontsize=8)
        
        return []
    
    def start(self):
        """Start the ASCII music visualizer"""
        print("[ASCII] Starting AI-Powered Music Visualizer...")
        print("[SYSTEM] ASCII art will react to your music!")
        print("[AI] Dynamic patterns and images generated in real-time")
        
        try:
            # Find audio device
            devices = sd.query_devices()
            device_id = None
            
            for i, device in enumerate(devices):
                if 'stereo mix' in device['name'].lower():
                    device_id = i
                    print(f"[DEVICE] Using: {device['name']}")
                    break
            
            # Start audio stream
            with sd.InputStream(device=device_id,
                              channels=1,
                              samplerate=self.sample_rate,
                              blocksize=self.buffer_size,
                              callback=self.audio_callback,
                              dtype=np.float32):
                
                # Start animation
                self.ani = animation.FuncAnimation(self.fig, self.update_frame, 
                                                 interval=150, blit=False, cache_frame_data=False)
                
                plt.tight_layout()
                plt.show(block=True)
                
        except KeyboardInterrupt:
            print("\n[STOP] ASCII visualizer stopped")
        except Exception as e:
            print(f"[ERROR] {e}")

def main():
    visualizer = ASCIIMusicVisualizer()
    visualizer.start()

if __name__ == "__main__":
    main()