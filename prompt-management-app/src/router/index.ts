import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AdvancedPromptListView from '../views/AdvancedPromptListView.vue'
import ModuleListView from '../views/ModuleListView.vue'
import TemplateView from '../views/TemplateView.vue'
import DraftView from '../views/DraftView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/prompts',
      name: 'prompts',
      component: AdvancedPromptListView
    },
    {
      path: '/modules',
      name: 'modules',
      component: ModuleListView
    },
    {
      path: '/templates',
      name: 'templates',
      component: TemplateView
    },
    {
      path: '/drafts',
      name: 'drafts',
      component: DraftView
    }
  ]
})

export default router 