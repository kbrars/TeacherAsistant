<template>
  <q-layout>
    <q-page-container>
      <q-page padding class="flex flex-center">
        <!-- Uyarı mesajı -->
        <q-form
          class="column q-pa-md shadow-3"
          @submit.prevent="createPost"
          method="POST"
          :style="{ maxWidth: formWidth, width: '100%', maxHeight: formHeight, height: '100%' }"
        >
          <q-input
            v-model="form.username"
            name="username"
            placeholder="Kullanıcı adınız"
            :rules="[requiredRule_userName]"
          />
          <q-input
            v-model="form.password"
            type="password"
            name="password"
            placeholder="Şifreniz"
            :rules="[requiredRule_password]"
          />
          <q-btn
            label="Giriş Yap"
            type="submit"
            color="indigo"
            style="height: 40px; margin-top: 15px;"
          />
        </q-form>
      </q-page>
    </q-page-container>
  </q-layout>
</template>

<script setup>

const { notifyError } = useNotify();

const formWidth = '500px';
const formHeight = '500px';
const requiredRule_userName = val => (val && val.length > 0) || "Please enter a valid username!";
const requiredRule_password = val => (val && val.length > 0) || "Please enter a valid password!";

</script>

<script>
import axios from 'axios';
import useNotify from '../../src/components/useNotify.js';

export default {
  setup() {
    const { notifyError } = useNotify();

    // setup fonksiyonu bir nesne döndürmeli
    return {
      notifyError
    };
  },

  data() {
    return {
      form: { username: "", password: "" },
      showErrorMessage: false,
    };
  },

  methods: {
    createPost() {
      // Kullanıcı adı ve şifre alanlarını kontrol et
      if (!this.form.username || !this.form.password) {
        // Hata mesajını göster
        this.showErrorMessage = true;
        return; // Formu göndermeyi durdur
      }

      axios
        .post("http://127.0.0.1:5000/api/login", this.form)
        .then((response) => {
          if (response.data.status == true) {
            var url;
            if (response.data.sys_role == 1) {
              url = "http://localhost:8080/#/TeacherPage/" + response.data.session_username;
            } else if (response.data.sys_role == 0) {
              url = "http://localhost:8080/#/StudentPage/" + response.data.session_username;
            }
            window.location.href = url;
          } else {
          }
        })
        .catch((error) => {
          this.$q.notify({
            color: 'negative',
            position: 'top',
            message: 'Session could not be opened. Check your username or password.',
            icon: 'error'
          });
          this.showErrorMessage = true;
        });
    }
  }
};

</script>

