import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/components/Home.vue'
import Chat from '@/components/Chat.vue'
import Login from '@/components/Login.vue'
import Signup from '@/components/Signup.vue'
import Payment from '@/components/Payment.vue'
import SuccessPage from '../components/SuccessPage.vue'
import CancelPage from '../components/CancelPage.vue'
import NotFound from '../components/NotFound.vue'

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/chat/:id', name: 'Chat', component: Chat, props: true },
  { path: '/login', name: 'Login', component: Login },
  { path: '/signup', name: 'Signup', component: Signup },
  { path: '/subscription', name: 'Subscription', component: Payment },
  {path: '/payments/success', name: 'SubscriptionSuccess', component: SuccessPage},
  {path: '/payments/cancel', name: 'SubscriptionCancel', component: CancelPage},
  {path: '/:catchAll(.*)*', component: NotFound}
]


export default createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})


