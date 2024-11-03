import IndexPage from "pages/IndexPage.vue"
import TeacherLayout from "layouts/TeacherLayout.vue"
import TeacherProfilPage from "src/pages/TeacherPages/TeacherProfil.vue"
import SinavOlusturPage from "src/pages/TeacherPages/SinavOlustur.vue"
import StudentProfilPage from "src/pages/StudentPages/StudentProfil.vue"
import MateryalOlusturPage from "src/pages/TeacherPages/MateryalOlustur.vue"

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
      { path: 'MateryalOlusturma', component: MateryalOlusturPage, name:"MateryalOlusturPage"}
    ]
  },

    // Student Pages
    {
      path: '/StudentPage/:username',
      component: TeacherLayout,
      children: [
        { path: '', component: StudentProfilPage, name:"StudentProfilPage"},
      ]
    },


  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes
