<template>
  <q-page>,
    <div v-if="loading" class="loading-indicator">
      <q-spinner-dots color="primary" /> <!-- You can use any loading spinner component you prefer -->
      <div>Yükleniyor...</div> <!-- Loading text -->
    </div>
    <div  class="q-pa-md row items-start q-gutter-md"  v-for="f in feedbacks" :key="f.id"  >
    <q-card class="my-card" style="width: 100%; max-width: 1000px; height: 300px;">
      <q-card-section class="bg-primary text-white">
        <div class="text-h6">Geri Bildirim</div>
        <div class="text-subtitle2">{{ lessons[f.lesson_id -1] }}</div>
      </q-card-section>
      <q-separator />

      <q-card-actions align="right">
        {{ f.text }}
      </q-card-actions>
    </q-card>
  </div>
  </q-page>
  </template>

<script>
import { ref } from 'vue';
import axios from 'axios';

export default {
  data(){
    return{
      feedbacks :[],
      lessons : ["Matematik","Kimya","Türkçe","Fizik","Tarih","Biyoloji","Edebiyat"],
      loading: true
    }
  },
  created (){
    this.feedbacks = []
    axios.post("http://127.0.0.1:5000/api/getFeedbacks")
        .then(response => {
          this.feedbacks = response.data
        })
        .catch(error => {
          console.error("Veriler alınırken hata oluştu:", error);
        })
        .finally(() => {
          this.loading = false;

      });;
    },
  }
</script>
<style>
.loading-indicator {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
}
</style>
