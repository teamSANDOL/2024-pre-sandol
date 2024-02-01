# main
## app_main()
1. import requests, json

2. url
- 서울 열린데이터 -> 샘플 데이터 url 사용
- url data 가공
  - integration_test 용으로 url 대신 RawSubwayArrival.json 파일로 경로 대체

3. 데이터 추출
- 도착지 방면: trainLineNm
- 첫번째 도착 메세지 : arvlMsg2
- 5개 소스 추출, for문으로 각 리스트에 append

4. result 딕셔너리 생성, zip(도착지, 도착메세지)

5. status: errorMessage.message 데이터 추출

6. 최종 딕셔너리 생성
- {"result" : result(list), "status" : status(data)}
- return 값으로 설정

### 예외처리
1. data에 'result' 키가 없으면 에러 메시지 반환
   - [Error] 데이터를 받아오지 못했습니다.
2. data에 'result'가 공백이면 에러 메시지 반환
   - [Error] 도착 정보가 없습니다.


## integration_test()
1. setUp()
- encoding error 이슈
- open() - encoding='utf-8' 인수 추가.
  - 해결!


# api_dev 
flask 미설치 이슈로 결과 확인은 못했습니다...

### app()
1. from week1.business_dev.main import app_main 모듈 추가
2. __load_json(path) 함수에 app_main 값 복사
3. add_text_element() 함수 생성
   - content 값을 ui대로 가공하여 body의 simpleText에 추가

flask 미숙으로 FlaskTestCase 까지 검사하진 못햇씁니다..