<template>
  <div class="d-flex flex-column w-75 p-3" style="margin: 0 auto;">

    <div class="d-flex mt-4 mb-3" @click="goBack">
      <img src="@/assets/arrowbutton.jpg" style="width: 30px;">
      <button class="back-button">BACK</button>
    </div>

    <h1 class="fs-1 fw-medium">나중에 볼 동영상</h1>

    <div v-if="savedVideos && savedVideos.length > 0" class="video-list">
      <div v-for="(video,index) in savedVideos" :key="index" class="video-card">
      
        <div @click="goDetail(video)">
          <img :src="video.snippet.thumbnails.medium.url" alt="YouTube Video Thumbnail" class="image-box">
          <p>{{ video.snippet.title }}</p>
        </div>

        <button @click="removeSavedVideo(video)" class="delete-button">나중에 볼 동영상에서 삭제</button>
      
      </div>
    </div>
    <div v-else>
      <p class="fs-5 fw-ligh" style="margin-top: 20px;">등록된 비디오 없음</p>
    </div>

  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router';


const savedVideos = ref(null)
savedVideos.value = JSON.parse(localStorage.getItem('savedVideos'))

const router = useRouter()

// 뒤로가기
const goBack = () => {
  router.go(-1)
}

const goDetail = (video) => {
  router.push(`/videos/${video.id}`)
}


const removeSavedVideo = (video) => {
  const itemIdx = savedVideos.value.findIndex((item) => item.id === video.id )

  savedVideos.value.splice(itemIdx, 1)

  localStorage.setItem('savedVideos', JSON.stringify(savedVideos.value))
}

</script>


<style scoped>
.video-card h4 {
  margin: 15px;
  font-weight: bold;
}

.image-box {
  width: 100%;
  border-radius: 10px;
}

.delete-button {
  background-color: #f9f9f9;
  border: 1px solid #ccc;
  text-align: center;
  border-radius: 5px;
  margin-left: 10px;
  margin-bottom: 10px;
}
</style>

