"""
Core audio capture and processing engine
"""
import sounddevice as sd
import numpy as np
import threading
from collections import deque
from typing import Optional, Callable, List, Tuple


class AudioEngine:
    def __init__(self, sample_rate: int = 44100, buffer_size: int = 1024, 
                 window_duration: float = 2.0):
        self.sample_rate = sample_rate
        self.buffer_size = buffer_size
        self.window_samples = int(sample_rate * window_duration)
        
        # Rolling buffer for visualization
        self.audio_buffer = deque(maxlen=self.window_samples)
        self.lock = threading.Lock()
        self.stream = None
        self.is_running = False
        
        # Callbacks
        self.data_callback: Optional[Callable] = None
        
    def list_devices(self) -> List[Tuple[int, str, bool]]:
        """List available audio devices with loopback capability"""
        devices = []
        for i, device in enumerate(sd.query_devices()):
            # Check for loopback or stereo mix capability
            is_loopback = ('stereo mix' in device['name'].lower() or 
                          'loopback' in device['name'].lower() or
                          'what u hear' in device['name'].lower() or
                          device['max_input_channels'] > 0)
            devices.append((i, device['name'], is_loopback))
        return devices
    
    def find_loopback_device(self) -> Optional[int]:
        """Auto-detect system loopback device"""
        devices = self.list_devices()
        
        # Priority order for loopback detection
        priorities = ['stereo mix', 'loopback', 'what u hear', 'speakers', 'headphones']
        
        for priority in priorities:
            for device_id, name, _ in devices:
                if priority in name.lower():
                    try:
                        # Test if device supports input
                        device_info = sd.query_devices(device_id)
                        if device_info['max_input_channels'] > 0:
                            return device_id
                    except:
                        continue
        
        # Fallback to default input device
        try:
            return sd.default.device[0]
        except:
            return None
    
    def _audio_callback(self, indata, frames, time, status):
        """Real-time audio callback"""
        if status:
            print(f"Audio callback status: {status}")
        
        # Convert to mono if stereo
        if indata.shape[1] > 1:
            audio_data = np.mean(indata, axis=1)
        else:
            audio_data = indata[:, 0]
        
        with self.lock:
            self.audio_buffer.extend(audio_data)
        
        # Trigger data callback if set
        if self.data_callback:
            self.data_callback(audio_data)
    
    def start_capture(self, device_id: Optional[int] = None) -> bool:
        """Start audio capture"""
        if self.is_running:
            return True
        
        if device_id is None:
            device_id = self.find_loopback_device()
        
        if device_id is None:
            print("No suitable audio device found")
            return False
        
        try:
            device_info = sd.query_devices(device_id)
            print(f"Using device: {device_info['name']}")
            
            self.stream = sd.InputStream(
                device=device_id,
                channels=min(2, device_info['max_input_channels']),
                samplerate=self.sample_rate,
                blocksize=self.buffer_size,
                callback=self._audio_callback,
                dtype=np.float32
            )
            
            self.stream.start()
            self.is_running = True
            return True
            
        except Exception as e:
            print(f"Failed to start audio capture: {e}")
            return False
    
    def stop_capture(self):
        """Stop audio capture"""
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None
        self.is_running = False
    
    def get_audio_data(self) -> np.ndarray:
        """Get current audio buffer data"""
        with self.lock:
            if len(self.audio_buffer) == 0:
                return np.zeros(self.window_samples)
            return np.array(list(self.audio_buffer))
    
    def set_data_callback(self, callback: Callable):
        """Set callback for real-time data processing"""
        self.data_callback = callback