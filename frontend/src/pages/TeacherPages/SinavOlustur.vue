<template>
    <q-page>
        <!-- Dersler -->
        <div class="row q-gutter-md wrap justify-center">
            <div class="col-12 col-sm-6 col-md-4 col-lg-3" v-for="lesson in lessons" :key="lesson.id">
                <q-card class="my-card" style="width: 400px; max-width: 100%; margin: 0 auto;" @click="openModal(lesson)">
                    <q-img v-if="lesson.image" :src="lesson.image" alt="Database Image"
                        style="object-fit: cover; height: 150px;">
                        <div class="absolute-bottom text-subtitle2 text-center bg-black text-white"
                            style="opacity: 0.7; padding: 5px;">
                            {{ lesson . lesson_name }}
                        </div>
                    </q-img>
                </q-card>
            </div>
        </div>

        <!-- Seçilen Derse ait Modal -->
        <q-dialog v-model="dialog" @hide="resetLesson">
            <q-card class="custom-modal">
                <q-card-section>
                    <div class="text-h6">{{ selectedLesson . lesson_name }}</div>
                    <q-img v-if="selectedLesson.image" :src="selectedLesson.image" alt="Modal Image"
                        style=" height: 100px; width: 100%;" />
                    <div class="q-pa-md">
                        <div class="q-gutter-sm" v-for="s in subjects" :key="s.id">
                            <q-list>
                                <q-item tag="label" v-ripple>
                                    <q-item-section avatar>
                                        <q-checkbox v-model="subjectt" :val="s[0]" color="teal" />
                                    </q-item-section>
                                    <q-item-section>
                                        <q-item-label>{{ s[0] }}</q-item-label>
                                    </q-item-section>
                                </q-item>
                            </q-list>
                        </div>
                        <div class="q-pa-md">
                            <p>Soru Sayısı: </p>
                            <q-input v-model.number="total_questions" type="number" filled style="max-width: 100%" />
                        </div>
                    </div>
                </q-card-section>
                <q-card-actions>
                    <q-btn label="Sınav Oluştur" :loading="loading" @click="sinav_olustur" color="secondary"
                        class="full-width" style="height: 40px;" />
                </q-card-actions>
            </q-card>
        </q-dialog>
    </q-page>
</template>

<script>
    import axios from 'axios'
    import {
        ref
    } from 'vue'
    import jsPDF from 'jspdf';
    import Roboto from '@fontsource/roboto/files/roboto-latin-400-normal.woff2';
    export default {
        setup() {
            return {
                subjectt: ref([]),
            }
        },
        data() {
            return {
                total_questions: null,
                userInfo: {
                    username: this.$route.params.username,
                },
                lessons: [], // API'den gelen ders verileri burada tutulacak
                dialog: false, // Modalın açık olup olmadığını kontrol eden değişken
                selectedLesson: {}, // Seçilen dersin bilgileri
                subjects: [], //Derse ait konular
                subject_info: {
                    username: null,
                    lesson_id: null,
                    selected_subjects: null,
                    total_questions: null,
                },
                loading: false,
                text: ''
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
                axios.post('http://127.0.0.1:5000/api/getSubjects', this.selectedLesson)
                    .then(response => {
                        // Gelen veriyi modalda göstermek için ayarlayın
                        this.subjects = response.data;
                        console.log("Deneme" + this.subject)
                    })
                    .catch(error => {
                        console.error("Ders detayları alınırken hata oluştu:", error);
                    });
                this.dialog = true;

            },
            resetLesson() {
                // Modal kapatıldığında seçilen dersi sıfırlayın
                this.selectedLesson = {};
                this.subject = []; // Checkbox seçimlerini sıfırlar
            },
            async sinav_olustur() {
                this.loading = true;
                this.subject_info = {
                    username: this.userInfo.username,
                    lesson_id: this.selectedLesson.id,
                    selected_subjects: this.subjectt,
                    total_questions: this.total_questions,
                };

                try {
                    axios.post('http://127.0.0.1:5000/api/createQuestions', this.subject_info)
                        .then(response => {

                            // Yeni bir jsPDF nesnesi oluştur
                            const doc = new jsPDF();
                            // Türkçe karakterleri destekleyen fontu ayarlayın
                            doc.addFileToVFS("Roboto.ttf", Roboto); // Fontu ekle
                            doc.addFont("Roboto.ttf", "Roboto", "normal"); // Fontu kaydet
                            doc.setFont("Roboto"); // Fontu kullan
                            doc.setFontSize(10);

                            // PDF'ye metin ekle
                            doc.text(response.data.questions, 5, 5);
                            // PDF'yi indirme
                            doc.save('quasar-pdf-example.pdf');

                        })
                        .catch(error => {
                            console.error("Veriler alınırken hata oluştu:", error);
                        });
                    await new Promise(resolve => setTimeout(resolve, 2000));
                } finally {
                    this.loading = false; // İşlem tamamlandığında yüklenme durumunu kapat
                }

            }
        }
    }
</script>

<style>
    .my-card {
        width: 400px;
        max-width: 100%;
        height: 200px;
    }

    .custom-modal {
        width: 80%;
        max-width: 600px;
    }
</style>
