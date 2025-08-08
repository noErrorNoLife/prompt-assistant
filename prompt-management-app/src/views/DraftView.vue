<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- 页面头部 -->
    <div class="mb-8">
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-6">
        <div>
          <h1 class="text-3xl font-bold text-gray-900">草稿箱</h1>
          <p class="mt-1 text-sm text-gray-500">
            专注创作的纯净写作空间
          </p>
        </div>
        <div class="mt-4 sm:mt-0">
          <button
            @click="handleNewDraft"
            class="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            <svg class="-ml-1 mr-2 h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
            新建草稿
          </button>
        </div>
      </div>
    </div>

    <!-- 草稿列表 -->
    <div v-if="loading" class="flex justify-center items-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
    </div>

    <div v-else-if="drafts.length === 0" class="text-center py-12">
      <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
      </svg>
      <h3 class="mt-4 text-lg font-medium text-gray-900">暂无草稿</h3>
      <p class="mt-2 text-sm text-gray-500">创建您的第一个草稿，享受纯净的写作体验</p>
      <div class="mt-6">
        <button
          @click="handleNewDraft"
          class="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
        >
          <svg class="-ml-1 mr-2 h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
          开始创作
        </button>
      </div>
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div
        v-for="draft in drafts"
        :key="draft.id"
        class="bg-white rounded-lg border border-gray-200 hover:border-gray-300 hover:shadow-md transition-all duration-200 cursor-pointer group"
        @click="handleEditDraft(draft.id)"
      >
        <div class="p-6">
          <!-- 标题和项目 -->
          <div class="flex items-start justify-between mb-3">
            <h3 class="text-lg font-medium text-gray-900 group-hover:text-blue-600 transition-colors line-clamp-2">
              {{ draft.title || '未命名草稿' }}
            </h3>
            <div class="ml-2 flex-shrink-0">
              <div class="relative" ref="menuRefs[draft.id]">
                <button
                  @click.stop="toggleMenu(draft.id)"
                  class="p-1 rounded-full text-gray-400 hover:text-gray-600 hover:bg-gray-100 opacity-0 group-hover:opacity-100 transition-all"
                >
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 5v.01M12 12v.01M12 19v.01M12 6a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2z" />
                  </svg>
                </button>
                
                <div v-if="activeMenu === draft.id" class="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg border border-gray-200 py-1 z-10">
                  <button
                    @click.stop="handlePublishDraft(draft.id)"
                    class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-50"
                  >
                    发布为提示词
                  </button>
                  <button
                    @click.stop="handleDeleteDraft(draft.id)"
                    class="block w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50"
                  >
                    删除草稿
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- 项目标签 -->
          <div v-if="draft.project_name" class="mb-3">
            <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
              {{ draft.project_name }}
            </span>
          </div>

          <!-- 内容预览 -->
          <div class="mb-4">
            <p class="text-sm text-gray-600 line-clamp-3">
              {{ getContentPreview(draft) }}
            </p>
          </div>

          <!-- 统计信息 -->
          <div class="flex items-center justify-between text-xs text-gray-500 mb-3">
            <span>{{ getCharacterCount(draft) }} 字符</span>
            <span>{{ getWordCount(draft) }} 词</span>
          </div>

          <!-- 时间和状态 -->
          <div class="flex items-center justify-between text-xs text-gray-400">
            <span>{{ formatDate(draft.updated_at) }}</span>
            <div class="flex items-center space-x-2">
              <span v-if="draft.auto_save_content && draft.auto_save_content !== draft.content" 
                    class="inline-flex items-center text-amber-600">
                <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
                </svg>
                有未保存更改
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 全屏编辑器 -->
    <DraftEditor
      v-if="showEditor"
      :draft-id="currentDraftId"
      :projects="projects"
      @close="handleCloseEditor"
      @saved="handleDraftSaved"
      @published="handleDraftPublished"
      @deleted="handleDraftDeleted"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { draftApi, type Draft } from '@/services/api'
import { useMainStore } from '@/stores'
import DraftEditor from '@/components/DraftEditor.vue'

const store = useMainStore()

