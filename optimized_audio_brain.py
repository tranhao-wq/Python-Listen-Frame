"""
Optimized Audio Brain - Ultra Performance Version
Minimal lag, maximum efficiency
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sounddevice as sd
import threading
from collections import deque
import time

class OptimizedAudioBrain:
    def __init__(self):
        self.sample_rate = 22050  # Reduced for performance
        self.buffer_size = 512    # Smaller buffer
        self.audio_data = np.zeros(1024)
        self.lock = threading.Lock()
        
        # Minimal state tracking
        self.energy = 0
        self.beat = False
        self.frame_count = 0
        
        # Ultra-light particle system
        self.particles = []
        self.max_particles = 10  # Drastically reduced
        
        # Setup minimal plot
        plt.ion()
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.fig.patch.set_facecolor('black')
        self.ax.set_facecolor('black')
        self.ax.set_xlim(-1, 1)
        self.ax.set_ylim(-1, 1)
        self.ax.axis('off')
        
        # Pre-allocate plot elements
        self.waveform_line, = self.ax.plot([], [], 'cyan', linewidth=1)
        self.energy_circle = plt.Circle((0, 0), 0.1, fill=False, color='red', linewidth=2)
        self.ax.add_patch(self.energy_circle)
        
    def audio_callback(self, indata, frames, time, status):
        """Ultra-fast audio processing"""
        # Convert to mono immediately
        mono = np.mean(indata, axis=1) if indata.shape[1] > 1 else indata[:, 0]
        
        # Quick energy calculation
        energy = np.mean(mono ** 2)
        
        # Simple beat detection
        beat = energy > 0.01
        
        # Thread-safe update
        with self.lock:
            self.audio_data = mono[-1024:] if len(mono) >= 1024 else np.pad(mono, (0, 1024-len(mono)))
            self.energy = energy
            self.beat = beat
            
            # Add particle only on strong beats
            if beat and energy > 0.05 and len(self.particles) < self.max_particles:
                self.particles.append({
                    'x': np.random.uniform(-0.5, 0.5),
                    'y': np.random.uniform(-0.5, 0.5),
                    'life': 30  # frames
                })
    
    def update_frame(self, frame):
        """Minimal rendering update"""
        self.frame_count += 1
        
        # Skip frames for performance
        if self.frame_count % 2 != 0:
            return []
        
        with self.lock:
            audio = self.audio_data.copy()
            energy = self.energy
            beat = self.beat
        
        # Update waveform (downsampled)
        if len(audio) > 0:
            # Use every 4th sample for performance
            downsampled = audio[::4]
            t = np.linspace(-1, 1, len(downsampled))
            self.waveform_line.set_data(t, downsampled * 0.5)
        
        # Update energy circle
        radius = min(0.8, energy * 20)
        self.energy_circle.set_radius(radius)
        self.energy_circle.set_color('red' if beat else 'blue')
        
        # Ultra-simple particle update
        for particle in self.particles[:]:
            particle['life'] -= 1
            if particle['life'] <= 0:
                self.particles.remove(particle)
        
        # Draw particles as simple dots
        self.ax.clear()
        self.ax.set_xlim(-1, 1)
        self.ax.set_ylim(-1, 1)
        self.ax.set_facecolor('black')
        self.ax.axis('off')
        
        # Redraw waveform
        if len(audio) > 0:
            downsampled = audio[::4]
            t = np.linspace(-1, 1, len(downsampled))
            self.ax.plot(t, downsampled * 0.5, 'cyan', linewidth=1)
        
        # Draw energy circle
        circle = plt.Circle((0, 0), radius, fill=False, 
                           color='red' if beat else 'blue', linewidth=2)
        self.ax.add_patch(circle)
        
        # Draw particles
        if self.particles:
            x_coords = [p['x'] for p in self.particles]
            y_coords = [p['y'] for p in self.particles]
            self.ax.scatter(x_coords, y_coords, c='yellow', s=20, alpha=0.8)
        
        # Status text
        self.ax.text(-0.9, 0.9, f'Energy: {energy:.3f}', color='lime', fontsize=10)
        self.ax.text(-0.9, 0.8, f'Beat: {"YES" if beat else "NO"}', 
                    color='red' if beat else 'gray', fontsize=10)
        
        return []
    
    def start(self):
        """Start optimized audio processing"""
        print("[OPTIMIZED] Starting Ultra-Performance Audio Brain...")
        print("[SYSTEM] Reduced settings for maximum performance")
        
        try:
            # Find audio device
            devices = sd.query_devices()
            device_id = None
            
            for i, device in enumerate(devices):
                if 'stereo mix' in device['name'].lower():
                    device_id = i
                    print(f"[DEVICE] Using: {device['name']}")
                    break
            
            # Start audio stream with minimal settings
            with sd.InputStream(device=device_id,
                              channels=1,  # Mono only
                              samplerate=self.sample_rate,
                              blocksize=self.buffer_size,
                              callback=self.audio_callback,
                              dtype=np.float32):
                
                # Start animation with longer interval
                self.ani = animation.FuncAnimation(self.fig, self.update_frame, 
                                            interval=100, blit=False, cache_frame_data=False)
                
                plt.tight_layout()
                plt.show(block=True)
                
        except KeyboardInterrupt:
            print("\n[STOP] Optimized processing stopped")
        except Exception as e:
            print(f"[ERROR] {e}")

def main():
    brain = OptimizedAudioBrain()
    brain.start()

if __name__ == "__main__":
    main()