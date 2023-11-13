<template>
  <div class="video-card" @click="handleClick">
    <img :src="thumbnail" alt="YouTube Video Thumbnail" class="image-box">
    <p v-html="title"></p>
  </div>
</template>

<script setup>

defineProps(['thumbnail', 'title'])
const emit = defineEmits(["handleClick"])

// 썸네일/제목 클릭시 부모에게 emit
const handleClick = () => {
  emit("handleClick")
}

</script>


<style scoped>
.video-card img {
  width: 100%;
  border-radius: 10px;
}
</style>


<style>
.video-card {
  margin-top: 20px;
  border: 1px solid lightgray;
  width: 30%;
  border-radius: 10px;
}

.video-card:hover {
  transform: scale(1.02);
}

.video-card p {
  margin: 10px;
  font-weight: bold;
  text-overflow: ellipsis;  /* 텍스트가 넘칠 때 생략 부호 (...) 표시 */
  white-space: nowrap;      /* 텍스트 자르기 */
  overflow: hidden;         /* 오버플로우 처리 */
}
</style>