<template>
  <q-page>
    <div class="row q-gutter-md wrap justify-center">
      <div class="col-12 col-sm-6 col-md-4 col-lg-3" v-for="lesson in lessons" :key="lesson.id">
        <q-card class="my-card" style="width: 400px; max-width: 100%; margin: 0 auto;" @click="openModal(lesson)">
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

    <!-- Modal -->
    <q-dialog v-model="dialog" @hide="resetLesson">
      <q-card class="custom-modal"> <!-- Özel sınıf ekliyoruz -->
        <q-card-section>
          <div class="text-h6">{{ selectedLesson.lesson_name }}</div>
          <q-img
            v-if="selectedLesson.image"
            :src="selectedLesson.image"
            alt="Modal Image"
            style=" height: 100px; width: 100%;"
          />




          <div class="q-pa-md">
    <div class="q-gutter-sm" v-for="subject in subjects" :key="subject.id">
    <q-list>
      <q-item tag="label" v-ripple>
        <q-item-section avatar>
          <q-checkbox v-model="color" :val="subject[0]" color="teal" />

        </q-item-section>
        <q-item-section>
          <q-item-label>{{ subject[0] }}</q-item-label>
        </q-item-section>
      </q-item>




    </q-list>
    </div>

    <div class="q-px-sm q-mt-sm">
      Your selection is: <strong>{{ color }}</strong>
    </div>
  </div>
        </q-card-section>
        <q-card-actions>
          <q-btn label="Close" @click="dialog = false" color="primary" />
        </q-card-actions>
      </q-card>
    </q-dialog>


  </q-page>
</template>


<script>
import axios from 'axios'
import { ref } from 'vue'
export default {
  setup () {
    return {
      color: ref([])
    }
  },
  data() {
    return {
      userInfo: {
        username: this.$route.params.username,
      },
      lessons: [], // API'den gelen ders verileri burada tutulacak
      dialog: false, // Modalın açık olup olmadığını kontrol eden değişken
      selectedLesson: {}, // Seçilen dersin bilgileri
      subjects: [] //Derse ait konular
    }
  },
  created() {
    // Sayfa yüklendiğinde API'den ders verilerini çek
    axios.post('http://127.0.0.1:5000/api/getTeacherLessons', this.userInfo)
      .then(response => {
        this.lessons = response.data;
        for (let i = 0; i < this.lessons.length; i++) {
          this.lessons[i]["image"] = `data:image/jpg;base64,${this.lessons[i]["image"]}`;
        }
      })
      .catch(error => {
        console.error("Veriler alınırken hata oluştu:", error);
      });
  },
  methods: {
    openModal(lesson) {
      // Seçilen dersi modal için ayarlayın ve modalı açın
      this.selectedLesson = lesson;
      this.dialog = true; // Modalı aç
        // Seçilen dersin detaylarını veritabanından çek
        axios.post('http://127.0.0.1:5000/api/getSubjects',this.selectedLesson)
        .then(response => {
          // Gelen veriyi modalda göstermek için ayarlayın
          this.subjects = response.data;
            console.log("Deneme"+this.color)
        })
        .catch(error => {
          console.error("Ders detayları alınırken hata oluştu:", error);
        });
      this.dialog = true;

    },
    resetLesson() {
      // Modal kapatıldığında seçilen dersi sıfırlayın
      this.selectedLesson = {};
      this.color = []; // Checkbox seçimlerini sıfırlar
    }
  }
}
</script>

<style>
.my-card {
  width: 400px; /* Kart genişliğini artırdık */
  max-width: 100%; /* Ekrana göre esnek olmasını sağlıyoruz */
  height: 200px; /* Kart yüksekliğini ayarlayın */
}
.custom-modal {
  width: 80%; /* Modal genişliği */
  max-width: 600px; /* Maksimum genişlik */
}
</style>
