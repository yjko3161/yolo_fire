# YOLO 화재 감지 웹 애플리케이션

이 프로젝트는 YOLO 모델을 사용하여 이미지에서 화재 및 기타 객체를 감지하는 Flask 웹 애플리케이션입니다.

## 기능

- 이미지 업로드
- YOLO 모델을 사용한 객체 감지 (화재 감지 포함)
- 감지 결과 시각화
- 감지된 객체 목록 및 신뢰도 표시 (색상으로 신뢰도 구분)

## 설치 방법

1. 저장소 클론:

```bash
git clone https://github.com/yourusername/yolo_fire.git
cd yolo_fire
```

2. 필요한 패키지 설치:

```bash
pip install -r requirements.txt
```

## 실행 방법

```bash
python app.py
```

기본적으로 애플리케이션은 http://127.0.0.1:5000/ 에서 실행됩니다.

## 사용 방법

1. 웹 브라우저에서 http://127.0.0.1:5000/ 접속
2. "이미지 파일 선택" 버튼을 클릭하여 분석할 이미지 선택
3. "분석하기" 버튼을 클릭하여 YOLO 모델로 분석 시작
4. 결과 페이지에서 감지된 객체 확인

## 폴더 구조

- `/static/uploads`: 업로드된 이미지 저장 폴더
- `/static/results`: 감지 결과 이미지 저장 폴더
- `/templates`: HTML 템플릿 파일
- `app.py`: 메인 Flask 애플리케이션
- `requirements.txt`: 필요한 패키지 목록

## 커스텀 YOLO 모델 사용

기본적으로 YOLOv8s 모델이 사용됩니다. 필요에 따라 사용자 정의 모델로 변경할 수 있습니다:

1. 커스텀 모델 파일(.pt)을 프로젝트 폴더에 추가
2. `app.py` 파일의 다음 줄을 수정:

```python
model = YOLO('your_custom_model.pt')
```

## 주의사항

- 첫 실행 시 YOLOv8s 모델이 자동으로 다운로드됩니다 (약 20MB)
- 대용량 이미지 처리 시 시간이 걸릴 수 있습니다
- 화재 감지의 정확도는 사용된 모델 및 이미지 품질에 따라 달라집니다 

## 라이선스

이 프로젝트는 [GNU Affero General Public License v3.0 (AGPL-3.0)](https://www.gnu.org/licenses/agpl-3.0.html)를 따릅니다.

프로그램을 사용하거나 배포하는 경우, 소스코드를 포함해 사용자에게 공개해야 합니다.  
자세한 사항은 LICENSE 파일을 참조하세요.
