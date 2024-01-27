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
    - 이 문서 하단에 테스트와 관련된 항목이 존재하므로 참고한다.
- **요구사항에 없는 기능은 스스로 판단하여 구현한다.**


### API 개발
#### Flask 실행법 및 파일 구조
##### Flask
- 제시된 파일에는 `\week2\api_dev\.venv`에 가상환경이 구성되어있다.
- 아래 명령어로 가상환경에 진입한다.(mac 기준)
- 윈도우의 경우 [해당 링크](https://hcnoh.github.io/2019-06-19-windows-python-virtualenv)의 설명을 따른다.
- 이후 app.py를 실행시키면 자동으로 서버가 실행될 것이다.


#### 요구사항
- 산돌이에 가장 인기 있는 기능인 "학식"은 산돌이 개발자가 직접 업주에게 연락하여 매일 수동으로 업데이트 하고 있다.
- 산돌팀 회의에서 이 과정이 복잡하고 지속가능하지 못하다 판단하여 업주들에게 산돌이에 접근할 수 있는 권한을 부여해 직접 업로드를 하려고한다.
- 산돌이에 메뉴를 알려주는 업체는 "산돌 분식", "한공 푸드", "티노 샌드위치"이다.
- 카카오톡에는 채팅방마다 고유한 id를 부여하여 사용자를 구분하는데 개발진은 임시로 이를 이용하기로 했다.
- 메뉴를 저장할 저장소는 아직 정하지 못하였으므로 메모리 상에 저장하며, 나중에 Amazon S3버킷으로 리펙토링될 가능성이 있다.
- 저장될 파일 명은 menu.json으로 `repo/menu.json`에 저장되어 있다.

---
- `/updateMenu`는 메뉴를 업데이트하는 항목이다.
  - 업주가 업데이트 하려는 가게가 업주의 소유인 경우에만 업데이트를 허용한다.
  - 업체의 메뉴가 저장된 파일에 이미 메뉴가 존재한다면 이전 메뉴를 모두 삭제한 뒤 새로운 데이터를 덮어쓴다.
  - 덮어쓰기에 성공했다면 성공메시지를 리턴한다.


```shell
source .venv/bin/activate
```

#### 입력 예시
```text
 - 봇 아이디 목록
 산돌 분식 : 5e0d180affa74800014bd33d
 한공 푸드 : 3c0f223affa74800024ac31c
 티노 샌드위치 : s2134a85n8021d1w87it3c3h
```

```json
{
  "bot": {
    "id": "5e0d180affa74800014bd33d",
    "name": "산돌이"
  },
  "action": {
    "name": "jp1j2gy39h",
    "clientExtra": null,
    "params": {
      "store_name": "산돌 분식",
      "lunch_menu": "떡볶이, 순대, 튀김",
      "dinner_list": "짜장면, 짬뽕국, 탕수육"
    },
    "id": "bwjfe6fxc96ngv9ra6dddzah"
  }
}
```
> bot.id가 발화한 사용자의 아이디이다. 또한 입력은 POST로 api에 전달된다.
> 
#### 출력 예시
```json
{
  "response": {
    "version": "2.0",
    "template": {
      "outputs": [
        {
          "simpleText": {
            "text": "성공적으로 저장하였습니다",
            "text": "[ERROR] 오류상황에 맞는 메시지 출력"
          }
        }
      ]
    }
  }
}
```

#### 파일 저장 예시
```json
{
  "store" : [
    {
      "name":  "산돌 분식", 
      "menu" : {
        "lunch" : ["떡볶이", "순대", "튀김"], 
        "dinner" : ["짜장면", "짬뽕국", "탕수육"]
      }
    },
    {
      "name":  "한공 푸드", 
      "menu" : {
        "lunch" : ["라면", "김밥", "주먹밥"], 
        "dinner" : ["식빵", "딸기잼", "우유"]
      }
    },
    {
      "name":  "티노 샌드위치", 
      "menu" : {
        "lunch" : ["이탈리안 샌드위치", "불고기 샌드위치"], 
        "dinner" : ["치즈 샌드위치, 핫도그"]
      }
    },    
  ],

}

```
> simpleText 안의 text는 성공과 실패에 각각 출력할 문구이다. 둘 중 하나만 출력하면 된다.

---
### 기능 개발

#### 요구사항
- 최근 학사정보에 접근하기 힘들다는 학우들의 의견을 반영하여 산돌이에서 학사 공지 중 주요 공지를 보여주고자 한다.
- 학사 공지는 [여기](https://www.tukorea.ac.kr/tukorea/1096/subview.do)에서 확인할 수 있다.
- 주요공지는 아래 이미지처럼 번호에 마이크모양이 있는것을 의미한다.
- ![tuk-info.png](resource%2Fimg%2Ftuk-info.png)
- 필요한 정보는 `제목, 작성자, 작성일`이며, 클릭시 해당 게시글로 갈 수 있도록 게시글의 하이퍼링크도 필요하다.
- 자세한 사항은 입출력 예시를 따른다.
- 상수를 따로 관리할 방법을 찾는다. 예를들면 URL과 같은 것들을 따로 constant.py에 정의 한 뒤 사용한다
- `week2/business_dev/main.py`파일의 run 파일의 결과로 출력 결과를 반환한다. (함수의 이름을 수정해선 안된다.)
  - 이외의 파일들은 자유롭게 생성해도 된다.

#### 파일 구조
```text
.
├── __init__.py
├── docs
│   └── README.md
├── lib
│   ├── __init__.py
│   └── frozen_json.py
├── main.py
└── tests
    ├── __init__.py
    └── test_main.py
```
- 위 트리의 예시는 business_dev의 파일구조이다.
- `\docs` : 개발을 진행하면서 작성할 개발문서이다.
- `\lib` : 필요하다면 사용이 가능한 라이브러리이다.
- `\tests` : 테스트 파일이 존재한다. 과제제출 전 test_main.py를 실행시켜 모든 테스트를 통과해야 한다.
- `main.py` : 출력 결과를 반환하는 함수 run()이 존재한다. 즉, 최종 프로그램의 완성은 해당 파일에서 개발한다.


#### 입력 예시
```text
아래 하이퍼링크에서 적절히 데이터를 받아온다
> https://www.tukorea.ac.kr/tukorea/1096/subview.do
```

#### 출력 예시
```json
{"informations": [
	{
		"title": "[사회봉사교과목] 2024-1학기 사회봉사 교과목 수강신청 안내", 
		"author": "사회봉사지원센터", 
		"date": "2024.01.26", 
		"link": "/bbs/tukorea/107/51544/artclView.do"
	}, 
	{
		"title": "기초교과, 계열기초(1학년 신입생 교과) 수강신청 안내(재학생, 신입생)", 
		"author": "교양교육운영센터", 
		"date": "2024.01.25", 
		"link": "/bbs/tukorea/107/51534/artclView.do"
	}
]}

```
> 출력 예시에는 2개의 게시물만 포함하였지만 1페이지에 있는 모든 공지 게시물을 가져온다.
> link에는 root url을 제외한 세부 디렉터리 주소만 포함해도 된다.

## 마케터
#### 요구사항


---
# 제출 방법
- 제출 마감 기한은 2월 2일 금요일 오후 17:00까지이다.
- 상세한 제출방법은 다음 문서를 참고한다.

# 기타
## 테스트 실행방법
- 주어진 코드는 pycharm에서 동작하도록 설계되어 있으며, pycharm에서 해당 소스로 이동 후 실행시 자동으로 테스트를 진행하도록 되어있습니다.
- 만약 콘솔에서 테스트를 진행하고 싶다면 아래 사항을 따라 테스트 코드를 일부 수정해야합니다.
  - 콘솔에서 파일을 실행시키는 위치는 `/week2`입니다. 
  - ModuleNotFoundError 또는 ImportError발생시 import 구문을 아래와같이 수정합니다.
```python
from unittest import TestCase
from ..main import run
```
- ![](../resource/img/test_screenshot1.png)
- ![test_screenshot2.png](resource%2Fimg%2Ftest_screenshot2.png)
## Flask 실행 법
```
api_dev/의 위치에서 flask run을 실행한다.
만약 "You did not provide the "FLASK_APP" environment variable"과 같은 오류 발생시 환경변수 설정(하단)을 따른다
```

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
