<template>
    <q-page>
        <div class="row q-gutter-md wrap justify-center">
            <div class="col-12 col-sm-6 col-md-4 col-lg-3" v-for="lesson in lessons" :key="lesson.id">
                <q-card class="my-card" :style="{ height: (100 + (42 * lesson.subjects.length)) + 'px' }">
                    <q-img v-if="lesson.image" :src="lesson.image" alt="Database Image"
                        style="object-fit: cover; height: 100px;">
                        <div class="absolute-bottom text-subtitle2 text-center bg-black text-white"
                            style="opacity: 0.7; padding: 5px;">
                            {{ lesson . lesson_name }}
                        </div>
                    </q-img>
                    <q-card-actions vertical>
                        <q-btn flat v-for="s in lesson.subjects" :key="s.id"
                            @click="createMaterial(s[0],lesson.lesson_name)">{{ s[0] }}</q-btn>
                    </q-card-actions>
                    <q-dialog v-model="loading" persistent>
                        <div v-if="loading" class="text-center">
                            <div v-if="loading" class="custom-loader">
                                <q-spinner color="primary" />
                                <p style="color: aliceblue;">Materyal Oluşturuluyor...</p>
                            </div>
                        </div>
                    </q-dialog>
                </q-card>
            </div>
        </div>
    </q-page>
</template>

<script>
    import axios from 'axios';
    import jsPDF from 'jspdf';
    import Roboto from '@fontsource/roboto/files/roboto-latin-400-normal.woff2';
    export default {
        data() {
            return {
                loading: false,
                lessons: [],
                userInfo: {
                    username: this.$route.params.username,
                },
                subjects: [],
                selected_subject: {
                    "subject_name": null,
                    "lesson_name": null
                }

            }
        },
        created() {
            axios.post("http://127.0.0.1:5000/api/getTeacherLessons_Subjects", this.userInfo)
                .then(response => {
                    this.lessons = response.data.s;

                    for (let i = 0; i < this.lessons.length; i++) {
                        this.lessons[i]["image"] = `data:image/jpg;base64,${this.lessons[i]["image"]}`;
                    }
                })
                .catch(error => {
                    console.error("Veriler alınırken hata oluştu:", error);
                });
        },
        methods: {
            createMaterial(subject, lesson_name) {
                this.selected_subject.subject_name = subject
                this.selected_subject.lesson_name = lesson_name
                this.loading = true;
                axios.post("http://127.0.0.1:5000/api/createMeterial", this.selected_subject)
                    .then(response => {
                        console.log(response)
                        // Yeni bir jsPDF nesnesi oluştur
                        const doc = new jsPDF();
                        // Türkçe karakterleri destekleyen fontu ayarlayın
                        doc.addFileToVFS("Roboto.ttf", Roboto); // Fontu ekle
                        doc.addFont("Roboto.ttf", "Roboto", "normal"); // Fontu kaydet
                        doc.setFont("Roboto"); // Fontu kullan
                        doc.setFontSize(10);

                        // PDF'ye metin ekle
                        doc.text(response.data.material, 5, 5);
                        // PDF'yi indirme
                        doc.save('quasar-pdf-example.pdf');

                    })

                    .catch(error => {
                        console.error("Veriler alınırken hata oluştu:", error);
                    })
                    .finally(() => {
                        this.loading = false;
                    });
            }
        }
    }
</script>

<style>
    .my-card {
        max-width: 100%;
        /* Allow cards to fill available width */
        margin: auto;
        /* Center cards */
    }

    .custom-modal {
        width: 80%;
        max-width: 600px;
    }
</style>
