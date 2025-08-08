<template>
  <div
    class="group relative bg-white rounded-xl shadow-sm border border-gray-200 hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1"
    :class="[
      { 'ring-2 ring-blue-500': isSelected },
      { 'border-yellow-300 bg-yellow-50': prompt.is_template },
      { 'z-20': showDropdown }
    ]"
    @click="handleCardClick"
  >
    <!-- 模板标识 -->
    <div v-if="prompt.is_template" class="absolute top-0 right-0 z-10">
      <div class="bg-yellow-500 text-white text-xs px-2 py-1 rounded-bl-md font-medium">
        模板
      </div>
    </div>

    <!-- 版本标识 -->
    <div v-if="prompt.version && prompt.version > 1" class="absolute top-0 left-0 z-10">
      <div class="bg-blue-500 text-white text-xs px-2 py-1 rounded-br-md font-medium">
        v{{ prompt.version }}
      </div>
    </div>

    <!-- 收藏按钮 -->
    <button
      @click.stop="toggleFavorite"
      class="absolute top-3 right-3 z-20 p-2 rounded-full bg-white/80 backdrop-blur-sm opacity-0 group-hover:opacity-100 transition-all duration-200 hover:bg-white hover:scale-110"
      :class="{ 'opacity-100 text-red-500': isFavorite }"
    >
      <svg class="h-5 w-5" :fill="isFavorite ? 'currentColor' : 'none'" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.682l-1.318-1.364a4.5 4.5 0 00-6.364 0z" />
      </svg>
    </button>

    <!-- 主要内容 -->
    <div class="p-6 cursor-pointer">
      <!-- 标题和评分 -->
      <div class="flex items-start justify-between mb-3">
        <h3 class="text-lg font-semibold text-gray-900 line-clamp-2 group-hover:text-blue-600 transition-colors duration-200">
          {{ prompt.title }}
        </h3>
        <div v-if="prompt.rating && prompt.rating > 0" class="flex items-center ml-2 shrink-0">
          <svg class="h-4 w-4 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
          </svg>
          <span class="text-sm text-gray-600 ml-1">{{ prompt.rating.toFixed(1) }}</span>
        </div>
      </div>

      <!-- 内容预览 -->
      <div class="mb-4">
        <p class="text-gray-600 text-sm line-clamp-3 leading-relaxed">
          {{ truncatedContent }}
        </p>
        <button
          v-if="prompt.content.length > maxContentLength"
          @click.stop="toggleExpanded"
          class="text-blue-600 hover:text-blue-700 text-sm font-medium mt-1 transition-colors duration-200"
        >
          {{ isExpanded ? '收起' : '展开' }}
        </button>
      </div>

      <!-- 标签 -->
      <div v-if="tags.length" class="mb-4">
        <div class="flex flex-wrap gap-1">
          <span
            v-for="tag in tags.slice(0, 3)"
            :key="tag"
            class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-800 hover:bg-gray-200 transition-colors duration-200"
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

      <!-- 分类和使用统计 -->
      <div class="flex items-center justify-between text-sm text-gray-500 mb-4">
        <div class="flex items-center space-x-4">
          <span v-if="prompt.category" class="flex items-center">
            <svg class="h-4 w-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
            </svg>
            {{ prompt.category }}
          </span>
          <span v-if="prompt.usage_count" class="flex items-center">
            <svg class="h-4 w-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
            {{ prompt.usage_count }} 次使用
          </span>
        </div>
        <div class="text-xs">
          {{ formatDate(prompt.created_at) }}
        </div>
      </div>

      <!-- 作者信息 -->
      <div v-if="prompt.author" class="flex items-center mb-4">
        <div class="h-6 w-6 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center text-white text-xs font-bold mr-2">
          {{ prompt.author.charAt(0).toUpperCase() }}
        </div>
        <span class="text-sm text-gray-600">{{ prompt.author }}</span>
      </div>
    </div>

    <!-- 操作按钮 -->
    <div class="px-6 pb-6">
      <div class="flex items-center justify-between">
        <div class="flex space-x-2">
          <!-- 编辑按钮 -->
          <button
            @click.stop="$emit('edit', prompt)"
            class="inline-flex items-center px-3 py-1.5 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-all duration-200"
          >
            <svg class="h-4 w-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
            </svg>
            编辑
          </button>

          <!-- 复制按钮 -->
          <button
            @click.stop="copyContent"
            class="inline-flex items-center px-3 py-1.5 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-all duration-200"
          >
            <svg class="h-4 w-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
            </svg>
            复制
          </button>

          <!-- 版本历史按钮 -->
          <button
            v-if="prompt.version && prompt.version > 1"
            @click.stop="$emit('versions', prompt)"
            class="inline-flex items-center px-3 py-1.5 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-all duration-200"
          >
            <svg class="h-4 w-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            历史
          </button>
        </div>

        <!-- 更多操作下拉菜单 -->
        <div class="relative" ref="dropdownContainer">
          <button
            @click.stop="showDropdown = !showDropdown"
            class="inline-flex items-center p-2 border border-gray-300 rounded-md text-gray-400 hover:text-gray-600 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-all duration-200"
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
            <div v-if="showDropdown" class="absolute right-0 z-50 mt-2 w-48 bg-white rounded-md shadow-lg ring-1 ring-black ring-opacity-5 divide-y divide-gray-100">
              <div class="py-1">
                <button
                  @click.stop="$emit('openMoveToProject', prompt)"
                  class="group flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 w-full text-left"
                >
                  <svg class="mr-3 h-4 w-4 text-gray-400 group-hover:text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path></svg>
                  移动到...
                </button>
                <button
                  v-if="prompt.is_template"
                  @click.stop="$emit('clone', prompt)"
                  class="group flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 w-full text-left"
                >
                  <svg class="mr-3 h-4 w-4 text-gray-400 group-hover:text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                  </svg>
                  克隆模板
                </button>
                <button
                  @click.stop="$emit('duplicate', prompt)"
                  class="group flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 w-full text-left"
                >
                  <svg class="mr-3 h-4 w-4 text-gray-400 group-hover:text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7v8a2 2 0 002 2h6M8 7V5a2 2 0 012-2h4.586a1 1 0 01.707.293l4.414 4.414a1 1 0 01.293.707V15a2 2 0 01-2 2h-2M8 7H6a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2v-2" />
                  </svg>
                  创建副本
                </button>
                <button
                  @click.stop="exportPrompt"
                  class="group flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 w-full text-left"
                >
                  <svg class="mr-3 h-4 w-4 text-gray-400 group-hover:text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  导出
                </button>
              </div>
              <div class="py-1">
                <button
                  @click.stop="$emit('delete', prompt)"
                  class="group flex items-center px-4 py-2 text-sm text-red-700 hover:bg-red-50 w-full text-left"
                >
                  <svg class="mr-3 h-4 w-4 text-red-400 group-hover:text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                  删除
                </button>
              </div>
            </div>
          </transition>
        </div>
      </div>
    </div>

    <!-- 加载状态遮罩 -->
    <div v-if="isLoading" class="absolute inset-0 bg-white bg-opacity-75 flex items-center justify-center rounded-xl">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, type PropType } from 'vue'
