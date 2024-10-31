import IndexPage from "pages/IndexPage.vue"
import TeacherLayout from "layouts/TeacherLayout.vue"
import TeacherProfilPage from "src/pages/TeacherPages/TeacherProfil.vue"
import StudentProfilPage from "src/pages/StudentPages/StudentProfil.vue"


const routes = [
  // Login Page
  {
    path: '/',
    component: IndexPage
  },
  // Teacher Portal
  {
    path: '/TeacherPage/:username',
    component: TeacherLayout,
    children: [
      { path: '', component: TeacherProfilPage, name:"TeacherProfilPage"}
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
