import time
import pandas as pd
import cv2
import json
import matplotlib.pyplot as plt

import shutil
import os
import random
try:
 from PIL import Image
except ImportError:
 import Image

import requests
import uuid
import time
import json

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 5000)

api_url = 'https://clovastudio.apigw.ntruss.com/'
secret_key = 'bld6Sk15aG13ZHluendVaXZzUmtyUXR6YVd3Vmt2Z1E='
image_file = '/Users/dongwoohan/Downloads/빵/삼립 옥수수크림빵.jpg'



# Setting up the request JSON
request_json = {
    'images': [
        {
            'format': 'jpg',
            'name': 'demo'
        }
    ],
    'requestId': str(uuid.uuid4()),
    'version': 'V2',
    'timestamp': int(round(time.time() * 1000))
}

payload = {'message': json.dumps(request_json).encode('UTF-8')}
headers = {'X-OCR-SECRET': secret_key}

# Make the OCR request
with open(image_file, 'rb') as img_file:
    files = [('file', img_file)]
    response = requests.post(api_url, headers=headers, data=payload, files=files)


# Load the original image for visualization
image = cv2.imread(image_file)
highlighted_image = image.copy()

# OCR 응답 처리
if response.status_code == 200:
    ocr_results = json.loads(response.text)
    all_texts = []  # 모든 텍스트를 저장할 리스트
    for image_result in ocr_results['images']:
        for field in image_result['fields']:
            text = field['inferText']
            all_texts.append(text)  # 텍스트 추가

            # 텍스트 주변에 빨간 사각형 그리기
            bounding_box = field['boundingPoly']['vertices']
            start_point = (int(bounding_box[0]['x']), int(bounding_box[0]['y']))
            end_point = (int(bounding_box[2]['x']), int(bounding_box[2]['y']))
            cv2.rectangle(highlighted_image, start_point, end_point, (0, 0, 255), 2)

    # 모든 텍스트를 띄어쓰기로 연결하여 출력
    #full_text = ' '.join(all_texts)
    #print(full_text)

    for i in response.json()['images'][0]['fields']:#한개씩 출력
        text = i['inferText']
        print(text)
else:
    print(f"OCR 결과를 받아오지 못했습니다. 상태 코드: {response.status_code}")


# Display the original and highlighted images side by side
fig, axs = plt.subplots(1, 2, figsize=(15, 10))
axs[0].imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
axs[0].set_title('Original Image')
axs[0].axis('off')

axs[1].imshow(cv2.cvtColor(highlighted_image, cv2.COLOR_BGR2RGB))
axs[1].set_title('Highlighted Image')
axs[1].axis('off')

plt.show()