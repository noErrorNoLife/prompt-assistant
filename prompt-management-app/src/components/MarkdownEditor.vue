<template>
  <div class="markdown-editor h-full flex flex-col">
    <!-- 工具栏 -->
    <div class="toolbar border-b border-gray-200 p-3 bg-gray-50">
      <div class="flex items-center justify-between">
        <div class="flex items-center space-x-2">
          <button
            type="button"
            @click="insertMarkdown('**', '**')"
            class="toolbar-btn"
            title="加粗"
          >
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path d="M3 5v10h4.5c1.933 0 3.5-1.567 3.5-3.5 0-.827-.287-1.587-.778-2.19A3.49 3.49 0 0011 6.5C11 4.567 9.433 3 7.5 3H3v2zm2 2h2.5c.828 0 1.5.672 1.5 1.5S8.328 8 7.5 8H5V7zm0 3h3c.828 0 1.5.672 1.5 1.5S8.828 12 8 12H5v-2z"/>
            </svg>
          </button>
          <button
            type="button"
            @click="insertMarkdown('*', '*')"
            class="toolbar-btn"
            title="斜体"
          >
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path d="M8 3v2h2l-2 10H6v2h6v-2h-2l2-10h2V3H8z"/>
            </svg>
          </button>
          <button
            type="button"
            @click="insertMarkdown('`', '`')"
            class="toolbar-btn"
            title="行内代码"
          >
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M12.316 3.051a1 1 0 01.633 1.265l-4 12a1 1 0 11-1.898-.632l4-12a1 1 0 011.265-.633zM5.707 6.293a1 1 0 010 1.414L3.414 10l2.293 2.293a1 1 0 11-1.414 1.414l-3-3a1 1 0 010-1.414l3-3a1 1 0 011.414 0zm8.586 0a1 1 0 011.414 0l3 3a1 1 0 010 1.414l-3 3a1 1 0 11-1.414-1.414L16.586 10l-2.293-2.293a1 1 0 010-1.414z" clip-rule="evenodd"/>
            </svg>
          </button>
          <button
            type="button"
            @click="insertCodeBlock"
            class="toolbar-btn"
            title="代码块"
          >
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 011 1v12a1 1 0 01-1 1H4a1 1 0 01-1-1V4zm2 2v8h10V6H5z" clip-rule="evenodd"/>
            </svg>
          </button>
          <div class="w-px h-6 bg-gray-300"></div>
          <button
            type="button"
            @click="insertMarkdown('## ', '')"
            class="toolbar-btn"
            title="标题"
          >
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path d="M3 4h14a1 1 0 010 2H3a1 1 0 010-2zm0 4h14a1 1 0 010 2H3a1 1 0 010-2zm0 4h10a1 1 0 010 2H3a1 1 0 010-2z"/>
            </svg>
          </button>
          <button
            type="button"
            @click="insertList"
            class="toolbar-btn"
            title="列表"
          >
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clip-rule="evenodd"/>
            </svg>
          </button>
        </div>
        <div class="flex items-center space-x-3">
          <button
            type="button"
            @click="togglePreview"
            :class="[
              'toolbar-btn',
              showPreview ? 'bg-blue-100 text-blue-600' : ''
            ]"
            title="切换预览"
          >
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path d="M10 12a2 2 0 100-4 2 2 0 000 4z"/>
              <path fill-rule="evenodd" d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clip-rule="evenodd"/>
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- 编辑器主体 -->
    <div class="flex-1 flex overflow-hidden">
      <!-- 左侧编辑区 -->
      <div :class="[
        'border-r border-gray-200 flex flex-col',
        showPreview ? 'w-1/2' : 'w-full'
      ]">
        <div class="bg-gray-50 px-4 py-2 text-sm font-medium text-gray-700 border-b border-gray-200">
          编辑器
        </div>
        <textarea
          ref="textareaRef"
          v-model="content"
          @input="handleInput"
          @keydown="handleKeydown"
          class="flex-1 p-4 font-mono text-sm resize-none outline-none border-none focus:ring-0"
          :placeholder="placeholder"
          spellcheck="false"
        ></textarea>
      </div>

      <!-- 右侧预览区 -->
      <div v-if="showPreview" class="w-1/2 flex flex-col">
        <div class="bg-gray-50 px-4 py-2 text-sm font-medium text-gray-700 border-b border-gray-200">
          预览
        </div>
        <div class="flex-1 p-4 overflow-y-auto prose prose-sm max-w-none">
          <div v-html="renderedContent" class="markdown-content"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, nextTick, onMounted, onUnmounted } from 'vue'

interface Props {
  modelValue: string
  placeholder?: string
  height?: string
}

const props = withDefaults(defineProps<Props>(), {
  placeholder: '在这里输入您的提示词内容...',
  height: '400px'
})

