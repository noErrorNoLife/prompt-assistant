<template>
  <div class="group relative bg-gradient-to-br from-white to-gray-50 rounded-xl shadow-sm border border-gray-200 hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2 overflow-hidden">
    <!-- 模板特殊标识 -->
    <div class="absolute top-0 right-0 z-10">
      <div class="bg-gradient-to-r from-yellow-400 to-orange-500 text-white text-xs px-3 py-1 rounded-bl-lg font-bold">
        <svg class="inline w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
          <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
        </svg>
        模板
      </div>
    </div>

    <!-- 评分显示 -->
    <div v-if="template.rating && template.rating > 0" class="absolute top-3 left-3 z-10">
      <div class="flex items-center bg-white/90 backdrop-blur-sm rounded-full px-2 py-1">
        <svg class="h-4 w-4 text-yellow-400 mr-1" fill="currentColor" viewBox="0 0 20 20">
          <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
        </svg>
        <span class="text-sm font-medium text-gray-700">{{ template.rating.toFixed(1) }}</span>
      </div>
    </div>

    <!-- 主要内容 -->
    <div class="p-6">
      <!-- 模板头部信息 -->
      <div class="mb-4">
        <h3 class="text-xl font-bold text-gray-900 mb-2 group-hover:text-blue-600 transition-colors duration-200 line-clamp-2">
          {{ template.title }}
        </h3>
        
        <!-- 使用统计 -->
        <div class="flex items-center space-x-4 text-sm text-gray-500 mb-3">
          <div class="flex items-center">
            <svg class="h-4 w-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
            <span>{{ template.usage_count || 0 }} 次使用</span>
          </div>
          <div class="flex items-center">
            <svg class="h-4 w-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span>{{ formatDate(template.created_at) }}</span>
          </div>
        </div>

        <!-- 模板描述 -->
        <p class="text-gray-600 text-sm line-clamp-3 leading-relaxed mb-4">
          {{ truncatedContent }}
        </p>
      </div>

      <!-- 模板变量预览 -->
      <div v-if="templateVariables.length" class="mb-4">
        <div class="flex items-center mb-2">
          <svg class="h-4 w-4 text-blue-500 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
          </svg>
          <span class="text-sm font-medium text-gray-700">可自定义变量 ({{ templateVariables.length }})</span>
        </div>
        <div class="flex flex-wrap gap-1">
          <span
            v-for="variable in templateVariables.slice(0, 3)"
            :key="variable.name"
            class="inline-flex items-center px-2 py-1 rounded-md text-xs font-medium bg-blue-100 text-blue-800"
          >
            {{ variable.name }}
          </span>
          <span
            v-if="templateVariables.length > 3"
            class="inline-flex items-center px-2 py-1 rounded-md text-xs font-medium bg-gray-100 text-gray-600"
          >
            +{{ templateVariables.length - 3 }} 个
          </span>
        </div>
      </div>

      <!-- 标签 -->
      <div v-if="tags.length" class="mb-4">
        <div class="flex flex-wrap gap-1">
          <span
            v-for="tag in tags.slice(0, 3)"
            :key="tag"
            class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-700 hover:bg-gray-200 transition-colors duration-200"
          >
            {{ tag }}
          </span>
          <span
            v-if="tags.length > 3"
            class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-500"
          >
            +{{ tags.length - 3 }}
          </span>
        </div>
      </div>

      <!-- 分类信息 -->
      <div v-if="template.category" class="mb-4">
        <div class="flex items-center">
          <svg class="h-4 w-4 text-purple-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
          </svg>
          <span class="text-sm text-gray-600">{{ template.category }}</span>
        </div>
      </div>

      <!-- 作者信息 -->
      <div v-if="template.author" class="mb-6">
        <div class="flex items-center">
          <div class="h-8 w-8 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center text-white text-sm font-bold mr-3">
            {{ template.author.charAt(0).toUpperCase() }}
          </div>
          <div>
            <p class="text-sm font-medium text-gray-900">{{ template.author }}</p>
            <p class="text-xs text-gray-500">模板作者</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 操作按钮区域 -->
    <div class="px-6 pb-6">
      <div class="flex space-x-2">
        <!-- 使用模板按钮 -->
        <button
          @click="$emit('clone', template)"
          class="flex-1 inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-lg text-white bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-all duration-200 transform hover:scale-105"
        >
          <svg class="h-4 w-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
          使用模板
        </button>

        <!-- 预览按钮 -->
        <button
          @click="showPreview"
          class="inline-flex items-center px-3 py-2 border border-gray-300 text-sm font-medium rounded-lg text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-all duration-200"
        >
          <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
          </svg>
        </button>

        <!-- 更多操作下拉菜单 -->
        <div class="relative">
          <button
            @click="showDropdown = !showDropdown"
            class="inline-flex items-center p-2 border border-gray-300 rounded-lg text-gray-400 hover:text-gray-600 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-all duration-200"
          >
            <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
              <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z" />
            </svg>
          </button>

          <!-- 下拉菜单 -->
          <transition
            enter-active-class="transition ease-out duration-100"
            enter-from-class="transform opacity-0 scale-95"
            enter-to-class="transform opacity-100 scale-100"
            leave-active-class="transition ease-in duration-75"
            leave-from-class="transform opacity-100 scale-100"
            leave-to-class="transform opacity-0 scale-95"
          >
            <div v-if="showDropdown" class="absolute right-0 z-30 mt-2 w-48 bg-white rounded-lg shadow-lg ring-1 ring-black ring-opacity-5 divide-y divide-gray-100">
              <div class="py-1">
                <button
                  @click.stop="$emit('edit', template)"
                  class="group flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 w-full text-left"
                >
                  <svg class="mr-3 h-4 w-4 text-gray-400 group-hover:text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                  </svg>
                  编辑模板
                </button>
                <button
                  @click.stop="copyTemplate"
                  class="group flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 w-full text-left"
                >
                  <svg class="mr-3 h-4 w-4 text-gray-400 group-hover:text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                  </svg>
                  复制模板
                </button>
                <button
                  @click.stop="shareTemplate"
                  class="group flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 w-full text-left"
                >
                  <svg class="mr-3 h-4 w-4 text-gray-400 group-hover:text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.367 2.684 3 3 0 00-5.367-2.684z" />
                  </svg>
                  分享模板
                </button>
              </div>
              <div class="py-1">
                <button
                  @click.stop="$emit('delete', template)"
                  class="group flex items-center px-4 py-2 text-sm text-red-700 hover:bg-red-50 w-full text-left"
                >
                  <svg class="mr-3 h-4 w-4 text-red-400 group-hover:text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                  删除模板
                </button>
              </div>
            </div>
          </transition>
        </div>
      </div>
    </div>

    <!-- 预览模态框 -->
    <transition
      enter-active-class="transition ease-out duration-300"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition ease-in duration-200"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div v-if="showPreviewModal" class="fixed inset-0 z-50 overflow-y-auto" @click.self="showPreviewModal = false">
        <div class="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
          <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"></div>
          
          <div class="inline-block align-bottom bg-white rounded-lg px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full sm:p-6">
            <div class="sm:flex sm:items-start">
              <div class="w-full">
                <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">
                  模板预览
                </h3>
                <div class="mt-2">
                  <div class="bg-gray-50 rounded-lg p-4">
                    <pre class="whitespace-pre-wrap text-sm text-gray-700">{{ template.content }}</pre>
                  </div>
                </div>
              </div>
            </div>
            <div class="mt-5 sm:mt-6">
              <button
                @click="showPreviewModal = false"
                class="inline-flex justify-center w-full rounded-md border border-transparent shadow-sm px-4 py-2 bg-blue-600 text-base font-medium text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:text-sm"
              >
                关闭
              </button>
            </div>
          </div>
        </div>
      </div>
    </transition>

    <!-- 加载状态 -->
    <div v-if="isLoading" class="absolute inset-0 bg-white bg-opacity-75 flex items-center justify-center rounded-xl">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import type { Prompt, TemplateVariable } from '@/services/api'

