<template>
  <div class="d-flex flex-column w-75 p-3" style="margin: 0 auto;">

    <div class="d-flex mt-4 mb-3" @click="goBack">
      <img src="@/assets/arrowbutton.jpg" style="width: 30px;">
      <button class="back-button">BACK</button>
    </div>

    <h1 class="fs-1 fw-medium">비디오 검색</h1>

    <nav class="navbar">
      <div style="width: 100%;">
        <form class="d-flex" role="search" @submit.prevent="searchYoutube">
          <input class="form-control" 
            type="text" 
            placeholder="검색어를 입력하세요." 
            aria-label="Search" 
            v-model="searchQuery"
            @keyup.enter="searchVideos">
          <button class="btn btn-outline-success" 
            style="width: 100px;" 
            type="submit"
            @click="searchVideos">검색
          </button>
        </form>
      </div>
    </nav>

    <div class="video-list">
      <!-- 각 video를 YoutubeVideo 로 prop -->
      <YoutubeVideo 
        v-for="(video,index) in videos" :key="index"
        :thumbnail="video.snippet.thumbnails.medium.url"
        :title="video.snippet.title"
        @handle-click="goDetail(video.id.videoId)"
      />
    </div>

  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRoute, useRouter } from 'vue-router';
import YoutubeVideo from '@/components/YoutubeVideo.vue'

const searchQuery = ref('')
const videos = ref([])
const apiKey = "AIzaSyC649LETwO62B76kuAVXau6SiYdmHG7iRM"
const router = useRouter()


const searchVideos = () => {
  axios
    .get("https://www.googleapis.com/youtube/v3/search", {
      params: {
        part : 'snippet',
        q : `${searchQuery.value}`,
        key : apiKey,
        type : "video",
        maxResults : 50,
      }
    })
    .then((response) => {
      videos.value = response.data.items
    })
    .catch((error) => {
      console.error("에러가 발생하였습니다.", error)
    })
}


// 뒤로가기
const goBack = () => {
  router.go(-1)
}


// 동영상 디테일 페이지로 이동하는 로직(YoutubeVideo에서 썸네일/제목 클릭시 활성화)
const goDetail = (videoId) => {
  // console.log(videoId)
  router.push({ name : 'detail', params : {videoId} })
}


</script>


<style scoped>

</style>


<style>
.video-list {
  display: flex;
  flex-wrap: wrap;
  gap: 30px;
}

.back-button {
  background-color: #f9f9f9;
  border: 1px solid #ccc;
  text-align: center;
  border-radius: 5px;
}
</style>