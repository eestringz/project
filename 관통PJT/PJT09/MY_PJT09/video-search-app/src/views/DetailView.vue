<template>
  <div class="d-flex flex-column w-75 p-3" style="margin: 0 auto;">

    <div class="d-flex mt-4 mb-3" @click="goBack">
      <img src="@/assets/arrowbutton.jpg" style="width: 30px;">
      <button class="back-button">BACK</button>
    </div>

    <div v-if="video.snippet">
      <p class="fs-1">{{ video.snippet.title }}</p>
      <p class="fs-5 fw-light">채널명 : {{ video.snippet.channelTitle }}</p>
      <p style="margin-top: 20px;">업로드 날짜 : {{ video.snippet.publishedAt.substring(0,10)}}</p>
      <!-- <iframe> 요소는 웹 페이지 내에서 외부 웹 페이지나 다른 문서를 포함시키기 위해 사용되는 HTML 태그 -->
      <!-- video.id 는 동적 데이터이므로 URL을 동적으로 사용해야함. -->
      <iframe 
        :src="'https://www.youtube.com/embed/' + video.id" 
        frameborder="0"
        width="100%"
        height="600px"
      ></iframe>
      <p style="word-break: break-all; white-space: pre-line;">{{ video.snippet.description }}</p>
      <button @click="saveVideo(video)" class="save-button">나중에 볼 동영상으로 저장</button>
    </div>
    <div v-else>
      <p>로딩 중...</p>
    </div>
    
  </div>

</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRoute, useRouter } from 'vue-router';

const video = ref({})
const apiKey = "AIzaSyC649LETwO62B76kuAVXau6SiYdmHG7iRM"
const route = useRoute()
const router = useRouter()


onMounted(() => {
  fetchVideoDetail()
})

const fetchVideoDetail = () => {
  const videoId = route.params.videoId
  // console.log(videoId)
  axios
    .get("https://www.googleapis.com/youtube/v3/videos", {
      params: {
        part : 'snippet',
        id : videoId,
        key : apiKey,
      }
    })
    .then((response) => {
      // console.log(response)
      // console.log(response.data.items[0])
      video.value = response.data.items[0]
      // console.log(video)
    })
    .catch((error) => {
      console.log('에러가 발생하였습니다.', error)
    })

}

// 뒤로가기
const goBack = () => {
  router.go(-1)
}


const saveVideo = (video) => {
  // 하나의 데이터만 저장하기
  // 문제점 : 데이터가 덮어쓰기 된다.
  // localStorage.setItem('savedVideos', JSON.stringify(video))

  // 여러 데이터 저장하기
  // 현재 localStorage에 저장된 데이터 가져오기
  // 만약 없다면 비어있는 리스트로 초기화 (null 로 인해 오류 발생할 수 있음.)
  const savedVideos = JSON.parse(localStorage.getItem('savedVideos')) || []

  // console.log(video.id)
  // console.log(savedVideos)

  // 중복된 데이터가 있는지 확인
  const isDuplicate = savedVideos.length > 0 && savedVideos.find((item) => item.id === video.id)

  // 중복이 아니라면 추가
  if (!isDuplicate) {
    savedVideos.push(video)
    alert('나중에 볼 동영상이 저장되었습니다. 나중에 볼 동영상 목록으로 이동합니다.')
  }
  else {
    alert('이 동영상은 이미 저장되어 있습니다. 나중에 볼 동영상 목록으로 이동합니다.')
  }

  // 수정된 savedvideds 데이터를 localStorage에 추가
  localStorage.setItem('savedVideos', JSON.stringify(savedVideos))

  // 나중에 볼 동영상 view로 이동
  router.push('/later')


}



</script>

<style scoped>
.save-button {
  background-color: #f9f9f9;
  border: 1px solid #ccc;
  text-align: center;
  border-radius: 5px;
}
</style>