interface Props {
  template: Prompt
  maxContentLength?: number
}

const props = withDefaults(defineProps<Props>(), {
  maxContentLength: 120
})

const emit = defineEmits<{
  clone: [template: Prompt]
  edit: [template: Prompt]
  delete: [template: Prompt]
}>()

const showDropdown = ref(false)
const showPreviewModal = ref(false)
const isLoading = ref(false)

// 计算属性
const tags = computed(() => {
  if (!props.template.tags) return []
  return props.template.tags.split(',').map(tag => tag.trim()).filter(Boolean)
})

const templateVariables = computed((): TemplateVariable[] => {
  if (!props.template.template_variables) return []
  return Array.isArray(props.template.template_variables) 
    ? props.template.template_variables 
    : []
})

const truncatedContent = computed(() => {
  if (props.template.content.length <= props.maxContentLength) {
    return props.template.content
  }
  return props.template.content.substring(0, props.maxContentLength) + '...'
})

// 方法
const showPreview = () => {
  showPreviewModal.value = true
  showDropdown.value = false
}

const copyTemplate = async () => {
  try {
    await navigator.clipboard.writeText(props.template.content)
    showSuccessMessage('模板内容已复制到剪贴板')
  } catch (error) {
    console.error('复制失败:', error)
    // 降级方案
    const textArea = document.createElement('textarea')
    textArea.value = props.template.content
    document.body.appendChild(textArea)
    textArea.select()
    document.execCommand('copy')
    document.body.removeChild(textArea)
    showSuccessMessage('模板内容已复制到剪贴板')
  }
  showDropdown.value = false
}

