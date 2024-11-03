<template>
  <q-page>
    <div v-if="loading" class="loading-indicator">
      <q-spinner-dots color="primary" />
      <div>Yükleniyor...</div>
    </div>
    <div class="q-pa-md row items-start q-gutter-md" v-if="!loading">
      <q-card class="my-card" style="width: 100%; max-width: 1000px; height: 500px;">
        <q-card-section class="bg-primary text-white">
          <div class="text-h6">Ders Geri Bildirimi</div>
        </q-card-section>
        <q-card-section style="height: 80%;">
          <q-form @submit="submit" class="q-gutter-md" style="height: 100%; width: 100%;">
            <div style="height: 100%;">
              <q-input
                v-model="text"
                filled
                type="textarea"
                rows="13"
              />
              <q-select
                v-model="selectedOccupation"
                :options="occupationOptions"
                id="occupation"
                label="Ders Seçimi"
                emit-value
                map-options
              />
              <br>
              <q-btn style="width: 100%;" label="Gönder" type="submit" color="secondary"/>
            </div>
          </q-form>
        </q-card-section>
      </q-card>
    </div>

    <!-- Dialog for submission confirmation -->
    <q-dialog v-model="submitted" persistent>
      <q-card>
        <q-card-section>
          <div class="text-h6">İşlem Tamamlandı!</div>
        </q-card-section>
        <q-card-actions>
          <q-btn label="Tamam" color="primary" @click="submitted = false" />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>
<script>
import { ref } from 'vue';
import axios from 'axios';

export default {
  setup() {
    const text = ref('');
    const selectedOccupation = ref(null);
    const occupationOptions = [
      { label: 'Matematik', value: '1' },
      { label: 'Kimya', value: '2' },
      { label: 'Türkçe', value: '3' },
      { label: 'Fizik', value: '4' },
      { label: 'Tarih', value: '5' },
      { label: 'Biyoloji', value: '6' },
      { label: 'Edebiyat', value: '7' },
    ];

    return {
      text,
      selectedOccupation,
      occupationOptions,
    };
  },
  data() {
    return {
      feedback_info: { text: '', lesson: '' },
      loading: false,
      submitted: false, // Track submission status
    };
  },
  methods: {
    submit(event) {
      event.preventDefault(); // Prevent default form submission
      this.loading = true; // Set loading to true
      this.submitted = false; // Reset submitted state
      this.feedback_info.text = this.text; // Use this.text
      this.feedback_info.lesson = this.selectedOccupation; // Use this.selectedOccupation

      axios.post("http://127.0.0.1:5000/api/postFeedback", this.feedback_info)
        .then(response => {
          // Handle success (optional)
        })
        .catch(error => {
          console.error("Veriler alınırken hata oluştu:", error);
        })
        .finally(() => {
          this.loading = false; // Hide loading
          this.submitted = true; // Show dialog after submission
        });
    },
  },
};
</script>
