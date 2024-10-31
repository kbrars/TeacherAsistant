<template>
  <div class="q-pa-md">
    <q-layout view="hHh Lpr lff" class="shadow-2 rounded-borders">
      <!-- Header -->
      <q-header elevated :class="$q.dark.isActive ? 'bg-secondary' : 'bg-black'">
        <q-toolbar>
          <q-btn flat @click="toggleDrawer" round dense icon="menu" />
          <q-toolbar-title>Teacher Portal</q-toolbar-title>
        </q-toolbar>
      </q-header>

      <!-- Drawer -->
      <q-drawer
        v-model="drawer"
        show-if-above
        :mini="miniState"
        @mouseover="miniState = false"
        @mouseout="miniState = true"
        :width="200"
        :breakpoint="500"
        bordered
        :class="$q.dark.isActive ? 'bg-grey-9' : 'bg-grey-3'"
      >
        <q-scroll-area class="fit" :horizontal-thumb-style="{ opacity: 0 }">
          <q-list padding>
            <!-- Profil -->
            <q-item clickable v-ripple @click="selectPage('TeacherProfilPage')">
              <q-item-section avatar>
                <q-icon name="account_box" />
              </q-item-section>
              <q-item-section>
                Profil
              </q-item-section>
            </q-item>

            <!-- Sinav Olustur -->
            <q-item clickable v-ripple @click="selectPage('SinavOlusturPage')">
              <q-item-section avatar>
                <q-icon name="description" style="position: relative; font-size: 26px; color: black;">
                <q-icon name="add" style="position: absolute; right: -9px; bottom: -6px; color: black; font-size: 16px;" />
              </q-icon>

              </q-item-section>
              <q-item-section>
                Sınav Oluştur
              </q-item-section>
            </q-item>

            <!-- Çıkış Yap -->
            <q-separator />
            <q-item clickable v-ripple @click="logout">
              <q-item-section avatar>
                <q-icon name="exit_to_app" />
              </q-item-section>
              <q-item-section>
                Çıkış Yap
              </q-item-section>
            </q-item>
          </q-list>
        </q-scroll-area>
      </q-drawer>

      <!-- Page Content -->
      <q-page-container>
        <q-page padding>
          <!-- İçerikler -->

          <div v-if="selectedPage === 'TeacherProfilPage'   ">
            <router-view></router-view>
            <!-- Profil içeriği -->
          </div>

          <div v-else-if="selectedPage === 'SinavOlusturPage'">
          <!-- Sinav Olusturma -->
            <router-view></router-view>
          </div>

        </q-page>
      </q-page-container>
    </q-layout>
  </div>
</template>


<script>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios'

export default {
setup() {
  const drawer = ref(false);
  const miniState = ref(true);
  const router = useRouter();
  const selectedPage = ref('TeacherProfilPage');

  const selectPage = (page) => {
    selectedPage.value = page;
    if (page === 'TeacherProfilPage') {
      router.push({ name: 'TeacherProfilPage' });
    } else if (page === 'SinavOlusturPage') {
      router.push({ name: 'SinavOlusturPage' });
    }
  };

  const toggleDrawer = () => {
    drawer.value = !drawer.value;
  };

  const logout = () => {
    axios.post('http://127.0.0.1:5000/api/logout')
      .then((response) => {
        window.location.href = '/';

      })
      .catch((error) => {
        console.error('Çıkış yapma hatası:', error);
      });
    };


  return {
    drawer,
    miniState,
    selectedPage,
    selectPage,
    toggleDrawer,
    logout
  };
}
};

</script>

