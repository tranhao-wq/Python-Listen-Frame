"""
Real-time audio visualization with multiple modes
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy import signal
from typing import Optional
import threading


class AudioVisualizer:
    def __init__(self, sample_rate: int = 44100, window_size: int = 2048):
        self.sample_rate = sample_rate
        self.window_size = window_size
        self.mode = 'waveform'  # 'waveform', 'fft', 'spectrogram'
        
        # Setup matplotlib
        plt.style.use('dark_background')
        self.fig, self.ax = plt.subplots(figsize=(12, 6))
        self.fig.canvas.manager.set_window_title('Real-time Audio Analyzer')
        
        # Initialize plots
        self.line_wave = None
        self.line_fft = None
        self.spectrogram_im = None
        self.spectrogram_data = []
        
        # Animation
        self.ani = None
        self.audio_data = np.zeros(window_size)
        self.data_lock = threading.Lock()
        
        # Setup key press handler
        self.fig.canvas.mpl_connect('key_press_event', self._on_key_press)
        
        self._setup_plots()
    
    def _setup_plots(self):
        """Initialize plot elements for all modes"""
        self.ax.clear()
        
        if self.mode == 'waveform':
            self.ax.set_title('Audio Waveform (Press: w=waveform, f=FFT, s=spectrogram)')
            self.ax.set_xlabel('Time (samples)')
            self.ax.set_ylabel('Amplitude')
            self.ax.set_ylim(-1, 1)
            self.line_wave, = self.ax.plot([], [], 'cyan', linewidth=1)
            
        elif self.mode == 'fft':
            self.ax.set_title('FFT Frequency Spectrum (Press: w=waveform, f=FFT, s=spectrogram)')
            self.ax.set_xlabel('Frequency (Hz)')
            self.ax.set_ylabel('Magnitude (dB)')
            self.ax.set_xlim(0, self.sample_rate // 2)
            self.ax.set_ylim(-80, 0)
            self.line_fft, = self.ax.plot([], [], 'lime', linewidth=1)
            
        elif self.mode == 'spectrogram':
            self.ax.set_title('Spectrogram (Press: w=waveform, f=FFT, s=spectrogram)')
            self.ax.set_xlabel('Time')
            self.ax.set_ylabel('Frequency (Hz)')
            self.spectrogram_data = []
    
    def _on_key_press(self, event):
        """Handle key press events for mode switching"""
        if event.key == 'w':
            self.mode = 'waveform'
            self._setup_plots()
        elif event.key == 'f':
            self.mode = 'fft'
            self._setup_plots()
        elif event.key == 's':
            self.mode = 'spectrogram'
            self._setup_plots()
    
    def update_data(self, audio_data: np.ndarray):
        """Update audio data for visualization"""
        with self.data_lock:
            # Ensure consistent size
            if len(audio_data) > self.window_size:
                self.audio_data = audio_data[-self.window_size:]
            else:
                # Pad with zeros if needed
                padded = np.zeros(self.window_size)
                padded[:len(audio_data)] = audio_data
                self.audio_data = padded
    
    def _animate(self, frame):
        """Animation function for matplotlib"""
        with self.data_lock:
            data = self.audio_data.copy()
        
        if self.mode == 'waveform':
            self.line_wave.set_data(range(len(data)), data)
            self.ax.set_xlim(0, len(data))
            return [self.line_wave]
        
        elif self.mode == 'fft':
            # Compute FFT
            windowed = data * np.hanning(len(data))
            fft = np.fft.rfft(windowed)
            magnitude = 20 * np.log10(np.abs(fft) + 1e-10)
            freqs = np.fft.rfftfreq(len(data), 1/self.sample_rate)
            
            self.line_fft.set_data(freqs, magnitude)
            return [self.line_fft]
        
        elif self.mode == 'spectrogram':
            # Compute spectrogram
            if len(data) > 0:
                f, t, Sxx = signal.spectrogram(data, self.sample_rate, 
                                             nperseg=min(256, len(data)//4))
                Sxx_db = 10 * np.log10(Sxx + 1e-10)
                
                # Keep rolling spectrogram
                self.spectrogram_data.append(Sxx_db)
                if len(self.spectrogram_data) > 100:  # Keep last 100 frames
                    self.spectrogram_data.pop(0)
                
                if len(self.spectrogram_data) > 1:
                    combined = np.hstack(self.spectrogram_data)
                    
                    if self.spectrogram_im is None:
                        self.spectrogram_im = self.ax.imshow(combined, 
                                                           aspect='auto', 
                                                           origin='lower',
                                                           cmap='plasma',
                                                           extent=[0, len(self.spectrogram_data), 
                                                                  f[0], f[-1]])
                    else:
                        self.spectrogram_im.set_array(combined)
                        self.spectrogram_im.set_extent([0, len(self.spectrogram_data), 
                                                       f[0], f[-1]])
            
            return [self.spectrogram_im] if self.spectrogram_im else []
        
        return []
    
    def start_visualization(self):
        """Start real-time visualization"""
        self.ani = animation.FuncAnimation(
            self.fig, self._animate, interval=50, blit=True, cache_frame_data=False
        )
        plt.tight_layout()
        plt.show()
    
    def stop_visualization(self):
        """Stop visualization"""
        if self.ani:
            self.ani.event_source.stop()
        plt.close(self.fig)