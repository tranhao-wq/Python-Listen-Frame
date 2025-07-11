"""
Combined Music Visualizer - Multi-Display Visual Art Generator
Combines all visualizers into one fullscreen display
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
from matplotlib.gridspec import GridSpec

class CombinedMusicVisualizer:
    def __init__(self):
        self.sample_rate = 44100
        self.buffer_size = 1024
        self.audio_data = np.zeros(1024)
        self.lock = threading.Lock()
        
        # Audio analysis
        self.energy = 0
        self.beat = False
        self.frequency_bands = np.zeros(8)
        self.neural_activation = 0
        self.last_energy = 0
        self.energy_history = []
        
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
        
        # Neural network nodes
        self.neural_nodes = []
        self.particles = []
        self.explosions = []
        self.init_neural_network()
        
        # AI patterns
        self.ai_images = {
            'calm': self.generate_calm_pattern(),
            'energetic': self.generate_energetic_pattern(),
            'bass': self.generate_bass_pattern(),
            'treble': self.generate_treble_pattern()
        }
        
        # Setup fullscreen visualization
        plt.style.use('dark_background')
        self.fig = plt.figure(figsize=(16, 9))
        self.fig.canvas.manager.full_screen_toggle()  # Enable fullscreen
        
        # Create grid layout
        gs = GridSpec(3, 4, figure=self.fig)
        
        # Initialize all visualization areas
        self.ax_ascii = self.fig.add_subplot(gs[0:2, 0])      # ASCII art
        self.ax_neural = self.fig.add_subplot(gs[0:2, 1:3])   # Neural network
        self.ax_ai = self.fig.add_subplot(gs[0:2, 3])         # AI art
        self.ax_wave = self.fig.add_subplot(gs[2, :2])        # Waveform
        self.ax_spectrum = self.fig.add_subplot(gs[2, 2:])    # Spectrum
        
        self.setup_plots()
        
    def init_neural_network(self):
        """Initialize neural network nodes"""
        for i in range(20):
            x = random.uniform(-1, 1)
            y = random.uniform(-1, 1)
            self.neural_nodes.append({
                'x': x, 'y': y,
                'activation': 0,
                'connections': random.randint(2, 5)
            })
    
    def generate_calm_pattern(self):
        """Generate calm AI pattern"""
        pattern = np.zeros((50, 50, 3))
        for i in range(50):
            for j in range(50):
                pattern[i, j] = [0.2 + 0.3*np.sin(i/10), 0.4 + 0.3*np.cos(j/10), 0.8]
        return pattern
    
    def generate_energetic_pattern(self):
        """Generate energetic pattern"""
        pattern = np.zeros((50, 50, 3))
        for i in range(50):
            for j in range(50):
                pattern[i, j] = [0.8 + 0.2*np.sin(i/5), 0.6 + 0.4*np.cos(j/5), 0.2]
        return pattern
    
    def generate_bass_pattern(self):
        """Generate bass pattern"""
        pattern = np.zeros((50, 50, 3))
        for i in range(50):
            for j in range(50):
                pattern[i, j] = [0.5 + 0.3*np.sin(i/8), 0.2, 0.7 + 0.3*np.cos(j/8)]
        return pattern
    
    def generate_treble_pattern(self):
        """Generate treble pattern"""
        pattern = np.zeros((50, 50, 3))
        for i in range(50):
            for j in range(50):
                pattern[i, j] = [0.2, 0.8 + 0.2*np.sin(i/3), 0.9 + 0.1*np.cos(j/3)]
        return pattern
    
    def setup_plots(self):
        """Setup all visualization areas"""
        # ASCII art area
        self.ax_ascii.set_xlim(0, 10)
        self.ax_ascii.set_ylim(0, 10)
        self.ax_ascii.set_facecolor('black')
        self.ax_ascii.axis('off')
        self.ax_ascii.set_title('🎨 ASCII Art', color='white', fontsize=12)
        
        # Neural network area
        self.ax_neural.set_xlim(-1.2, 1.2)
        self.ax_neural.set_ylim(-1.2, 1.2)
        self.ax_neural.set_facecolor('black')
        self.ax_neural.axis('off')
        self.ax_neural.set_title('🧠 Neural Network', color='cyan', fontsize=12)
        
        # AI art area
        self.ax_ai.set_xlim(0, 1)
        self.ax_ai.set_ylim(0, 1)
        self.ax_ai.axis('off')
        self.ax_ai.set_title('🤖 AI Art', color='lime', fontsize=12)
        
        # Waveform area
        self.ax_wave.set_xlim(0, 1024)
        self.ax_wave.set_ylim(-1, 1)
        self.ax_wave.set_facecolor('black')
        self.ax_wave.set_title('🎵 Waveform', color='yellow', fontsize=12)
        
        # Spectrum area
        self.ax_spectrum.set_xlim(0, 8)
        self.ax_spectrum.set_ylim(0, 1)
        self.ax_spectrum.set_facecolor('black')
        self.ax_spectrum.set_title('📊 Frequency Spectrum', color='magenta', fontsize=12)
    
    def audio_callback(self, indata, frames, time, status):
        """Process audio input"""
        if status:
            print(f"Audio status: {status}")
            
        # Convert to mono and normalize
        audio_data = np.mean(indata, axis=1) if indata.shape[1] > 1 else indata[:, 0]
        
        # Energy calculation
        energy = np.mean(audio_data ** 2)
        self.energy_history.append(energy)
        if len(self.energy_history) > 50:
            self.energy_history.pop(0)
            
        # Beat detection
        beat = energy > 0.02 and energy > np.mean(self.energy_history) * 1.5
        
        # Frequency analysis
        fft = np.fft.rfft(audio_data)
        magnitude = np.abs(fft)
        
        # Split into frequency bands
        bands = np.zeros(8)
        band_size = len(magnitude) // 8
        for i in range(8):
            start = i * band_size
            end = (i + 1) * band_size
            bands[i] = np.mean(magnitude[start:end])
        
        # Neural activation
        energy_delta = energy - self.last_energy
        neural_activation = max(0, energy_delta * 1000)
        
        with self.lock:
            self.audio_data = audio_data[-1024:]
            self.energy = energy
            self.beat = beat
            self.frequency_bands = bands
            self.neural_activation = neural_activation
            self.last_energy = energy
            
        # Trigger effects on beat
        if beat and energy > 0.02:
            self.trigger_neural_explosion(energy)
    
    def trigger_neural_explosion(self, intensity):
        """Create neural explosion effect"""
        num_particles = int(intensity * 500)
        center_x = random.uniform(-0.5, 0.5)
        center_y = random.uniform(-0.5, 0.5)
        
        for _ in range(min(num_particles, 50)):
            angle = random.uniform(0, 2 * np.pi)
            speed = random.uniform(0.1, 0.5)
            self.particles.append({
                'x': center_x,
                'y': center_y,
                'vx': np.cos(angle) * speed,
                'vy': np.sin(angle) * speed,
                'life': 1.0,
                'color': random.choice(['cyan', 'magenta', 'yellow', 'lime'])
            })
            
        self.explosions.append({
            'x': center_x,
            'y': center_y,
            'radius': 0.1,
            'max_radius': intensity * 2,
            'life': 1.0
        })
    
    def update_neural_network(self):
        """Update neural network state"""
        for node in self.neural_nodes:
            node['activation'] = min(1.0, self.energy * 100 + random.uniform(0, 0.3))
            node['x'] += random.uniform(-0.01, 0.01)
            node['y'] += random.uniform(-0.01, 0.01)
            node['x'] = max(-1, min(1, node['x']))
            node['y'] = max(-1, min(1, node['y']))
    
    def update_particles(self):
        """Update particle effects"""
        for particle in self.particles[:]:
            particle['x'] += particle['vx'] * 0.02
            particle['y'] += particle['vy'] * 0.02
            particle['life'] -= 0.05
            if particle['life'] <= 0:
                self.particles.remove(particle)
                
        for explosion in self.explosions[:]:
            explosion['radius'] += 0.1
            explosion['life'] -= 0.1
            if explosion['life'] <= 0 or explosion['radius'] > explosion['max_radius']:
                self.explosions.remove(explosion)
    
    def select_ascii_pattern(self):
        """Select ASCII pattern based on audio analysis"""
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
        """Select AI image based on audio analysis"""
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
        """Update all visualizations"""
        with self.lock:
            audio = self.audio_data.copy()
            energy = self.energy
            beat = self.beat
            bands = self.frequency_bands.copy()
        
        # Clear all plots
        self.ax_ascii.clear()
        self.ax_neural.clear()
        self.ax_ai.clear()
        self.ax_wave.clear()
        self.ax_spectrum.clear()
        
        # Setup plots
        self.setup_plots()
        
        # Update neural network
        self.update_neural_network()
        self.update_particles()
        
        # Draw ASCII art
        ascii_pattern = self.select_ascii_pattern()
        rows, cols = 8, 10
        for row in range(rows):
            for col in range(cols):
                band_idx = col % 8
                intensity = min(1.0, bands[band_idx] * 1000)
                
                if band_idx < 2:
                    color = (1, intensity * 0.5, 0)
                elif band_idx < 6:
                    color = (0, 1, intensity * 0.5)
                else:
                    color = (intensity * 0.5, 0.5, 1)
                
                char_idx = (row + col + frame//10) % len(ascii_pattern)
                if char_idx < len(ascii_pattern):
                    char = ascii_pattern[char_idx]
                    self.ax_ascii.text(col, rows-row, char,
                                     color=color, fontsize=20,
                                     ha='center', va='center',
                                     weight='bold')
        
        # Draw neural network
        for i, node1 in enumerate(self.neural_nodes):
            for j, node2 in enumerate(self.neural_nodes[i+1:], i+1):
                if j < i + node1['connections']:
                    alpha = self.neural_activation * node1['activation'] * node2['activation']
                    if alpha > 0.1:
                        self.ax_neural.plot([node1['x'], node2['x']],
                                          [node1['y'], node2['y']],
                                          color='cyan', alpha=alpha, linewidth=alpha*3)
        
        for node in self.neural_nodes:
            size = 50 + node['activation'] * 200
            color_intensity = node['activation']
            self.ax_neural.scatter(node['x'], node['y'], s=size,
                                 c=[[color_intensity, 1-color_intensity, 1]],
                                 alpha=0.8, edgecolors='white', linewidth=1)
        
        # Draw particles and explosions
        for particle in self.particles:
            alpha = particle['life']
            size = particle['life'] * 30
            self.ax_neural.scatter(particle['x'], particle['y'],
                                 s=size, c=particle['color'], alpha=alpha)
        
        for explosion in self.explosions:
            circle = plt.Circle((explosion['x'], explosion['y']),
                              explosion['radius'],
                              fill=False, color='red',
                              alpha=explosion['life'], linewidth=2)
            self.ax_neural.add_patch(circle)
        
        # Draw AI art
        ai_image = self.select_ai_image()
        self.ax_ai.imshow(ai_image, aspect='auto')
        
        # Draw waveform
        self.ax_wave.plot(audio, color='cyan', linewidth=1)
        self.ax_wave.fill_between(range(len(audio)), audio,
                                alpha=0.3, color='cyan')
        
        # Draw spectrum
        for i, band in enumerate(bands):
            height = min(1.0, band * 500)
            color = plt.cm.plasma(i / 8)
            self.ax_spectrum.bar(i, height, width=0.8,
                               alpha=0.7, color=color)
        
        # Add status information
        self.fig.suptitle('🎼 Combined Music Visualizer', color='white',
                         fontsize=16, weight='bold', y=0.98)
        status_text = f'Energy: {energy:.3f} | Beat: {"🔥" if beat else "💤"}'
        self.fig.text(0.02, 0.98, status_text, color='white',
                     fontsize=10, transform=self.fig.transFigure)
        
        return []
    
    def find_audio_device(self):
        """Find suitable audio input device"""
        try:
            devices = sd.query_devices()
            device_id = None
            
            # List of possible device name keywords
            device_keywords = [
                'stereo mix',
                'wave out',
                'what u hear',
                'loopback',
                'virtual audio',
                'cable output',
                'output mix',
                'mix output',
                'default output'
            ]
            
            print("\n[INFO] Available audio devices:")
            for i, device in enumerate(devices):
                print(f"[{i}] {device['name']} (in={device['max_input_channels']}, out={device['max_output_channels']})")
                
                # Check if device name contains any of our keywords
                if any(keyword in device['name'].lower() for keyword in device_keywords):
                    device_id = i
                    print(f"[FOUND] Selected device {i}: {device['name']}")
                    break
            
            if device_id is None:
                # Try to find any input device
                for i, device in enumerate(devices):
                    if device['max_input_channels'] > 0:
                        device_id = i
                        print(f"[FALLBACK] Using first available input device {i}: {device['name']}")
                        break
            
            if device_id is None:
                # If still no device found, use default input
                device_id = sd.default.device[0]
                print(f"[DEFAULT] Using system default input device")
            
            return device_id
            
        except Exception as e:
            print(f"[WARNING] Error finding audio device: {e}")
            return None
    
    def start(self):
        """Start the combined visualizer"""
        print("[START] Combined Music Visualizer")
        print("[INFO] Multiple visualizations in one display")
        print("[SYSTEM] Press F11 for fullscreen")
        print("[SYSTEM] Press Ctrl+C to stop")
        
        try:
            # Find audio device
            device_id = self.find_audio_device()
            
            # Start audio stream
            with sd.InputStream(device=device_id,
                              channels=2,
                              samplerate=self.sample_rate,
                              blocksize=self.buffer_size,
                              callback=self.audio_callback):
                
                # Start animation
                ani = animation.FuncAnimation(self.fig, self.update_frame,
                                           interval=50, blit=False,
                                           cache_frame_data=False)
                plt.tight_layout()
                plt.show()
                
        except KeyboardInterrupt:
            print("\n[STOP] Visualizer stopped")
        except Exception as e:
            print(f"[ERROR] {e}")

def main():
    visualizer = CombinedMusicVisualizer()
    visualizer.start()

if __name__ == "__main__":
    main()
