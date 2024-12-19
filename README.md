# Pico W DHT11 센서를 이용한 Google Sheets 연동

이 프로젝트는 Raspberry Pi Pico W가 DHT11 센서로부터 실시간 온도와 습도 데이터를 수집하여 Google Sheets에 전송하는 방법을 제공합니다. Google Apps Script를 활용하여 Google Sheets가 자동으로 업데이트됩니다.

## 주요 기능
- DHT11 센서로부터 온도와 습도 데이터를 읽어옵니다.
- 지정된 Wi-Fi 네트워크에 연결하여 데이터를 전송합니다.
- Google Apps Script Webhook을 통해 데이터를 Google Sheets에 전송합니다.

---

## 작동 방식
1. DHT11 센서가 온도와 습도 데이터를 수집합니다.
2. Pico W가 Wi-Fi 네트워크에 연결합니다.
3. 수집된 데이터는 HTTP POST 요청을 통해 Google Apps Script Webhook으로 전송됩니다.
4. Webhook은 데이터를 Google Sheets에 추가합니다.

---

## 사전 준비
1. **Raspberry Pi Pico W** (MicroPython 설치 필요).
2. **DHT11 센서** (Pico W와 연결).
3. **Google Cloud Platform (GCP) 프로젝트** (Google Sheets 및 Apps Script 활성화).

---

## 설정

### 1. 하드웨어 설정
- DHT11 센서를 Pico W에 연결:
  - **Signal (S)** 핀: GPIO26에 연결.
  - **VCC (5V)** 핀: Pico W의 5V 핀에 연결.
  - **GND** 핀: Pico W의 GND 핀에 연결.

### 2. Google Sheets 및 Apps Script 설정
#### 단계 1: Google Sheets 생성
1. 새로운 Google Sheets 생성 (예: `Pico Data`).
2. URL에서 **Spreadsheet ID**를 복사:
  - https://docs.google.com/spreadsheets/d/<스프레드시트-ID>/edit

3. 첫 번째 시트(탭)의 이름을 확인 (예: `Sheet1`).


#### 단계 2: Google Apps Script Webhook 생성
1. Google Sheets에서 **확장 프로그램 > Apps Script**로 이동.
2. 기본 코드를 다음 코드로 교체:

```javascript
function doPost(e) {
    var sheet = SpreadsheetApp.openById('<스프레드시트-ID>').getSheetByName('Sheet1');
    var data = JSON.parse(e.postData.contents);
    sheet.appendRow([new Date(), data.temperature, data.humidity]);
    
    return ContentService.createTextOutput(
        JSON.stringify({ status: 'success' })
    ).setMimeType(ContentService.MimeType.JSON);
}
```
  - <스프레드시트-ID>를 실제 Spreadsheet ID로 교체.
  - 스크립트를 저장하고 Web App으로 배포:
    1.  배포 > 새 배포 클릭.
    2. Web App 선택.
    3. 실행 권한: 나.
    4. 접근 권한: 모든 사용자.
    5. 배포 후 Web App URL 복사.

#### 단계 3: 시트 공유
1.웹 앱 서비스 계정 이메일과 Google Sheet 공유 (필요시):
2.파일 > 공유로 이동.
3.이메일 추가 후 편집자 권한 부여.


### 3. 라즈베리파이 피코 실행 코드 dht-google-sheet.py  
1.Python 스크립트를 열고 다음 값을 수정:
2.WIFI_SSID: 와이파이 이름(2.4G 사용).
3.WIFI_PASSWORD: 비밀번호.
4.WEBHOOK_URL: Google Apps Script Web App URL.
5.스크립트를 저장하고 Pico W에 업로드/실행.
WIFI_SSID: Wi-Fi SSID.
WIFI_PASSWORD: Wi-Fi 비밀번호.
WEBHOOK_URL: Google Apps Script Web App URL.
스크립트를 저장하고 Pico W에 업로드.
