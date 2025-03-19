import json
import logging
import requests
import threading
import websocket
from typing import Dict, Any, List, Callable, Optional
from urllib.parse import urljoin

class BaseApiClient:
    """
    기본 API 클라이언트 클래스.
    모든 도메인별 API 클라이언트가 상속받을 기본 클래스입니다.
    """
    
    def __init__(self, base_url: str, api_key: str = "", ws_url: str = ""):
        """
        BaseApiClient 초기화
        
        Args:
            base_url: API 기본 URL
            api_key: API 키
            ws_url: WebSocket URL
        """
        self.base_url = base_url
        self.api_key = api_key
        self.ws_url = ws_url
        self.ws = None
        self.ws_thread = None
        self.ws_callbacks = {}
        
        # 로깅 설정
        self.logger = logging.getLogger(self.__class__.__name__)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
    
    def _get_headers(self) -> Dict[str, str]:
        """
        API 요청에 사용할 헤더를 가져옵니다.
        
        Returns:
            Dict[str, str]: 요청 헤더
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        if self.api_key:
            headers["X-API-Key"] = self.api_key
            
        return headers
    
    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """
        API 응답을 처리합니다.
        
        Args:
            response: HTTP 응답 객체
            
        Returns:
            Dict[str, Any]: 응답 데이터
            
        Raises:
            HTTPError: HTTP 에러 발생 시
        """
        response.raise_for_status()  # 4XX, 5XX 에러 시 예외 발생
        
        if response.status_code == 204:  # No Content
            return {}
            
        try:
            return response.json()
        except json.JSONDecodeError:
            self.logger.error("응답 JSON 파싱 오류")
            return {"error": "응답 형식 오류", "content": response.text}
    
    def get(self, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        GET 요청을 수행합니다.
        
        Args:
            endpoint: API 엔드포인트
            params: 쿼리 파라미터
            
        Returns:
            Dict[str, Any]: 응답 데이터
        """
        url = urljoin(self.base_url, endpoint)
        
        try:
            response = requests.get(
                url,
                params=params,
                headers=self._get_headers()
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            self.logger.error(f"GET 요청 오류 ({url}): {str(e)}")
            raise
    
    def post(self, endpoint: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        POST 요청을 수행합니다.
        
        Args:
            endpoint: API 엔드포인트
            data: 요청 데이터
            
        Returns:
            Dict[str, Any]: 응답 데이터
        """
        url = urljoin(self.base_url, endpoint)
        
        try:
            response = requests.post(
                url,
                json=data,
                headers=self._get_headers()
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            self.logger.error(f"POST 요청 오류 ({url}): {str(e)}")
            raise
    
    def put(self, endpoint: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        PUT 요청을 수행합니다.
        
        Args:
            endpoint: API 엔드포인트
            data: 요청 데이터
            
        Returns:
            Dict[str, Any]: 응답 데이터
        """
        url = urljoin(self.base_url, endpoint)
        
        try:
            response = requests.put(
                url,
                json=data,
                headers=self._get_headers()
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            self.logger.error(f"PUT 요청 오류 ({url}): {str(e)}")
            raise
    
    def delete(self, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        DELETE 요청을 수행합니다.
        
        Args:
            endpoint: API 엔드포인트
            params: 쿼리 파라미터
            
        Returns:
            Dict[str, Any]: 응답 데이터
        """
        url = urljoin(self.base_url, endpoint)
        
        try:
            response = requests.delete(
                url,
                params=params,
                headers=self._get_headers()
            )
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            self.logger.error(f"DELETE 요청 오류 ({url}): {str(e)}")
            raise
    
    def connect_websocket(self, callback: Optional[Callable[[Dict], None]] = None) -> bool:
        """
        WebSocket 연결을 설정합니다.
        
        Args:
            callback: WebSocket 메시지를 처리할 콜백 함수
            
        Returns:
            bool: 연결 성공 여부
        """
        if not self.ws_url:
            self.logger.error("WebSocket URL이 설정되지 않았습니다.")
            return False
        
        def on_message(ws, message):
            try:
                data = json.loads(message)
                channel = data.get("channel", "default")
                
                # 기본 콜백 호출
                if callback:
                    callback(data)
                
                # 채널별 콜백 호출
                if channel in self.ws_callbacks:
                    for cb in self.ws_callbacks[channel]:
                        cb(data)
            except json.JSONDecodeError:
                self.logger.error("WebSocket 메시지 파싱 오류")
            except Exception as e:
                self.logger.error(f"WebSocket 메시지 처리 오류: {str(e)}")
        
        def on_error(ws, error):
            self.logger.error(f"WebSocket 오류: {str(error)}")
        
        def on_close(ws, close_status_code, close_msg):
            self.logger.info("WebSocket 연결 종료")
        
        def on_open(ws):
            self.logger.info("WebSocket 연결 성공")
            # 인증 메시지 전송
            auth_message = {
                "type": "auth",
                "api_key": self.api_key
            }
            ws.send(json.dumps(auth_message))
        
        # WebSocket 연결
        try:
            self.ws = websocket.WebSocketApp(
                self.ws_url,
                on_message=on_message,
                on_error=on_error,
                on_close=on_close,
                on_open=on_open
            )
            
            # 백그라운드 스레드에서 WebSocket 실행
            self.ws_thread = threading.Thread(target=self.ws.run_forever)
            self.ws_thread.daemon = True
            self.ws_thread.start()
            
            return True
        except Exception as e:
            self.logger.error(f"WebSocket 연결 오류: {str(e)}")
            return False
    
    def subscribe_channel(self, channel: str, callback: Callable[[Dict], None]) -> bool:
        """
        특정 채널을 구독합니다.
        
        Args:
            channel: 채널 이름
            callback: 채널 메시지를 처리할 콜백 함수
            
        Returns:
            bool: 구독 성공 여부
        """
        if not self.ws:
            return False
        
        # 콜백 등록
        if channel not in self.ws_callbacks:
            self.ws_callbacks[channel] = []
        self.ws_callbacks[channel].append(callback)
        
        # 구독 메시지 전송
        subscribe_message = {
            "type": "subscribe",
            "channel": channel
        }
        self.ws.send(json.dumps(subscribe_message))
        
        return True
    
    def disconnect_websocket(self) -> bool:
        """
        WebSocket 연결을 종료합니다.
        
        Returns:
            bool: 종료 성공 여부
        """
        if self.ws:
            self.ws.close()
            self.ws = None
            return True
        return False 