"""
Module xử lý Text-to-Speech (TTS) qua WebSocket.
"""

import os
import json
import asyncio
import logging
from pathlib import Path

# Cần cài đặt thư viện 'websockets' nếu chưa có: pip install websockets
try:
    import websockets
except ImportError:
    logging.warning("Thư viện 'websockets' chưa được cài đặt. Hãy chạy: pip install websockets")

class TTSService:
    """
    Dịch vụ Text-to-Speech kết nối qua WebSocket.
    """
    def __init__(self, url: str = None, api_key: str = None, voice: str = None):
        # Xử lý an toàn typo URL của bạn (ws://http:// -> ws://)
        raw_url = url or "ws://103.253.20.27:8767"
        self.url = raw_url.replace("ws://http://", "ws://").replace("http://", "ws://")
        
        self.api_key = api_key or "ws_3f9e7cba-d8e4-4b6a-9c73-9c9f5e2c8d21"
        self.voice = voice or "thuyanh-north"
        
        self.logger = logging.getLogger(__name__)
        # Xoá handler cũ nếu có để tránh log bị lặp
        if not self.logger.handlers:
            logging.basicConfig(level=logging.INFO)

    async def _generate_audio_ws(self, text: str, output_file: str):
        """
        Xử lý kết nối WebSocket bất đồng bộ (async) để nhận audio.
        (Lưu ý: Payload JSON có thể cần điều chỉnh lại đúng cấu trúc API của model bạn dùng)
        """
        self.logger.info(f"Đang kết nối tới mô hình TTS tại: {self.url} (Voice: {self.voice})")
        
        # Thêm header Authorization theo chuẩn nếu model yêu cầu token qua header,
        # Nếu model yêu cầu gửi key qua message JSON thì sẽ nằm ở dòng weksocket.send
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        
        # Tuỳ thuộc vào cấu hình server, bạn có thể xóa headers hoặc thêm vào extra_headers
        async with websockets.connect(self.url) as websocket:
            # 1. Gửi cấu hình và đoạn text cần đọc
            payload = {
                "action": "tts",          # Tên action có thể thay đổi tùy API
                "api_key": self.api_key,  # Một số server yêu cầu API key gửi thẳng vào payload
                "text": text,
                "voice": self.voice,
                "speed": 1.0              # Tuỳ chọn
            }
            
            await websocket.send(json.dumps(payload))
            self.logger.info("Đã gửi văn bản, đang chờ dữ liệu Audio trả về...")
            
            # 2. Nhận dữ liệu Audio liên tục (Streaming)
            with open(output_file, "wb") as f:
                while True:
                    try:
                        message = await websocket.recv()
                        
                        # Nếu server trả về dữ liệu nhi phân (binary byte) -> ghi thẳng vào file âm thanh
                        if isinstance(message, bytes):
                            f.write(message)
                            
                        # Nếu server trả về chuỗi JSON (Text) -> xử lý trạng thái
                        elif isinstance(message, str):
                            data = json.loads(message)
                            
                            # Có thể trả info báo lỗi
                            if data.get("error"):
                                self.logger.error(f"Lỗi từ server TTS: {data['error']}")
                                break
                            
                            # Có thể trả tín hiệu báo kịch bản đã đọc xong
                            if data.get("status") in ["completed", "done"] or data.get("end"):
                                self.logger.info("Hoàn thành việc nhận luồng âm thanh.")
                                break
                                
                    except websockets.exceptions.ConnectionClosed:
                        self.logger.info("Đóng kết nối WebSocket.")
                        break
                    except Exception as exc:
                        self.logger.error(f"Lỗi rò rỉ khi tải Audio: {exc}")
                        break

    def generate_audio(self, text: str, output_path: str) -> bool:
        """
        Hàm public chạy đồng bộ (sync) dễ dàng tích hợp vào code Streamlit/Python thường.
        """
        try:
            # Chạy hàm async bằng asyncio trong môi trường đồng bộ
            asyncio.run(self._generate_audio_ws(text, output_path))
            
            # Kiểm tra xem file có được tạo và có dữ liệu không
            if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                self.logger.info(f"Đã lưu thành công file audio tại: {output_path}")
                return True
            else:
                self.logger.error("File audio trống hoặc chưa được lưu.")
                return False
                
        except Exception as exc:
            self.logger.error(f"Lỗi chạy tts: {exc}")
            return False

# ===============================================
# TEST NHANH KHI CHẠY TRỰC TIẾP FILE NÀY
# ===============================================
if __name__ == "__main__":
    # Thay đổi URL/Key nếu cần
    tts = TTSService()
    test_text = "Chào bạn, đây là luồng kiểm tra tính năng chuyển văn bản thành giọng nói."
    
    # Tạo thư mục test nếu chưa có
    os.makedirs("output_audio", exist_ok=True)
    out_file = "output_audio/test_audio.wav" # Đổi thành .mp3 nếu model của bạn trả về mp3
    
    success = tts.generate_audio(test_text, out_file)
    if success:
        print(f"Xong! Bạn có thể mở file {out_file} lên để nghe thử.")
