"""
ElonMusk Audio Brain - Fixed Visual Panel
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sounddevice as sd
import threading
import random
import math
from collections import deque

class ElonMuskFixedVisual:
    def __init__(self):
        self.sample_rate = 22050
        self.buffer_size = 512
        self.audio_buffer = deque(maxlen=2048)
        self.lock = threading.Lock()
        
        # Audio analysis
        self.energy = 0
        self.beat = False
        self.frequency_bands = np.zeros(8)
        
        # Visual effects
        self.particles = []
        self.neural_nodes = []
        
        # Setup visualization
        plt.style.use('dark_background')
        self.fig = plt.figure(figsize=(16, 8))
        
        # Create layout: main neural area + right visual panel
        gs = self.fig.add_gridspec(2, 3, width_ratios=[2, 2, 1], height_ratios=[1, 1])
        self.ax_main = self.fig.add_subplot(gs[:, :2])  # Main neural network
        self.ax_visual = self.fig.add_subplot(gs[:, 2])  # Right visual panel
        
        self.init_neural_network()
        
    def init_neural_network(self):
        """Initialize neural nodes"""
        for i in range(15):
            self.neural_nodes.append({
                'x': random.uniform(-1, 1),
                'y': random.uniform(-1, 1),
                'activation': 0,
                'size': random.uniform(20, 60)
            })
    
    def audio_callback(self, indata, frames, time, status):
        """Process audio"""
        mono = np.mean(indata, axis=1) if indata.shape[1] > 1 else indata[:, 0]
        
        # Energy and beat detection
        energy = np.mean(mono ** 2)
        beat = energy > 0.02
        
        # Frequency analysis
        if len(mono) >= 256:
            fft = np.fft.rfft(mono[:256])
            magnitude = np.abs(fft)
            bands = np.zeros(8)
            band_size = len(magnitude) // 8
            for i in range(8):
                start = i * band_size
                end = (i + 1) * band_size
                bands[i] = np.mean(magnitude[start:end])
        else:
            bands = np.zeros(8)
        
        with self.lock:
            self.audio_buffer.extend(mono)
            self.energy = energy
            self.beat = beat
            self.frequency_bands = bands
            
            # Add particles on beat
            if beat and energy > 0.05 and len(self.particles) < 20:
                self.particles.append({
                    'x': random.uniform(-0.8, 0.8),
                    'y': random.uniform(-0.8, 0.8),
                    'vx': random.uniform(-0.1, 0.1),
                    'vy': random.uniform(-0.1, 0.1),
                    'life': 30,
                    'color': random.choice(['cyan', 'magenta', 'yellow', 'lime'])
                })
    
    def draw_ascii_art(self):
        """Generate ASCII art based on frequency bands"""
        patterns = []
        
        # Different patterns for different frequency ranges
        low_pattern = ["###", "===", "---", "..."]
        mid_pattern = ["^^^", "~~~", "***", "+++"]
        high_pattern = ["!!!", "|||", "^^^", ":::"]
        
        # Select pattern based on dominant frequency
        low_energy = np.mean(self.frequency_bands[:2])
        mid_energy = np.mean(self.frequency_bands[2:6])
        high_energy = np.mean(self.frequency_bands[6:])
        
        if high_energy > mid_energy and high_energy > low_energy:
            base_pattern = high_pattern
        elif mid_energy > low_energy:
            base_pattern = mid_pattern
        else:
            base_pattern = low_pattern
        
        # Create 8x8 grid
        grid = []
        for row in range(8):
            line = ""
            for col in range(8):
                band_idx = col % 8
                intensity = min(1.0, self.frequency_bands[band_idx] * 500)
                
                if intensity > 0.7:
                    char = "#"
                elif intensity > 0.4:
                    char = "*"
                elif intensity > 0.2:
                    char = "+"
                elif intensity > 0.1:
                    char = "."
                else:
                    char = " "
                
                line += char
            grid.append(line)
        
        return grid
    
    def update_frame(self, frame):
        """Update visualization"""
        with self.lock:
            audio_data = list(self.audio_buffer)[-1024:] if self.audio_buffer else np.zeros(1024)
            energy = self.energy
            beat = self.beat
            bands = self.frequency_bands.copy()
        
        # Clear plots
        self.ax_main.clear()
        self.ax_visual.clear()
        
        # Setup main plot
        self.ax_main.set_xlim(-1.2, 1.2)
        self.ax_main.set_ylim(-1.2, 1.2)
        self.ax_main.set_facecolor('black')
        self.ax_main.axis('off')
        self.ax_main.set_title('ELONMUSK NEURAL BRAIN', color='white', fontsize=16, weight='bold')
        
        # Draw neural network
        for i, node in enumerate(self.neural_nodes):
            # Update node activation
            node['activation'] = min(1.0, energy * 100 + random.uniform(0, 0.2))
            
            # Draw connections
            for j, other_node in enumerate(self.neural_nodes[i+1:], i+1):
                if j < i + 3:  # Limit connections
                    alpha = node['activation'] * other_node['activation'] * 0.5
                    if alpha > 0.1:
                        self.ax_main.plot([node['x'], other_node['x']], 
                                        [node['y'], other_node['y']], 
                                        color='cyan', alpha=alpha, linewidth=1)
            
            # Draw node
            size = node['size'] + node['activation'] * 100
            color_intensity = node['activation']
            self.ax_main.scatter(node['x'], node['y'], s=size,
                               c=[[color_intensity, 1-color_intensity, 1]], 
                               alpha=0.8, edgecolors='white', linewidth=1)
        
        # Draw waveform
        if len(audio_data) > 0:
            audio_array = np.array(audio_data)
            t = np.linspace(-1, 1, len(audio_array))
            self.ax_main.plot(t, audio_array * 0.3, color='cyan', alpha=0.6, linewidth=1)
        
        # Draw particles
        for particle in self.particles[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['life'] -= 1
            
            if particle['life'] <= 0:
                self.particles.remove(particle)
            else:
                alpha = particle['life'] / 30
                self.ax_main.scatter(particle['x'], particle['y'], 
                                   s=30, c=particle['color'], alpha=alpha)
        
        # Status display
        self.ax_main.text(-1.1, 1.0, f'Energy: {energy:.4f}', color='lime', fontsize=12, weight='bold')
        self.ax_main.text(-1.1, 0.9, f'Beat: {"DETECTED" if beat else "---"}', 
                         color='red' if beat else 'gray', fontsize=12, weight='bold')
        
        # RIGHT PANEL - ASCII ART VISUALIZATION
        self.ax_visual.set_xlim(0, 8)
        self.ax_visual.set_ylim(0, 8)
        self.ax_visual.set_facecolor('black')
        self.ax_visual.axis('off')
        self.ax_visual.set_title('ASCII ART', color='yellow', fontsize=14, weight='bold')
        
        # Generate and display ASCII art
        ascii_grid = self.draw_ascii_art()
        
        for row, line in enumerate(ascii_grid):
            for col, char in enumerate(line):
                # Color based on frequency band
                band_idx = col % 8
                intensity = min(1.0, bands[band_idx] * 500)
                
                if band_idx < 2:  # Low freq - red
                    color = (1, intensity * 0.5, 0)
                elif band_idx < 6:  # Mid freq - green  
                    color = (0, 1, intensity * 0.5)
                else:  # High freq - blue
                    color = (intensity * 0.5, 0.5, 1)
                
                self.ax_visual.text(col, 7-row, char, color=color, 
                                  fontsize=16, ha='center', va='center', 
                                  weight='bold', family='monospace')
        
        # Frequency bars in visual panel
        for i, band in enumerate(bands):
            height = min(7, band * 1000)
            if height > 0.1:
                self.ax_visual.bar(i, height, 0.8, bottom=0, 
                                 alpha=0.3, color=plt.cm.plasma(i/8))
        
        return []
    
    def start(self):
        """Start the visualizer"""
        print("[ELONMUSK] Starting Fixed Visual Brain...")
        print("[SYSTEM] Neural network + ASCII art panel")
        
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
                                                 interval=100, blit=False, cache_frame_data=False)
                
                plt.tight_layout()
                plt.show(block=True)
                
        except KeyboardInterrupt:
            print("\n[STOP] ElonMusk brain stopped")
        except Exception as e:
            print(f"[ERROR] {e}")

def main():
    brain = ElonMuskFixedVisual()
    brain.start()

if __name__ == "__main__":
    main()