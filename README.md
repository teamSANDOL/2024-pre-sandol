![](https://github.com/teamSANDOL/kpu_sandol_team/blob/main/img/logo_profile3.png?raw=true)
# 미션
---
## 개발자
### 개발자 공통 요구사항
- 모든 미션은 Jetbrains의 Pycharm을 기준으로 구현되어있다.
- 기능을 구현하기 전 `docs/README.md`에 **구현할 기능 목록을 정리해 추가한다.**
**- `requirement.txt`에서 제공된 라이브러리만 사용하여 개발해야 한다.**
	- [PyCharm에서 requirement.txt 다운로드 하는 방법](https://www.jetbrains.com/help/pycharm/managing-dependencies.html#revert-ignored)
	- [Requirement.txt 사용법](https://engineer-mole.tistory.com/258)
- 파이썬 버전 3.7 이상에서 실행 가능해야 한다.
- 기능요구사항에 있는 모든 기능을 구현하여야 한다.
- 제출 전 테스트 파일에 있는 모든 테스트를 통과하여야 한다.
	- [PyCharm에서 테스트를 실행하는 방법](https://www.jetbrains.com/help/pycharm/testing-your-first-python-application.html#write-test)
	- [Python unittest 라이브러리 docs](https://docs.python.org/ko/3/library/unittest.html)
    - **해당 라이브러리를 사용하여 `\test`아래에 각각 필요한 유닛테스트를 시행한다**
    - 유닛테스트에 대한 참고사항은 [여기](https://kchanguk.tistory.com/40)를 참고한다.
- **요구사항에 없는 기능은 스스로 판단하여 구현한다.**
- **모든 백엔드 개발자는 `utility/Frozen`사용이 가능하다. 사용법은 해당 문서 최 하단에 있다.**

### API 개발
#### 요구사항


#### 입력 예시
```
```

#### 출력 예시
```
```

---
### 기능 개발
#### 요구사항
- 최근 학사정보에 접근하기 힘들다는 학우들의 의견을 반영하여 산돌이에서 학사 공지 중 주요 공지를 보여주고자 한다.
- 학사 공지는 [여기](https://www.tukorea.ac.kr/tukorea/1096/subview.do)에서 확인할 수 있다.
- 주요공지는 아래 이미지처럼 번호에 마이크모양이 있는것을 의미한다.
- ![tuk-info.png](resource%2Fimg%2Ftuk-info.png)
- 필요한 정보는 `제목, 작성자, 작성일`이며, 클릭시 해당 게시글로 갈 수 있도록 게시글의 하이퍼링크도 필요하다.
- 자세한 사항은 입출력 예시를 따른다.

#### 입력 예시
```text
아래 하이퍼링크에서 적절히 데이터를 받아온다
> https://www.tukorea.ac.kr/tukorea/1096/subview.do
```

#### 출력 예시
```json
```

## 마케터
#### 요구사항
- 산돌이는 kakao i openbuilder로 제작되어 있습니다. 이는 챗봇 관리자들이 간편하게 챗봇의 기능을 만들 수 있도록 구성되어있습니다.
- 오픈빌더는 크게 시나리오탭과 스킬탭으로 구성되어있는데 시나리오에서 산돌이의 기능 블록을 만들 수 있습니다.
- 예를들어 산돌이에 `셔틀`이라는 발화를 하면 봇 응답을 지정할 수 있습니다.
- 즉, 정적인 컨텐츠를 만드는데 사용됩니다.
- 스킬탭은 동적인 컨텐츠를 만드는데 사용됩니다. 웹서버와 연동하여 개발자가 응답을 자유롭게 생성할 수 있습니다.

초대해드린 [테스트 봇](https://i.kakao.com/bot/5ff710328c008e4e081b2f92/intent/new?scenarioId=default)을 산돌이와 최대한 비슷하게 시나리오 및 블럭을 구성하면 됩니다.

![openbuilder_example1.png](resource%2Fimg%2Fopenbuilder_example1.png)

---
# 제출 방법
- 제출 마감 기한은 2월 2일 금요일 오후 17:00까지이다.
- 상세한 제출방법은 다음 문서를 참고한다.

# 기타
## 테스트 실행방법
- business에 대한 테스트는 `\tests\test\integration_test`로 지정되어 있습니다. 해당 파일을 실행시키시면 pycharm기준 하단 파이썬 콘솔에 성공/실패여부가 자세하게 나옵니다.
- api에 대한 테스트는 `\tests\api_test\FlaskTestCase`에 있습니다.
- ![](../resource/img/test_screenshot1.png)
- ![test_screenshot2.png](resource%2Fimg%2Ftest_screenshot2.png)
## Flask 실행 법
```
api_dev/의 위치에서 flask run을 실행한다.
만약 "You did not provide the "FLASK_APP" environment variable"과 같은 오류 발생시 환경변수 설정(하단)을 따른다
```

### 환경변수 설정
- https://teki.tistory.com/37
- `set FLASK_APP = app`을 실행 한뒤 서버를 실행시킨다.

## FacadeJSON
- 파이썬에서 JSON을 편하게 사용할 수 있도록 도와주는 (제작된)라이브러리
### 기존 사용법
```python
content = json.loads(f)
print(content['status'])
```

### FacadeJSON
```python
content = FacadeJSON(json.loads(f))
print(content.status)
```
