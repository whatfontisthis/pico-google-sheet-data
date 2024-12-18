# 설정
WIFI_SSID = '<your-ssid>'  # Wi-Fi SSID를 입력하세요
WIFI_PASSWORD = '<your-password>'  # Wi-Fi 비밀번호를 입력하세요
WEBHOOK_URL = '<your-webhook-url>'  # Google Apps Script Webhook URL을 입력하세요

import dht
from machine import Pin
import network
import urequests
import time

# DHT 센서 초기화
sensor = dht.DHT11(Pin(26))  # GPIO 26번 핀에 연결된 DHT11 센서를 초기화합니다.

# Wi-Fi 연결 설정
def connect_to_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)  # Wi-Fi STA 모드 활성화
    wlan.active(True)
    wlan.connect(ssid, password)  # 지정된 SSID와 비밀번호로 Wi-Fi 연결 시도

    while not wlan.isconnected():
        print('Wi-Fi에 연결 중...')  # Wi-Fi 연결 대기 중 출력
        time.sleep(2)

    print('Wi-Fi 연결 완료:', wlan.ifconfig())  # Wi-Fi 연결 성공 시 네트워크 설정 출력
    return wlan

# Google Sheets에 데이터를 전송하는 함수
def send_to_google_sheets(temperature, humidity):
    data = {
        "temperature": temperature,  # 온도 데이터
        "humidity": humidity  # 습도 데이터
    }
    headers = {"Content-Type": "application/json"}  # JSON 형식으로 데이터 전송
    response = urequests.post(WEBHOOK_URL, json=data, headers=headers)  # Webhook URL로 POST 요청
    print("응답:", response.text)  # 응답 내용 출력

# Wi-Fi에 연결
connect_to_wifi(WIFI_SSID, WIFI_PASSWORD)

# 메인 루프
while True:
    sensor.measure()  # DHT 센서에서 온도와 습도 측정
    temp = sensor.temperature()  # 측정된 온도 값
    hum = sensor.humidity()  # 측정된 습도 값
    print(f"온도: {temp}°C, 습도: {hum}%")  # 온도와 습도 값을 출력

    try:
        send_to_google_sheets(temp, hum)  # Google Sheets에 데이터 전송 시도
        print("데이터가 Google Sheets에 전송되었습니다.")
    except Exception as e:
        print("오류:", e)  # 예외 발생 시 오류 메시지 출력

    time.sleep(3)  # 3초 대기 후 반복
