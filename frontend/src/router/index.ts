import { createRouter, createWebHashHistory } from 'vue-router'
import LoadingView from '../views/LoadingView.vue'
import StudioView from '../views/StudioView.vue'

const routes = [
  {
    path: '/',
    name: 'loading',
    component: LoadingView
  },
  {
    path: '/studio',
    name: 'Studio',
    component: StudioView
  },
  // {
  //   path: '/scene2',
  //   name: 'Opening',
  //   component: Scene1View
  // }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