// 状态管理
const drafts = ref<Draft[]>([])
const loading = ref(false)
const showEditor = ref(false)
const currentDraftId = ref<number | null>(null)
const activeMenu = ref<number | null>(null)
const menuRefs = ref<{[key: number]: HTMLElement}>({})

// 计算属性
const projects = ref(store.projects)

// 获取内容预览
const getContentPreview = (draft: Draft) => {
  const content = draft.auto_save_content || draft.content || ''
  return content.replace(/[#*`>-]/g, '').trim().substring(0, 150) || '空白草稿'
}

// 获取字符数
const getCharacterCount = (draft: Draft) => {
  const content = draft.auto_save_content || draft.content || ''
  return content.length
}

// 获取词数
const getWordCount = (draft: Draft) => {
  const content = draft.auto_save_content || draft.content || ''
  return content.trim() ? content.trim().split(/\s+/).length : 0
}

// 格式化日期
const formatDate = (dateString?: string) => {
  if (!dateString) return ''
  
  const date = new Date(dateString)
  const now = new Date()
  const diffInHours = (now.getTime() - date.getTime()) / (1000 * 60 * 60)
  
  if (diffInHours < 1) {
    return '刚刚'
  } else if (diffInHours < 24) {
    return `${Math.floor(diffInHours)}小时前`
  } else if (diffInHours < 48) {
    return '昨天'
  } else {
    return date.toLocaleDateString('zh-CN', { 
      month: 'short', 
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }
}

// 获取草稿列表
const fetchDrafts = async () => {
  try {
    loading.value = true
    drafts.value = await draftApi.getAll()
  } catch (error) {
    console.error('获取草稿列表失败:', error)
  } finally {
    loading.value = false
  }
}

// 新建草稿
const handleNewDraft = () => {
  currentDraftId.value = null
  showEditor.value = true
}

// 编辑草稿
const handleEditDraft = (draftId: number) => {
  currentDraftId.value = draftId
  showEditor.value = true
}

// 关闭编辑器
const handleCloseEditor = () => {
  showEditor.value = false
  currentDraftId.value = null
  // 重新获取草稿列表以更新状态
  fetchDrafts()
}

// 草稿保存成功
const handleDraftSaved = (draftId: number) => {
  console.log('草稿保存成功:', draftId)
  // 可以在这里添加通知
}

// 草稿发布成功
const handleDraftPublished = (promptId: number) => {
  console.log('草稿发布成功:', promptId)
  // 可以在这里添加通知或跳转到提示词页面
}

// 草稿删除成功
const handleDraftDeleted = () => {
  console.log('草稿删除成功')
  // 重新获取草稿列表
  fetchDrafts()
}

// 切换菜单
const toggleMenu = (draftId: number) => {
  activeMenu.value = activeMenu.value === draftId ? null : draftId
}

// 发布草稿
const handlePublishDraft = async (draftId: number) => {
  try {
    const result = await draftApi.publish(draftId)
    console.log('草稿发布成功:', result.id)
    // 重新获取草稿列表
    await fetchDrafts()
    // 可以在这里添加成功通知
  } catch (error) {
    console.error('发布草稿失败:', error)
  }
  activeMenu.value = null
}

// 删除草稿
const handleDeleteDraft = async (draftId: number) => {
  if (!confirm('确定要删除这个草稿吗？此操作无法撤销。')) {
    activeMenu.value = null
    return
  }
  
  try {
    await draftApi.delete(draftId)
    console.log('草稿删除成功')
    // 重新获取草稿列表
    await fetchDrafts()
    // 可以在这里添加成功通知
  } catch (error) {
    console.error('删除草稿失败:', error)
  }
  activeMenu.value = null
}

// 点击外部关闭菜单
const handleClickOutside = (event: Event) => {
  const target = event.target as Node
  let shouldClose = true
  
  for (const [draftId, menuEl] of Object.entries(menuRefs.value)) {
    if (menuEl && menuEl.contains(target)) {
      shouldClose = false
      break
    }
  }
  
  if (shouldClose) {
    activeMenu.value = null
  }
}

// 生命周期
onMounted(async () => {
  await Promise.all([
    fetchDrafts(),
    store.fetchProjects()
  ])
  
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
</style>