const shareTemplate = async () => {
  const shareData = {
    title: `模板: ${props.template.title}`,
    text: props.template.content,
    url: window.location.href
  }

  if (navigator.share) {
    try {
      await navigator.share(shareData)
    } catch (error) {
      // 用户取消分享或不支持
      copyShareLink()
    }
  } else {
    copyShareLink()
  }
  showDropdown.value = false
}

const copyShareLink = async () => {
  const shareUrl = `${window.location.origin}/templates/${props.template.id}`
  try {
    await navigator.clipboard.writeText(shareUrl)
    showSuccessMessage('分享链接已复制到剪贴板')
  } catch (error) {
    console.error('复制分享链接失败:', error)
  }
}

const formatDate = (dateString?: string) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))
  
  if (days === 0) return '今天'
  if (days === 1) return '昨天'
  if (days < 7) return `${days} 天前`
  if (days < 30) return `${Math.floor(days / 7)} 周前`
  if (days < 365) return `${Math.floor(days / 30)} 月前`
  return `${Math.floor(days / 365)} 年前`
}

const showSuccessMessage = (message: string) => {
  // 这里可以集成全局消息提示组件
  console.log(message)
}

// 点击外部关闭下拉菜单
const handleClickOutside = (event: Event) => {
  const target = event.target as HTMLElement
  if (!target.closest('.relative')) {
    showDropdown.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* 悬浮动画效果 */
@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-4px); }
}

.group:hover {
  animation: float 0.6s ease-in-out;
}

/* 渐变边框效果 */
.group::before {
  content: '';
  position: absolute;
  inset: 0;
  padding: 2px;
  background: linear-gradient(45deg, #3B82F6, #8B5CF6, #F59E0B);
  border-radius: inherit;
  mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  mask-composite: exclude;
  opacity: 0;
  transition: opacity 0.3s;
}

.group:hover::before {
  opacity: 1;
}
</style>