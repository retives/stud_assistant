import { createRouter, createWebHashHistory } from 'vue-router'
import Chat from '@/components/Chat.vue'
import Login from '@/components/Login.vue'
import Signup from '@/components/Signup.vue'

const routes = [
  {path: '/', name: 'Home', component: Chat },
  { path: "/login", name: "Login", component: Login },
  { path: "/signup", name: "Signup", component: Signup },
]

const router = createRouter({
  history: createWebHashHistory('/stud-assistant'),
  routes
})

export default router
