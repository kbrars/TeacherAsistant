<template>
  <q-page >
    <div class="row q-gutter-md wrap justify-center">
  <div class="col-12 col-sm-6 col-md-4 col-lg-3" v-for="lesson in lessons" :key="lesson.id">
    <q-card class="my-card" style="max-width: 300px; margin: 0 auto;">
      <q-img
            v-if="lesson.image"
            :src="lesson.image"
            alt="Database Image"
            style="object-fit: cover; height: 150px;"
          >
            <div class="absolute-bottom text-subtitle2 text-center bg-black text-white" style="opacity: 0.7; padding: 5px;">
              {{ lesson.lesson_name }}
            </div>
          </q-img>
    </q-card>
  </div>
</div>

  </q-page>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {

      userInfo :{
        username: this.$route.params.username,
      },
      lessons: [] // API'den gelen ders verileri burada tutulacak
    }
  },
  created() {
    // Sayfa yüklendiğinde API'den ders verilerini çek
    axios.post('http://127.0.0.1:5000/api/getTeacherLessons',this.userInfo)
      .then(response => {
        console.log(response)
        this.lessons = response.data
        for (let i = 0; i < this.lessons.length; i++)
          this.lessons[i]["image"] = `data:image/jpg;base64,${this.lessons[i]["image"]}`;

      })
      .catch(error => {
        console.error("Veriler alınırken hata oluştu:", error)
      })
  }
}
</script>

<style>
.my-card {
  width: 300px; /* Kart genişliğini ayarlayabilirsiniz */
  height: 200px;
}
</style>
