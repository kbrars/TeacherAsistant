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
                        <q-btn flat v-for="s in lesson.subjects" :key="s.id">{{ s[0] }}</q-btn>
                    </q-card-actions>
                </q-card>
            </div>
        </div>
    </q-page>
</template>

<script>
    import axios from 'axios';

    export default {
        data() {
            return {
                lessons: [],
                userInfo: {
                    username: this.$route.params.username,
                },
                subjects: []
            }
        },
        created() {
            axios.post("http://127.0.0.1:5000/api/getTeacherLessons_Subjects", this.userInfo)
                .then(response => {
                    this.lessons = response.data.s;
                    console.log(this.lessons)
                    for (let i = 0; i < this.lessons.length; i++) {
                        this.lessons[i]["image"] = `data:image/jpg;base64,${this.lessons[i]["image"]}`;
                    }
                })
                .catch(error => {
                    console.error("Veriler alınırken hata oluştu:", error);
                });
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
