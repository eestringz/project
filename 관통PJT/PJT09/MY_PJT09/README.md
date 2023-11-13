# 프로젝트 소개
> 관통 09_pjt. Vue를 활용한 동영상 검색 관리 서비스 구현

- 목표 
  - 동영상 검색 및 나중에 볼 영상을 저장할 수 있는 서비스 구현

- 특징 
  - 외부 API(Youtube API)를 통한 데이터 수집

- 팀원
  - 오유진


<br>

# 프로젝트 구조
## 개발 도구
- Visual Studio Code 
- Google Chrome
- Node.js LTS
- Vue.js 3.x


## 요구 사항
**요구사항 완성 후에 Bootstrap 을 이용하여 자유롭게 스타일링한다.**
1. 동영상 검색결과 출력
2. 동영상 상세 정보 출력
3. 나중에 볼 동영상 저장 및 삭제
4. 내가 좋아하는 채널 저장 및 삭제 (도전과제)
 

## 구현 상세 
1. 동영상 검색결과 출력
    - 네비게이션 바에서 Search 링크 클릭
    - 원하는 검색어 입력
    - `YouTube API` 로부터 JSON 데이터 요청

```html
import { RouterLink, RouterView } from 'vue-router'

    <RouterLink to="/" class="nav-link">Home</RouterLink>  
    <RouterLink to="/search" class="nav-link">Search</RouterLink> 
    <RouterLink to="/later" class="nav-link">Later</RouterLink>  
  <RouterView />
```

2. 동영상 상세 정보 출력
    - 검색결과에서 특정 비디오 클릭
    - 동영상에 대한 상세 정보  출력
    - `iframe 태그` 활용해 동영상 재생
    - 동영상 저장
    - `Local Storage` 활용
    - 저장 안 된 동영상 => 동영상 저장 버튼
    - 저장된 동영상 => 저장 취소 버튼



3. 나중에 볼 동영상 저장 및 삭제
    - 저장된 동영상 목록 확인
    - Local Storage 활용
    - 등록된 동영상 없을 경우 => 등록된 비디오 없음 출력


4. 내가 좋아하는 채널 저장 및 삭제 (도전과제)
    - 상세 페이지에 채널 저장 기능 추가
    - 클릭 시 Local Storage 활용해 채널 저장
    - 채널 페이지 접속 시 저장된 채널 목록 출력


## 참고 사항
**Youtube API 발급**

Docs: https://developers.google.com/youtube/v3/getting-started?hl=ko



<br>

# 회고
## 문제해결
**local storage에 여러 데이터 저장하기**
```js
  // 하나의 데이터만 저장하기
  // 문제점 : 데이터가 덮어쓰기 된다.
  localStorage.setItem('savedVideos', JSON.stringify(video))
  
  // 여러 데이터 저장하기
  // 현재 localStorage에 저장된 데이터 가져오기
  // 만약 없다면 비어있는 리스트로 초기화 (null 로 인해 오류 발생할 수 있음.)
  const savedVideos = JSON.parse(localStorage.getItem('savedVideos')) || []
```




## 새롭게 습득한 내용
> `iframe tag` : iframe 요소는 웹 페이지 내에서 외부 웹 페이지나 다른 문서를 포함시키기 위해 사용되는 HTML 태그 
>
> video.id 는 동적 데이터이므로 URL을 동적으로 사용 해야 함. 

>`local storage`


## 느낀점
> 전반적으로 vue에 대한 공부가 더 필요하다고 느낀 프로젝트였다. 
> 특히, router에 대한 부분이 많이 부족했던 것 같다.
>
> 이를 제외하고는 css 부분에서 많은 시간을 쏟았다. 
> 이후에 css를 더 깔끔학게 수정해야겠다. 