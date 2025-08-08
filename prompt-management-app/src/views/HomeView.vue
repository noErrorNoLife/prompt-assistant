<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
    <!-- 顶部横幅 -->
    <div class="relative overflow-hidden">
      <div class="absolute inset-0 bg-gradient-to-r from-blue-600 to-purple-600 opacity-10"></div>
      <div class="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div class="text-center">
          <!-- 主标题 -->
          <div class="flex justify-center mb-8">
            <div class="flex items-center space-x-3">
              <div class="h-12 w-12 bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl flex items-center justify-center">
                <svg class="h-8 w-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <h1 class="text-5xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                Prompt Assistant
              </h1>
            </div>
          </div>
          
          <p class="text-xl text-gray-600 mb-8 max-w-3xl mx-auto leading-relaxed">
            智能提示词管理平台，支持版本控制、模板复用、模块化管理，让您的AI工作流更加高效
          </p>

          <!-- 快速操作按钮 -->
          <div class="flex flex-wrap justify-center gap-4 mb-12">
            <router-link
              to="/prompts"
              class="group inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-xl text-white bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 transform hover:scale-105 transition-all duration-200 shadow-lg"
            >
              <svg class="mr-2 h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              管理提示词
            </router-link>
            
            <router-link
              to="/templates"
              class="group inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-xl text-white bg-gradient-to-r from-purple-600 to-purple-700 hover:from-purple-700 hover:to-purple-800 transform hover:scale-105 transition-all duration-200 shadow-lg"
            >
              <svg class="mr-2 h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
              </svg>
              模板市场
            </router-link>
            
            <router-link
              to="/modules"
              class="group inline-flex items-center px-6 py-3 border border-gray-300 text-base font-medium rounded-xl text-gray-700 bg-white hover:bg-gray-50 transform hover:scale-105 transition-all duration-200 shadow-lg"
            >
              <svg class="mr-2 h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
              </svg>
              模块管理
            </router-link>
          </div>
        </div>
      </div>
    </div>

    <!-- 统计信息面板 -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 -mt-8">
      <div v-if="stats" class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
        <div class="bg-white overflow-hidden shadow-lg rounded-xl border border-gray-100 hover:shadow-xl transition-shadow duration-300">
          <div class="p-6">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div class="w-10 h-10 bg-gradient-to-r from-blue-500 to-blue-600 rounded-lg flex items-center justify-center">
                  <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                </div>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">提示词总数</dt>
                  <dd class="flex items-baseline">
                    <div class="text-2xl font-bold text-gray-900">{{ stats.total_prompts }}</div>
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-white overflow-hidden shadow-lg rounded-xl border border-gray-100 hover:shadow-xl transition-shadow duration-300">
          <div class="p-6">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div class="w-10 h-10 bg-gradient-to-r from-purple-500 to-purple-600 rounded-lg flex items-center justify-center">
                  <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                  </svg>
                </div>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">模板数量</dt>
                  <dd class="flex items-baseline">
                    <div class="text-2xl font-bold text-gray-900">{{ stats.total_templates }}</div>
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-white overflow-hidden shadow-lg rounded-xl border border-gray-100 hover:shadow-xl transition-shadow duration-300">
          <div class="p-6">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div class="w-10 h-10 bg-gradient-to-r from-green-500 to-green-600 rounded-lg flex items-center justify-center">
                  <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                  </svg>
                </div>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">模块数量</dt>
                  <dd class="flex items-baseline">
                    <div class="text-2xl font-bold text-gray-900">{{ stats.total_modules }}</div>
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-white overflow-hidden shadow-lg rounded-xl border border-gray-100 hover:shadow-xl transition-shadow duration-300">
          <div class="p-6">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div class="w-10 h-10 bg-gradient-to-r from-red-500 to-red-600 rounded-lg flex items-center justify-center">
                  <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.682l-1.318-1.364a4.5 4.5 0 00-6.364 0z" />
                  </svg>
                </div>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">收藏数量</dt>
                  <dd class="flex items-baseline">
                    <div class="text-2xl font-bold text-gray-900">{{ stats.total_favorites }}</div>
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 主要功能区域 -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-12">
        <!-- 最近提示词 -->
        <div class="bg-white rounded-xl shadow-lg border border-gray-100 overflow-hidden">
          <div class="p-6 border-b border-gray-100">
            <h2 class="text-xl font-bold text-gray-900 flex items-center">
              <svg class="h-6 w-6 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              最近创建
            </h2>
          </div>
          <div class="divide-y divide-gray-100">
            <div v-if="!stats?.recent_prompts?.length" class="p-6 text-center text-gray-500">
              <svg class="mx-auto h-12 w-12 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              暂无提示词，快去创建第一个吧！
            </div>
            <div
              v-for="prompt in stats?.recent_prompts"
              :key="prompt.id"
              class="p-4 hover:bg-gray-50 transition-colors duration-200 cursor-pointer"
              @click="navigateToPrompts"
            >
              <div class="flex items-center justify-between">
                <div class="flex-1 min-w-0">
                  <p class="text-sm font-medium text-gray-900 truncate">
                    {{ prompt.title }}
                  </p>
                  <p class="text-sm text-gray-500">
                    {{ formatDate(prompt.created_at) }}
                  </p>
                </div>
                <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                </svg>
              </div>
            </div>
          </div>
        </div>

        <!-- 分类统计 -->
        <div class="bg-white rounded-xl shadow-lg border border-gray-100 overflow-hidden">
          <div class="p-6 border-b border-gray-100">
            <h2 class="text-xl font-bold text-gray-900 flex items-center">
              <svg class="h-6 w-6 mr-2 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
              </svg>
              分类统计
            </h2>
          </div>
          <div class="p-6">
            <div v-if="!stats?.categories?.length" class="text-center text-gray-500">
              <svg class="mx-auto h-12 w-12 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
              </svg>
              暂无分类数据
            </div>
            <div v-else class="space-y-4">
              <div
                v-for="category in stats.categories.slice(0, 5)"
                :key="category.category"
                class="flex items-center justify-between"
              >
                <div class="flex items-center">
                  <div class="w-3 h-3 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full mr-3"></div>
                  <span class="text-sm font-medium text-gray-900">{{ category.category }}</span>
                </div>
                <span class="text-sm text-gray-500">{{ category.count }} 个</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 功能特色 -->
    <div class="bg-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div class="text-center mb-16">
          <h2 class="text-3xl font-bold text-gray-900 mb-4">强大功能</h2>
          <p class="text-lg text-gray-600">全方位提升您的AI工作流效率</p>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div class="text-center p-6 rounded-xl hover:bg-gray-50 transition-colors duration-200">
            <div class="w-16 h-16 bg-gradient-to-r from-blue-500 to-blue-600 rounded-xl mx-auto mb-4 flex items-center justify-center">
              <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-gray-900 mb-2">版本控制</h3>
            <p class="text-gray-600">跟踪每个提示词的修改历史，轻松回滚到任意版本</p>
          </div>

          <div class="text-center p-6 rounded-xl hover:bg-gray-50 transition-colors duration-200">
            <div class="w-16 h-16 bg-gradient-to-r from-purple-500 to-purple-600 rounded-xl mx-auto mb-4 flex items-center justify-center">
              <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-gray-900 mb-2">模板系统</h3>
            <p class="text-gray-600">创建可复用的模板，支持变量替换，提高工作效率</p>
          </div>

          <div class="text-center p-6 rounded-xl hover:bg-gray-50 transition-colors duration-200">
            <div class="w-16 h-16 bg-gradient-to-r from-green-500 to-green-600 rounded-xl mx-auto mb-4 flex items-center justify-center">
              <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-gray-900 mb-2">模块化管理</h3>
            <p class="text-gray-600">将相关提示词组织成模块，便于团队协作和共享</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useMainStore } from '@/stores'
import type { Stats } from '@/services/api'

const router = useRouter()
const store = useMainStore()

const stats = ref<Stats | null>(null)
const loading = ref(false)

const navigateToPrompts = () => {
  router.push('/prompts')
}

const formatDate = (dateString: string) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))
  
  if (days === 0) return '今天'
  if (days === 1) return '昨天'
  if (days < 7) return `${days} 天前`
  return date.toLocaleDateString('zh-CN')
}

onMounted(async () => {
  try {
    loading.value = true
    await store.fetchStats()
    stats.value = store.stats
  } catch (error) {
    console.error('获取统计信息失败:', error)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
/* 渐变动画 */
@keyframes gradient {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

.bg-gradient-to-br {
  background-size: 400% 400%;
  animation: gradient 15s ease infinite;
}

/* 悬浮效果 */
.hover\:shadow-xl:hover {
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

/* 按钮悬浮效果 */
.transform.hover\:scale-105:hover {
  transform: scale(1.05);
}
</style>