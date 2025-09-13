import { createRouter, createWebHashHistory } from 'vue-router'
import Chat from '@/components/Chat.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Chat
  },
  // Add more routes here later
]

const router = createRouter({
  history: createWebHashHistory(), // <--- hash-based routing
  routes
})

export default router