const emit = defineEmits<{
  'update:modelValue': [value: string]
  save: [value: string]
}>()

const textareaRef = ref<HTMLTextAreaElement>()
const showPreview = ref(true)
const content = ref(props.modelValue)

// 简单的 Markdown 渲染（实际项目中建议使用 marked 或类似库）
const renderedContent = computed(() => {
  let html = content.value
    // 标题
    .replace(/^### (.*$)/gim, '<h3>$1</h3>')
    .replace(/^## (.*$)/gim, '<h2>$1</h2>')
    .replace(/^# (.*$)/gim, '<h1>$1</h1>')
    // 加粗
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    // 斜体
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    // 行内代码
    .replace(/`(.*?)`/g, '<code>$1</code>')
    // 换行
    .replace(/\n/g, '<br>')
    
  // 代码块
  html = html.replace(/```([\s\S]*?)```/g, '<pre><code>$1</code></pre>')
  
  // 列表
  html = html.replace(/^\- (.*$)/gim, '<li>$1</li>')
  html = html.replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>')
  
  return html || '<p class="text-gray-400">在左侧编辑器中输入内容来查看预览...</p>'
})

// 监听内容变化
watch(content, (newValue) => {
  emit('update:modelValue', newValue)
})

// 监听外部值变化
watch(() => props.modelValue, (newValue) => {
  if (newValue !== content.value) {
    content.value = newValue
  }
})

// 工具栏方法
const insertMarkdown = (before: string, after: string) => {
  if (!textareaRef.value) return
  
  const textarea = textareaRef.value
  const start = textarea.selectionStart
  const end = textarea.selectionEnd
  const selectedText = content.value.substring(start, end)
  
  const newText = before + selectedText + after
  content.value = content.value.substring(0, start) + newText + content.value.substring(end)
  
  nextTick(() => {
    textarea.focus()
    textarea.setSelectionRange(start + before.length, start + before.length + selectedText.length)
  })
}

const insertCodeBlock = () => {
  insertMarkdown('\n```\n', '\n```\n')
}

const insertList = () => {
  if (!textareaRef.value) return
  
  const textarea = textareaRef.value
  const start = textarea.selectionStart
  const lines = content.value.substring(0, start).split('\n')
  const currentLine = lines[lines.length - 1]
  
  if (currentLine.trim() === '') {
    insertMarkdown('- ', '')
  } else {
    insertMarkdown('\n- ', '')
  }
}

const togglePreview = () => {
  showPreview.value = !showPreview.value
}

// 键盘事件处理
const handleKeydown = (event: KeyboardEvent) => {
  // Ctrl+S 保存
  if (event.ctrlKey && event.key === 's') {
    event.preventDefault()
    emit('save', content.value)
    return
  }
  
  // Tab 键插入空格
  if (event.key === 'Tab') {
    event.preventDefault()
    insertMarkdown('  ', '')
    return
  }
  
  // 自动列表
  if (event.key === 'Enter') {
    const textarea = textareaRef.value!
    const start = textarea.selectionStart
    const lines = content.value.substring(0, start).split('\n')
    const currentLine = lines[lines.length - 1]
    
    if (currentLine.match(/^(\s*)[-*+]\s/)) {
      event.preventDefault()
      const indent = currentLine.match(/^(\s*)/)?.[1] || ''
      insertMarkdown('\n' + indent + '- ', '')
    }
  }
}

const handleInput = () => {
  // 处理输入事件
}

onMounted(() => {
  // 挂载时自动聚焦
  nextTick(() => {
    textareaRef.value?.focus()
  })
})

onUnmounted(() => {
  // 组件卸载时无需操作
})
</script>

<style scoped>
.toolbar-btn {
  @apply p-2 text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded transition-colors duration-150;
}

.markdown-content {
  @apply text-gray-800;
}

.markdown-content h1 {
  @apply text-2xl font-bold mb-4 text-gray-900;
}

.markdown-content h2 {
  @apply text-xl font-bold mb-3 text-gray-900;
}

.markdown-content h3 {
  @apply text-lg font-bold mb-2 text-gray-900;
}

.markdown-content code {
  @apply bg-gray-100 px-1 py-0.5 rounded text-sm font-mono text-pink-600;
}

.markdown-content pre {
  @apply bg-gray-100 p-3 rounded-lg overflow-x-auto mb-4;
}

.markdown-content pre code {
  @apply bg-transparent p-0 text-gray-800;
}

.markdown-content ul {
  @apply list-disc list-inside mb-4;
}

.markdown-content li {
  @apply mb-1;
}

.markdown-content strong {
  @apply font-bold;
}

.markdown-content em {
  @apply italic;
}
</style> 