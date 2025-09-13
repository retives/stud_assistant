import { createRouter, createWebHashHistory } from 'vue-router'
import SimpleChat from '@/components/SimpleChat.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: SimpleChat
  },
  // Add more routes here later
]

const router = createRouter({
  history: createWebHashHistory(), // <--- hash-based routing
  routes
})

export default router
