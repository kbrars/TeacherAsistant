import IndexPage from "pages/IndexPage.vue"
import TeacherLayout from "layouts/TeacherLayout.vue"
import StudentLayout from "layouts/StudentLayout.vue"
import TeacherProfilPage from "src/pages/TeacherPages/TeacherProfil.vue"
import SinavOlusturPage from "src/pages/TeacherPages/SinavOlustur.vue"
import StudentFeedback from "src/pages/StudentPages/StudentFeedback.vue"
import MateryalOlusturPage from "src/pages/TeacherPages/MateryalOlustur.vue"
import TeacherFeedbacks from "src/pages/TeacherPages/TeacherFeedbacks.vue"

const routes = [
  // Login Page
  {
    path: '/',
    component: IndexPage,
    name:"LoginPage"
  },
  // Teacher Portal
  {
    path: '/TeacherPage/:username',
    component: TeacherLayout,
    children: [
      { path: '', component: TeacherProfilPage, name:"TeacherProfilPage"},
      { path: 'SinavOlusturma', component: SinavOlusturPage, name:"SinavOlusturPage"},
      { path: 'MateryalOlusturma', component: MateryalOlusturPage, name:"MateryalOlusturPage"},
      { path: 'Feedbacks', component: TeacherFeedbacks, name:"TeacherFeedbacks"}
    ]
  },
      // Student Pages
      {
        path: '/StudentPage/:username',
        component: StudentLayout,
        children: [
          { path: '', component: StudentFeedback, name:"StudentFeedback"},
        ]
      },



  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes
