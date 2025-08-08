<template>
  <div class="fixed inset-0 bg-gray-50 z-50 flex flex-col">
    <!-- 顶部工具栏 -->
    <div class="h-16 bg-white border-b border-gray-200 flex items-center justify-between px-6 flex-shrink-0">
      <div class="flex items-center space-x-4">
        <button
          @click="$emit('close')"
          class="inline-flex items-center p-2 rounded-md text-gray-400 hover:text-gray-600 hover:bg-gray-100 transition-colors"
          title="关闭编辑器"
        >
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
        
        <div class="h-6 w-px bg-gray-300"></div>
        
        <div class="flex items-center space-x-2">
          <input
            v-model="title"
            type="text"
            placeholder="输入标题..."
            class="bg-transparent text-lg font-medium text-gray-900 placeholder-gray-400 border-none focus:outline-none focus:ring-0 min-w-0 flex-1"
            @blur="handleTitleChange"
          />
          <span v-if="autoSaveStatus" class="text-sm text-gray-500">
            {{ autoSaveStatus }}
          </span>
        </div>
      </div>

      <div class="flex items-center space-x-3">
        <!-- 字数统计 -->
        <div class="text-sm text-gray-500">
          {{ characterCount }} 字符
        </div>
        
        <!-- 项目选择 -->
        <select
          v-model="selectedProjectId"
          class="text-sm border border-gray-300 rounded-md px-3 py-1 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          @change="handleProjectChange"
        >
          <option :value="null">无项目</option>
          <option v-for="project in projects" :key="project.id" :value="project.id">
            {{ project.name }}
          </option>
        </select>

        <!-- 保存按钮 -->
        <button
          @click="handleSave"
          :disabled="!hasChanges"
          class="px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          保存
        </button>

        <!-- 发布按钮 -->
        <button
          @click="handlePublish"
          :disabled="!content.trim()"
          class="px-4 py-2 bg-green-600 text-white text-sm font-medium rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          发布
        </button>

        <!-- 更多选项 -->
        <div class="relative" ref="menuRef">
          <button
            @click="showMenu = !showMenu"
            class="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-md transition-colors"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 5v.01M12 12v.01M12 19v.01M12 6a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2z" />
            </svg>
          </button>
          
          <div v-if="showMenu" class="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg border border-gray-200 py-1 z-10">
            <button
              @click="handleDeleteDraft"
              class="block w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50"
            >
              删除草稿
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 编辑区域 -->
    <div class="flex-1 flex overflow-hidden">
      <!-- 左侧：纯文本编辑器 -->
      <div class="flex-1 flex flex-col">
        <div class="h-full p-8 overflow-auto">
          <textarea
            v-model="content"
            ref="textareaRef"
            placeholder="开始编写您的 AI Prompt...

支持 Markdown 语法：
- **粗体文本**
- *斜体文本*
- `代码`
- > 引用
- - 列表项
- [链接](URL)

提示：
- 使用 Ctrl+S 快速保存
- 内容会自动保存，无需担心丢失
- 专注于创作，让创意自由流淌"
            class="w-full h-full resize-none border-none focus:outline-none focus:ring-0 text-gray-900 placeholder-gray-400 bg-transparent text-lg leading-relaxed font-mono"
            @input="handleContentChange"
            @keydown="handleKeydown"
          ></textarea>
        </div>
      </div>

      <!-- 右侧：实时预览 -->
      <div v-if="showPreview" class="w-1/2 border-l border-gray-200 bg-white flex flex-col">
        <div class="h-12 border-b border-gray-200 flex items-center justify-between px-4 bg-gray-50">
          <h3 class="text-sm font-medium text-gray-700">实时预览</h3>
          <button
            @click="showPreview = false"
            class="text-gray-400 hover:text-gray-600"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <div class="flex-1 overflow-auto p-6">
          <div class="prose prose-gray max-w-none" v-html="previewContent"></div>
        </div>
      </div>
    </div>

    <!-- 底部状态栏 -->
    <div class="h-8 bg-gray-100 border-t border-gray-200 flex items-center justify-between px-6 text-xs text-gray-500 flex-shrink-0">
      <div class="flex items-center space-x-4">
        <span>行 {{ currentLine }} 列 {{ currentColumn }}</span>
        <span>{{ wordCount }} 词</span>
        <span v-if="lastSaved">上次保存: {{ formatTime(lastSaved) }}</span>
      </div>
      
      <div class="flex items-center space-x-4">
        <button
          @click="showPreview = !showPreview"
          class="hover:text-gray-700 transition-colors"
        >
          {{ showPreview ? '隐藏预览' : '显示预览' }}
        </button>
        <span>{{ language === 'zh' ? '中文' : 'English' }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted, onUnmounted, nextTick } from 'vue'
import { marked } from 'marked'
import { draftApi, type Draft } from '@/services/api'

interface Props {
  draftId?: number
  projects?: Array<{id: number, name: string}>
}

const props = defineProps<Props>()
const emit = defineEmits<{
  close: []
  saved: [draftId: number]
  published: [promptId: number]
  deleted: []
}>()

// 状态管理
const title = ref('')
const content = ref('')
const selectedProjectId = ref<number | null>(null)
const language = ref('zh')
const showPreview = ref(false)
const showMenu = ref(false)
const autoSaveStatus = ref('')
const hasChanges = ref(false)
const lastSaved = ref<Date | null>(null)

// DOM 引用
const textareaRef = ref<HTMLTextAreaElement | null>(null)
const menuRef = ref<HTMLElement | null>(null)

// 自动保存相关
let autoSaveTimer: ReturnType<typeof setTimeout> | null = null
let currentDraftId = ref<number | null>(props.draftId || null)

// 计算属性
const characterCount = computed(() => content.value.length)
const wordCount = computed(() => {
  return content.value.trim() ? content.value.trim().split(/\s+/).length : 0
})

const previewContent = computed(() => {
  if (!content.value.trim()) return '<p class="text-gray-400">开始输入内容以查看预览...</p>'
  try {
    return marked(content.value)
  } catch (error) {
    return '<p class="text-red-400">预览解析错误</p>'
  }
})

// 获取当前光标位置
const currentLine = ref(1)
const currentColumn = ref(1)

// 格式化时间
const formatTime = (date: Date) => {
  return date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
}

// 更新光标位置
const updateCursorPosition = () => {
  if (!textareaRef.value) return
  
  const textarea = textareaRef.value
  const cursorPos = textarea.selectionStart
  const textBeforeCursor = content.value.substring(0, cursorPos)
  const lines = textBeforeCursor.split('\n')
  
  currentLine.value = lines.length
  currentColumn.value = lines[lines.length - 1].length + 1
}

// 处理内容变化
const handleContentChange = () => {
  hasChanges.value = true
  updateCursorPosition()
  
  // 清除之前的自动保存计时器
  if (autoSaveTimer) {
    clearTimeout(autoSaveTimer)
  }
  
  // 设置新的自动保存计时器（2秒后自动保存）
  autoSaveTimer = setTimeout(() => {
    handleAutoSave()
  }, 2000)
}

// 处理标题变化
const handleTitleChange = () => {
  hasChanges.value = true
}

// 处理项目变化
const handleProjectChange = () => {
  hasChanges.value = true
}

// 自动保存
const handleAutoSave = async () => {
  if (!currentDraftId.value || !content.value.trim()) return
  
  try {
    autoSaveStatus.value = '正在保存...'
    await draftApi.autoSave(currentDraftId.value, content.value)
    autoSaveStatus.value = '已自动保存'
    setTimeout(() => {
      autoSaveStatus.value = ''
    }, 2000)
  } catch (error) {
    console.error('自动保存失败:', error)
    autoSaveStatus.value = '保存失败'
  }
}

// 手动保存
const handleSave = async () => {
  try {
    if (!currentDraftId.value) {
      // 创建新草稿
      const result = await draftApi.create({
        title: title.value || undefined,
        content: content.value,
        project_id: selectedProjectId.value,
        language: language.value
      })
      currentDraftId.value = result.id
    } else {
      // 更新现有草稿
      await draftApi.update(currentDraftId.value, {
        title: title.value || undefined,
        content: content.value,
        project_id: selectedProjectId.value,
        language: language.value
      })
    }
    
    hasChanges.value = false
    lastSaved.value = new Date()
    emit('saved', currentDraftId.value)
  } catch (error) {
    console.error('保存失败:', error)
  }
}

// 发布草稿
const handlePublish = async () => {
  if (!currentDraftId.value) {
    // 先保存为草稿
    await handleSave()
  }
  
  if (!currentDraftId.value) return
  
  try {
    const result = await draftApi.publish(currentDraftId.value)
    emit('published', result.id)
    emit('close')
  } catch (error) {
    console.error('发布失败:', error)
  }
}

// 删除草稿
const handleDeleteDraft = async () => {
  if (!currentDraftId.value) {
    emit('close')
    return
  }
  
  if (!confirm('确定要删除这个草稿吗？此操作无法撤销。')) return
  
  try {
    await draftApi.delete(currentDraftId.value)
    emit('deleted')
    emit('close')
  } catch (error) {
    console.error('删除失败:', error)
  }
}

// 键盘快捷键
const handleKeydown = (event: KeyboardEvent) => {
  // Ctrl+S 保存
  if ((event.ctrlKey || event.metaKey) && event.key === 's') {
    event.preventDefault()
    handleSave()
  }
  
  // Ctrl+Enter 发布
  if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') {
    event.preventDefault()
    handlePublish()
  }
  
  // ESC 关闭
  if (event.key === 'Escape') {
    if (hasChanges.value) {
      if (confirm('有未保存的更改，确定要关闭吗？')) {
        emit('close')
      }
    } else {
      emit('close')
    }
  }
}

// 点击外部关闭菜单
const handleClickOutside = (event: Event) => {
  if (menuRef.value && !menuRef.value.contains(event.target as Node)) {
    showMenu.value = false
  }
}

// 加载草稿数据
const loadDraft = async (draftId: number) => {
  try {
    const draft = await draftApi.getById(draftId)
    title.value = draft.title || ''
    content.value = draft.auto_save_content || draft.content || ''
    selectedProjectId.value = draft.project_id || null
    language.value = draft.language || 'zh'
    hasChanges.value = false
    
    await nextTick()
    updateCursorPosition()
  } catch (error) {
    console.error('加载草稿失败:', error)
  }
}

// 生命周期
onMounted(async () => {
  if (props.draftId) {
    await loadDraft(props.draftId)
  }
  
  document.addEventListener('click', handleClickOutside)
  
  // 聚焦到编辑器
  await nextTick()
  if (textareaRef.value) {
    textareaRef.value.focus()
  }
})

onUnmounted(() => {
  if (autoSaveTimer) {
    clearTimeout(autoSaveTimer)
  }
  document.removeEventListener('click', handleClickOutside)
})

// 监听内容变化更新光标位置
watch(content, () => {
  nextTick(() => {
    updateCursorPosition()
  })
})

// 监听 textarea 的点击和键盘事件
onMounted(() => {
  if (textareaRef.value) {
    textareaRef.value.addEventListener('click', updateCursorPosition)
    textareaRef.value.addEventListener('keyup', updateCursorPosition)
  }
})
</script>

<style scoped>
/* 滚动条样式 */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
}

::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

/* 确保 textarea 在全屏状态下正确显示 */
textarea {
  font-family: 'JetBrains Mono', 'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', Consolas, 'Courier New', monospace;
}
</style>