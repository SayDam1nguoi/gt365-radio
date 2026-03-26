import asyncio
import websockets
import json
import base64
import logging
import re
import wave
import os
from dataclasses import dataclass
from typing import Optional, AsyncIterator

logger = logging.getLogger(__name__)

@dataclass
class TTSChunk:
    raw_pcm: bytes = b""
    is_final: bool = False
    duration: float = 0.0
    sample_rate: int = 8000
    text: str = ""
    origin_text: str = ""

class TTSService:
    def __init__(self, url: str = None, api_key: str = None, voice: str = "thuyanh-north", tempo: float = 1.0):
        # Fix typing errors in URL
        raw_url = url or "ws://103.253.20.27:8767"
        self.ws_url = raw_url.replace("ws://http://", "ws://").replace("http://", "ws://")
        
        self.api_key = api_key or "ws_3f9e7cba-d8e4-4b6a-9c73-9c9f5e2c8d21"
        self.voice = voice
        self.tempo = tempo
        self.ws = None
        self.sample_rate = 8000
        self.is_auth = False
        self.result_queue: Optional[asyncio.Queue] = None
        self._receive_task: Optional[asyncio.Task] = None
        self._lock = None
        self.max_text_length = 200  

    async def _get_lock(self):
        if self._lock is None:
            self._lock = asyncio.Lock()
        return self._lock
        
    async def connect(self):
        """Connect to WebSocket and authenticate"""
        lock = await self._get_lock()
        async with lock:
            if self.ws is not None:
                try:
                    await self.ws.close()
                except Exception:
                    pass
                finally:
                    self.ws = None
            
            if self._receive_task and not self._receive_task.done():
                self._receive_task.cancel()
                try:
                    await self._receive_task
                except asyncio.CancelledError:
                    pass
            
            self.result_queue = asyncio.Queue(maxsize=100)
            
            try:
                self.ws = await asyncio.wait_for(
                    websockets.connect(self.ws_url),
                    timeout=10.0
                )
            except asyncio.TimeoutError:
                raise Exception("[TTS] Connection timeout")
            except Exception as e:
                raise Exception(f"[TTS] Failed to connect WebSocket: {e}")
            
            logger.info(f"voice {self.voice} tempo {self.tempo}")
            auth_msg = {
                "text": " ", 
                "voice_settings": {
                    "voiceId": self.voice,
                    "resample_rate": 8000, 
                    "tempo": self.tempo,
                },
                "generator_config": {
                    "chunk_length_schedule": [1],
                },
                "xi_api_key": self.api_key, 
            }
            
            try:
                await asyncio.wait_for(
                    self.ws.send(json.dumps(auth_msg)),
                    timeout=5.0
                )
            except Exception as e:
                await self.ws.close()
                raise Exception(f"[TTS] Failed to send auth: {e}")
            
            try:
                response = await asyncio.wait_for(
                    self.ws.recv(),
                    timeout=5.0
                )
                auth_resp = json.loads(response)
            except asyncio.TimeoutError:
                await self.ws.close()
                raise Exception("[TTS] Failed to read auth response: timeout")
            except Exception as e:
                await self.ws.close()
                raise Exception(f"[TTS] Failed to read auth response: {e}")
            
            status = auth_resp.get("status")
            if status != "authenticated":
                error_msg = auth_resp.get("error", "unknown error")
                await self.ws.close()
                raise Exception(f"[TTS] Authentication failed: {error_msg}")
            
            self.is_auth = True
            if "sampling_rate" in auth_resp:
                self.sample_rate = int(auth_resp["sampling_rate"])
            else:
                self.sample_rate = 8000
            
            logger.info(f"[TTS] WebSocket authenticated: voice={self.voice}, sample_rate={self.sample_rate}")
            
            self._receive_task = asyncio.create_task(self._receive_loop())
            logger.info("[TTS] Receive loop task started")
    
    async def send_text(self, text: str, end_of_input: bool) -> None:
        """Send text to synthesize"""
        lock = await self._get_lock()
        async with lock:
            if not self.is_auth:
                raise Exception("[TTS] Not authenticated")
            
            if self.ws is None:
                raise Exception("[TTS] WebSocket not connected")
            
            msg = {
                "text": text,
                "end_of_input": end_of_input,
            }
            
            try:
                await self.ws.send(json.dumps(msg))
                logger.info(f"[TTS] sent text: '{text}', end_of_input={end_of_input}")
            except Exception as e:
                raise Exception(f"[TTS] Failed to send text: {e}")
    
    async def reset(self) -> None:
        """Reset buffer and cancel ongoing synthesis"""
        lock = await self._get_lock()
        async with lock:
            if not self.is_auth:
                raise Exception("[TTS] Not authenticated")
            
            if self.ws is None:
                raise Exception("[TTS] WebSocket not connected")
            
            msg = {"reset": True}
            try:
                await self.ws.send(json.dumps(msg))
            except Exception as e:
                raise Exception(f"[TTS] Failed to send reset: {e}")
    
    async def _receive_loop(self) -> None:
        """Receive audio chunks from WebSocket"""
        logger.info("[TTS] Receive loop started")
        try:
            while True:
                if self.ws is None:
                    break
                
                try:
                    response = await asyncio.wait_for(self.ws.recv(), timeout=60.0)
                    msg = json.loads(response)
                except asyncio.CancelledError:
                    break
                except asyncio.TimeoutError:
                    continue
                except websockets.exceptions.ConnectionClosed:
                    break
                except Exception as e:
                    break
                
                if "error" in msg:
                    continue
                
                if msg.get("status") == "reset":
                    continue
                
                chunk = TTSChunk(raw_pcm=b"")
                
                if "audio" in msg and msg["audio"]:
                    audio_b64 = msg["audio"]
                    try:
                        pcm = base64.b64decode(audio_b64)
                        chunk.raw_pcm = pcm
                    except Exception as e:
                        logger.error(f"[TTS] base64 decode error: {e}")
                
                if "isFinal" in msg:
                    chunk.is_final = bool(msg["isFinal"])
                
                if self.result_queue:
                    try:
                        await self.result_queue.put(chunk)
                    except Exception as e:
                        pass
        except Exception as e:
            pass
        finally:
            if self.result_queue:
                try:
                    await self.result_queue.put(None)
                except Exception:
                    pass
    
    def _split_text_by_sentences(self, text: str, max_length: int = 500):
        if len(text) <= max_length:
            return [text]
        sentence_endings = r'[.!?;]'
        sentences = re.split(f'({sentence_endings})', text)
        combined = []
        for i in range(0, len(sentences)-1, 2):
            if i+1 < len(sentences):
                combined.append(sentences[i] + sentences[i+1])
            else:
                combined.append(sentences[i])
        if len(sentences) % 2 == 1 and sentences[-1].strip():
            combined.append(sentences[-1])
        
        chunks = []
        current_chunk = ""
        for sentence in combined:
            sentence = sentence.strip()
            if not sentence: continue
            if len(current_chunk) + len(sentence) + 1 <= max_length:
                current_chunk += (" " + sentence if current_chunk else sentence)
            else:
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = sentence
        if current_chunk:
            chunks.append(current_chunk)
            
        final_chunks = []
        for chunk in chunks:
            if len(chunk) <= max_length:
                final_chunks.append(chunk)
            else:
                parts = chunk.split(',')
                temp_chunk = ""
                for part in parts:
                    if len(temp_chunk) + len(part) + 1 <= max_length:
                        temp_chunk += ("," + part if temp_chunk else part)
                    else:
                        if temp_chunk:
                            final_chunks.append(temp_chunk)
                        temp_chunk = part
                if temp_chunk:
                    final_chunks.append(temp_chunk)
                    
        very_final_chunks = []
        for chunk in final_chunks:
            if len(chunk) <= max_length:
                very_final_chunks.append(chunk)
            else:
                words = chunk.split()
                temp_chunk = ""
                for word in words:
                    if len(temp_chunk) + len(word) + 1 <= max_length:
                        temp_chunk += (" " + word if temp_chunk else word)
                    else:
                        if temp_chunk:
                            very_final_chunks.append(temp_chunk)
                        temp_chunk = word
                if temp_chunk:
                    very_final_chunks.append(temp_chunk)
                    
        return [c.strip() for c in very_final_chunks if c.strip()]
    
    async def _ensure_connected(self):
        """Ensure WebSocket is connected, reconnect if needed"""
        if self.ws is None:
            await self.connect()
    
    async def synthesize(self, text: str) -> AsyncIterator[bytes]:
        await self._ensure_connected()
        
        if self._receive_task and not self._receive_task.done():
            self._receive_task.cancel()
            try:
                await asyncio.wait_for(self._receive_task, timeout=1.0)
            except (asyncio.CancelledError, asyncio.TimeoutError):
                pass
            self._receive_task = None
        
        text_chunks = self._split_text_by_sentences(text, self.max_text_length)
        logger.info(f"[TTS] Synthesizing {len(text)} chars in {len(text_chunks)} chunks")
        
        for i, chunk_text in enumerate(text_chunks):
            is_last_chunk = (i == len(text_chunks) - 1)
            
            try:
                await self.send_text(chunk_text, is_last_chunk)
            except Exception as e:
                try:
                    await self._ensure_connected()
                    await self.send_text(chunk_text, is_last_chunk)
                except Exception:
                    continue
            
            chunk_received = False
            timeout_seconds = 2  
            max_timeout_count = 3  
            timeout_count = 0
            
            while True:
                try:
                    if self.ws is None:
                        break
                    
                    response = await asyncio.wait_for(
                        self.ws.recv(),
                        timeout=timeout_seconds
                    )
                    msg = json.loads(response)
                    timeout_count = 0
                    
                    if "error" in msg:
                        break
                    
                    if msg.get("status") == "reset":
                        continue
                    
                    if "audio" in msg and msg["audio"]:
                        audio_b64 = msg["audio"]
                        try:
                            pcm = base64.b64decode(audio_b64)
                            chunk_received = True
                            yield pcm
                        except Exception:
                            pass
                    
                    if msg.get("isFinal", False):
                        break
                        
                except asyncio.TimeoutError:
                    timeout_count += 1
                    if not chunk_received:
                        if timeout_count >= max_timeout_count:
                            break
                    else:
                        if timeout_count >= 2:
                            break
                        timeout_seconds = 1
                        continue
                except websockets.exceptions.ConnectionClosed:
                    break
                except Exception as e:
                    break
        
        if self.ws is not None and self.is_auth:
            self._receive_task = asyncio.create_task(self._receive_loop())
    
    async def close(self):
        """Close WebSocket connection"""
        lock = await self._get_lock()
        async with lock:
            if self._receive_task and not self._receive_task.done():
                self._receive_task.cancel()
                try:
                    await self._receive_task
                except asyncio.CancelledError:
                    pass
            
            if self.ws is not None:
                try:
                    await self.ws.close()
                except Exception:
                    pass
                finally:
                    self.ws = None
                    self.is_auth = False

    def generate_audio(self, text: str, output_path: str) -> bool:
        """
        Streamlit Sync Frontend Wrapper. 
        Calls async generator, bundles raw PCM into playable WAV file.
        """
        async def _run():
            pcm_bytes = bytearray()
            try:
                async for chunk in self.synthesize(text):
                    if chunk:
                        pcm_bytes.extend(chunk)
            except Exception as e:
                logger.error(f"Error wrapping generator: {e}")
            finally:
                await self.close()
            return pcm_bytes

        try:
            # Tạo event loop mới nếu chạy từ luồng đồng bộ (Streamlit)
            pcm_data = asyncio.run(_run())
            
            if not pcm_data:
                logger.error("No PCM data received.")
                return False
                
            with wave.open(output_path, 'wb') as wav_file:
                wav_file.setnchannels(1)      
                wav_file.setsampwidth(2)      
                wav_file.setframerate(self.sample_rate) 
                wav_file.writeframes(pcm_data)
                
            if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                logger.info(f"Đã xuất WAV thành công: {output_path}")
                return True
            return False
            
        except Exception as exc:
            logger.error(f"Sync UI Wrapper Error: {exc}")
            return False
