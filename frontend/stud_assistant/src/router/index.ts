import { createRouter, createWebHistory } from 'vue-router'
import Chat from '@/components/Chat.vue'
import Login from '@/components/Login.vue'
import Signup from '@/components/Signup.vue'
import Payment from '@/components/Payment.vue'


const routes = [
  { path: '/', name: 'Home', component: Chat },
  { path: '/chat/:id', name: 'Chat', component: Chat, props: true },
  { path: '/login', name: 'Login', component: Login },
  { path: '/signup', name: 'Signup', component: Signup },
  { path: '/subscription', name: 'Subscription', component: Payment },
]


export default createRouter({
  history: createWebHistory('/stud_assistant/'),  
  routes,
})


