import requests

# 클로바 OCR API URL 및 인증 정보
url = "https://naveropenapi.apigw.ntruss.com/vision/v1/ocr"
headers = {
    "X-NCP-APIGW-API-KEY-ID": "YOUR_CLIENT_ID",
    "X-NCP-APIGW-API-KEY": "YOUR_CLIENT_SECRET",
}

# 분석할 이미지 파일 경로 설정
image_path = "/path/to/your/image.jpg"  # 여기에 이미지 파일 경로 입력
files = {"image": open(image_path, "rb")}

# API 요청 및 응답 처리
response = requests.post(url, headers=headers, files=files)
if response.status_code == 200:
    result = response.json()
    print("OCR 결과:", result)
else:
    print("Error:", response.status_code, response.text)
