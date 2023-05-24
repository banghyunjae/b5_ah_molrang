# b5_ah_molrang

동현: 소셜로그인 기능 구현을 위해선 아래와 같은 절차를 따라주세요.
<br/>
<br/>
[공통]
<br/>
소셜로그인 기능을 구현하기 위해서 pip install django-allauth 가 되어있어야 합니다.
<br/>
<br/>
[카카오로그인]
<br/>
1. https://developers.kakao.com/ 방문
<br/>
2. 회원가입
<br/>
3. 내 애플리케이션 > 애플리케이션 추가하기 > 로고, 앱이름, 사업자명 임의로 작성, 정책위반아님 체크
<br/>
4. 생성된 애플리케이션 클릭 > REST API 키 복사해서 아무데나 메모장에 잘 적어놓기
<br/>
5. 왼쪽 카테고리 중 보안 > Client Secret 코드생성 > 생성된 코드 복사해서 아까 REST API 키와 함께 메모장에 잘 적어놓기 > 활성화 클릭
<br/>
6. 왼쪽 카테고리 중 카카오 로그인 > 상태 ON
<br/>
7. 같은 화면의 하단에 Redirect URI 등록 클릭 > 줄바꿈 가능하니 다음과 같은 url 두 줄 입력
<br/>
http://127.0.0.1:8000/accounts/kakao/login/callback/
<br/>
http://127.0.0.1:8000
<br/>
8. 왼쪽 카테고리 중 동의항목 > 사용자로부터 받을 개인정보 (닉네임 있으면 필수동의, 이메일 있으면 선택동의) 설정을 필요에 맞게 설정
<br/>
9. 수퍼유저생성 및 런서버 된 상태에서 브라우저에서 http://127.0.0.1:8000/admin/ 접속
<br/>
10. 소셜계정 카테고리 중 소셜 어플리케이션 > 우측 상단 소셜 어플리케이션 추가 버튼 > 제공자 카카오 > 이름 카카오로그인
<br/>
11. 클라이언트 아이디: 아까 적어 둔 REST API 키 , 비밀 키: 아까 적어 둔 Client Secret 코드
<br/>
12. 마지막으로 Sites: 목록에 뜬 url들 중 http://127.0.0.1:8000 이것과 http://127.0.0.1:8000/accounts/kakao/login/callback/ 이것을 선택해서 오른쪽으로 옮기면 카카오 로그인을 위한 준비작업 끝.
<br/>
**백엔드 연결포트가 8000번이 아니거나 배포를 위한 도메인이 따로 있을 경우, 위에서 언급된 http://127.0.0.1:8000 들의 경로를 상황에 맞게 수정합니다.
<br/>
<br/>
[구글로그인]
<br/>
1.https://console.developers.google.com/ 접속 > 로그인 및 약관 동의
<br/>
2.탑 배너의 GoogleAPIs로고 오른쪽에 있는 프로젝트 선택 클릭 > 팝업에서 새 프로젝트 > 프로젝트 이름 임의로 설정 > 만들기
<br/>
3.프로젝트 생성까지 시간이 좀 걸림 > 생성되면 똑같이 탑배너에서 프로젝트 선택하여 생성한 프로젝트로 이동
<br/>
4.화면 좌측 상단 모서리에 삼선 아이콘 클릭 > API 및 서비스 > 사용자 인증 정보 > 동의 화면 구성 (닉네임 필수동의, 이메일 선택동의 + 카카오로부터 제공받기) > 외부 > 만들기
<br/>
5.애플리케이션이름 임의로 설정 > 동의항목 문의용 이메일 입력(개발자 이메일) > 하단에 한 번 더 이메일 입력 > 저장
<br/>
**그외 빨간 별표 있는 항목 모두 기입
<br/>
6.몇 단계 더 있는듯 보이나 할 필요 없고 OAuth 동의 완성 됨
<br/>
7.다시 사용자 인증정보 카테고리로 이동 > OAuth 2.0 클라이언트 ID 만들것임. 상단에 사용자 인증 정보 만들기 > OAuth 클라이언트 ID
<br/>
8.애플리케이션유형 > 웹 애플리케이션 > 이름 임의로 설정 > 승인된 자바스크립트 URI에 http://127.0.0.1:8000 추가
<br/>
9.승인된 리디렉션 URI에 http://127.0.0.1:8000 추가, http://127.0.0.1:8000/accounts/google/login/callback/ 추가.
<br/>
10.팝업창에서 생성된 클라이언트 ID와 클라이언트 보안 비밀번호를 메모장에 잘 적어둔다.
<br/>
11.수퍼유저생성 및 런서버 된 상태에서 브라우저에서 http://127.0.0.1:8000/admin/ 접속
<br/>
12.소셜계정 카테고리 중 소셜 어플리케이션 > 우측 상단 소셜 어플리케이션 추가 버튼 > 제공자 google > 이름 구글로그인
<br/>
13.클라이언트 아이디: 아까 적어 둔 클라이언트 ID, 비밀 키: 아까 적어 둔 클라이언트 보안 비밀번호 기입.
<br/>
14.마지막으로 Sites: 목록에 뜬 url들 중 http://127.0.0.1:8000 이것과 http://127.0.0.1:8000/accounts/google/login/callback/ 이것을 선택해서 오른쪽으로 옮기면 구글 로그인을 위한 준비작업 끝.
<br/>
**백엔드 연결포트가 8000번이 아니거나 배포를 위한 도메인이 따로 있을 경우, 위에서 언급된 http://127.0.0.1:8000 들의 경로를 상황에 맞게 수정합니다.
<br/>
프론트와 서버를 연결할 때 우회해서 갈 수 있도록 CORS를 넣었습니다. 실행하시기전에 pip install django-cors-headers
해주세욥 ~현재