import { useMainStore } from '@/stores'
import type { Prompt } from '@/services/api'

interface Props {
  prompt: Prompt
  isSelected?: boolean
  maxContentLength?: number
}

const props = withDefaults(defineProps<Props>(), {
  isSelected: false,
  maxContentLength: 150
})

const emit = defineEmits<{
  (e: 'click', prompt: Prompt): void
  (e: 'edit', prompt: Prompt): void
  (e: 'delete', prompt: Prompt): void
  (e: 'clone', prompt: Prompt): void
  (e: 'versions', prompt: Prompt): void
  (e: 'duplicate', prompt: Prompt): void
  (e: 'select', prompt: Prompt, selected: boolean): void
  (e: 'openMoveToProject', prompt: Prompt): void
}>()

const store = useMainStore()

const isExpanded = ref(false)
const showDropdown = ref(false)
const isLoading = ref(false)
const dropdownContainer = ref<HTMLElement | null>(null)

// 计算属性
const tags = computed(() => {
  if (!props.prompt.tags) return []
  return props.prompt.tags.split(',').map(tag => tag.trim()).filter(Boolean)
})

const truncatedContent = computed(() => {
  const content = props.prompt.content || ''
  if (isExpanded.value || content.length <= props.maxContentLength) {
    return content
  }
  return content.substring(0, props.maxContentLength) + '...'
})

const isFavorite = computed(() => store.isFavorite(props.prompt.id))

// 方法
const toggleExpanded = () => {
  isExpanded.value = !isExpanded.value
}

const toggleFavorite = async () => {
  try {
    isLoading.value = true
    await store.toggleFavorite(props.prompt.id)
  } catch (error) {
    console.error('切换收藏状态失败:', error)
  } finally {
    isLoading.value = false
  }
}

const copyContent = async () => {
  try {
    await navigator.clipboard.writeText(props.prompt.content)
    // 可以添加一个成功提示
    showSuccessMessage('内容已复制到剪贴板')
  } catch (error) {
    console.error('复制失败:', error)
    // 降级方案
    const textArea = document.createElement('textarea')
    textArea.value = props.prompt.content
    document.body.appendChild(textArea)
    textArea.select()
    document.execCommand('copy')
    document.body.removeChild(textArea)
    showSuccessMessage('内容已复制到剪贴板')
  }
}

const exportPrompt = () => {
  const data = {
    title: props.prompt.title,
    content: props.prompt.content,
    category: props.prompt.category,
    tags: props.prompt.tags,
    author: props.prompt.author,
    created_at: props.prompt.created_at
  }
  
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `${props.prompt.title.replace(/[^a-zA-Z0-9\u4e00-\u9fa5]/g, '_')}.json`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
  
  showSuccessMessage('提示词已导出')
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
  // 这里可以集成一个全局的消息提示组件
  console.log(message)
}

const closeDropdown = (event: MouseEvent) => {
  if (dropdownContainer.value && !dropdownContainer.value.contains(event.target as Node)) {
    showDropdown.value = false
  }
}

const handleCardClick = () => {
  console.log('Card clicked:', props.prompt.title)
  emit('click', props.prompt)
}

onMounted(() => {
  document.addEventListener('click', closeDropdown)
})

onUnmounted(() => {
  document.removeEventListener('click', closeDropdown)
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

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.group:hover .group-hover\:opacity-100 {
  animation: fadeIn 0.2s ease-out;
}

.prompt-card {
  @apply cursor-pointer bg-white rounded-lg shadow-md transition-all duration-300 hover:shadow-lg border border-transparent;
}
.prompt-card:hover {
  @apply border-blue-500;
}
</style>