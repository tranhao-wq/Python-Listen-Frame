"""
ElonMusk Audio Brain - Advanced Real-time Audio Reactive Visual Effects
Intelligent audio analysis with dynamic visual responses
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sounddevice as sd
import threading
import time
from collections import deque
import random
import math

class ElonMuskAudioBrain:
    def __init__(self):
        self.sample_rate = 44100
        self.buffer_size = 1024
        self.audio_buffer = deque(maxlen=self.sample_rate * 2)  # 2 seconds
        self.lock = threading.Lock()
        
        # Neural network-inspired parameters
        self.energy_threshold = 0.01
        self.last_energy = 0
        self.energy_history = deque(maxlen=50)
        self.beat_detected = False
        self.neural_activation = 0
        
        # Visual effects
        self.particles = []
        self.explosions = []
        self.neural_nodes = []
        self.connection_strength = 0
        
        # Setup visualization
        plt.style.use('dark_background')
        self.fig, self.ax = plt.subplots(figsize=(16, 10))
        self.fig.canvas.manager.set_window_title('🧠 ElonMusk Audio Brain - Neural Audio Reactor')
        
        self.init_neural_network()
        
    def init_neural_network(self):
        """Initialize neural network visualization nodes"""
        for i in range(20):
            x = random.uniform(-1, 1)
            y = random.uniform(-1, 1)
            self.neural_nodes.append({
                'x': x, 'y': y, 
                'activation': 0,
                'connections': random.randint(2, 5)
            })
    
    def audio_callback(self, indata, frames, time, status):
        """Real-time audio processing with neural analysis"""
        if status:
            print(f"Audio status: {status}")
        
        # Convert to mono
        audio_data = np.mean(indata, axis=1) if indata.shape[1] > 1 else indata[:, 0]
        
        with self.lock:
            self.audio_buffer.extend(audio_data)
            
        # Real-time neural processing
        self.process_neural_audio(audio_data)
    
    def process_neural_audio(self, audio_chunk):
        """ElonMusk-style neural audio processing"""
        # Energy calculation
        energy = np.sum(audio_chunk ** 2) / len(audio_chunk)
        self.energy_history.append(energy)
        
        # Neural activation based on energy change
        if len(self.energy_history) > 1:
            energy_delta = energy - self.last_energy
            self.neural_activation = max(0, energy_delta * 1000)
            
            # Beat detection using neural threshold
            avg_energy = np.mean(list(self.energy_history)[-10:])
            if energy > avg_energy * 1.5 and energy > self.energy_threshold:
                self.trigger_neural_explosion(energy)
                self.beat_detected = True
            else:
                self.beat_detected = False
        
        self.last_energy = energy
        
        # Update neural network activation
        self.update_neural_network(energy)
    
    def trigger_neural_explosion(self, intensity):
        """Create explosive visual effect"""
        num_particles = int(intensity * 500)
        center_x = random.uniform(-0.5, 0.5)
        center_y = random.uniform(-0.5, 0.5)
        
        for _ in range(min(num_particles, 50)):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(0.1, 0.5)
            self.particles.append({
                'x': center_x,
                'y': center_y,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'life': 1.0,
                'color': random.choice(['cyan', 'magenta', 'yellow', 'lime'])
            })
        
        # Add explosion effect
        self.explosions.append({
            'x': center_x,
            'y': center_y,
            'radius': 0.1,
            'max_radius': intensity * 2,
            'life': 1.0
        })
    
    def update_neural_network(self, energy):
        """Update neural network visualization"""
        for node in self.neural_nodes:
            # Neural activation based on audio energy
            node['activation'] = min(1.0, energy * 100 + random.uniform(0, 0.3))
            
            # Neural drift for organic movement
            node['x'] += random.uniform(-0.01, 0.01)
            node['y'] += random.uniform(-0.01, 0.01)
            
            # Keep nodes in bounds
            node['x'] = max(-1, min(1, node['x']))
            node['y'] = max(-1, min(1, node['y']))
        
        # Connection strength based on overall energy
        self.connection_strength = min(1.0, energy * 50)
    
    def update_particles(self):
        """Update particle physics"""
        for particle in self.particles[:]:
            particle['x'] += particle['vx'] * 0.02
            particle['y'] += particle['vy'] * 0.02
            particle['life'] -= 0.05
            
            if particle['life'] <= 0:
                self.particles.remove(particle)
        
        # Update explosions
        for explosion in self.explosions[:]:
            explosion['radius'] += 0.1
            explosion['life'] -= 0.1
            
            if explosion['life'] <= 0 or explosion['radius'] > explosion['max_radius']:
                self.explosions.remove(explosion)
    
    def render_frame(self, frame):
        """Render neural audio visualization"""
        self.ax.clear()
        self.ax.set_xlim(-1.2, 1.2)
        self.ax.set_ylim(-1.2, 1.2)
        self.ax.set_facecolor('black')
        
        # Get current audio data
        with self.lock:
            if len(self.audio_buffer) > 0:
                current_audio = np.array(list(self.audio_buffer)[-1024:])
            else:
                current_audio = np.zeros(1024)
        
        # Neural network visualization
        self.render_neural_network()
        
        # Audio waveform as neural signal
        if len(current_audio) > 0:
            t = np.linspace(-1, 1, len(current_audio))
            waveform = current_audio * 0.3
            self.ax.plot(t, waveform, color='cyan', alpha=0.6, linewidth=1)
        
        # Render particles and explosions
        self.render_effects()
        
        # Update physics
        self.update_particles()
        
        # Neural status display
        energy = self.last_energy
        self.ax.text(-1.1, 1.0, f'BRAIN Energy: {energy:.4f}', 
                    color='lime', fontsize=12, weight='bold')
        self.ax.text(-1.1, 0.9, f'FIRE Activation: {self.neural_activation:.2f}', 
                    color='orange', fontsize=12, weight='bold')
        self.ax.text(-1.1, 0.8, f'BEAT: {"DETECTED" if self.beat_detected else "---"}', 
                    color='red' if self.beat_detected else 'gray', fontsize=12, weight='bold')
        
        self.ax.set_title('ELONMUSK AUDIO BRAIN - Neural Reactive System', 
                         color='white', fontsize=16, weight='bold')
        self.ax.axis('off')
    
    def render_neural_network(self):
        """Render neural network nodes and connections"""
        # Draw connections
        for i, node1 in enumerate(self.neural_nodes):
            for j, node2 in enumerate(self.neural_nodes[i+1:], i+1):
                if j < i + node1['connections']:
                    alpha = self.connection_strength * node1['activation'] * node2['activation']
                    if alpha > 0.1:
                        self.ax.plot([node1['x'], node2['x']], [node1['y'], node2['y']], 
                                   color='cyan', alpha=alpha, linewidth=alpha*3)
        
        # Draw nodes
        for node in self.neural_nodes:
            size = 50 + node['activation'] * 200
            color_intensity = node['activation']
            self.ax.scatter(node['x'], node['y'], s=size, 
                          c=[[color_intensity, 1-color_intensity, 1]], 
                          alpha=0.8, edgecolors='white', linewidth=1)
    
    def render_effects(self):
        """Render particles and explosions"""
        # Render particles
        for particle in self.particles:
            alpha = particle['life']
            size = particle['life'] * 30
            self.ax.scatter(particle['x'], particle['y'], s=size, 
                          c=particle['color'], alpha=alpha)
        
        # Render explosions
        for explosion in self.explosions:
            alpha = explosion['life']
            circle = plt.Circle((explosion['x'], explosion['y']), 
                              explosion['radius'], 
                              fill=False, color='red', 
                              alpha=alpha, linewidth=3)
            self.ax.add_patch(circle)
    
    def start_neural_processing(self):
        """Start the neural audio processing system"""
        print("[BRAIN] Starting ElonMusk Audio Brain...")
        print("[AUDIO] Neural audio processing activated")
        print("[VISUAL] Visual effects will trigger on audio changes")
        print("[SYSTEM] Press Ctrl+C to stop")
        
        # Find audio device
        try:
            # Try to find stereo mix or loopback
            devices = sd.query_devices()
            device_id = None
            
            for i, device in enumerate(devices):
                if ('stereo mix' in device['name'].lower() or 
                    'loopback' in device['name'].lower() or
                    'what u hear' in device['name'].lower()):
                    device_id = i
                    print(f"[DEVICE] Using device: {device['name']}")
                    break
            
            if device_id is None:
                print("[WARNING] Using default input device")
            
            # Start audio stream
            with sd.InputStream(device=device_id,
                              channels=2,
                              samplerate=self.sample_rate,
                              blocksize=self.buffer_size,
                              callback=self.audio_callback):
                
                # Start visualization
                ani = animation.FuncAnimation(self.fig, self.render_frame, 
                                            interval=50, blit=False)
                plt.tight_layout()
                plt.show()
                
        except KeyboardInterrupt:
            print("\n[STOP] Neural processing stopped")
        except Exception as e:
            print(f"[ERROR] {e}")

def main():
    """Launch ElonMusk Audio Brain"""
    brain = ElonMuskAudioBrain()
    brain.start_neural_processing()

if __name__ == "__main__":
    main()