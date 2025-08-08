<template>
  <div class="flex flex-col bg-white rounded-lg max-h-[100vh] h-full overflow-hidden" @click.stop>
    <div class="border-b border-gray-200 px-6 py-4 flex-shrink-0">
      <h3 class="text-lg font-medium text-gray-900">
        {{ isEditing ? '编辑提示词' : '创建新提示词' }}
      </h3>
      <p class="text-sm text-gray-500 mt-1">
        {{ isEditing ? '修改您的提示词内容' : '创建一个新的AI提示词' }}
      </p>
    </div>

    <form @submit.prevent="handleSubmit" class="flex-1 flex flex-col overflow-hidden">
      <div class="flex-1 overflow-y-auto p-6 space-y-6">
        <!-- 基本信息 -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label for="title" class="block text-sm font-medium text-gray-700 mb-2">
              标题 <span class="text-red-500">*</span>
            </label>
            <input
              id="title"
              v-model="form.title"
              type="text"
              required
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              placeholder="请输入提示词标题"
            />
          </div>

          <div>
            <label for="project" class="block text-sm font-medium text-gray-700 mb-2">
              项目
            </label>
            <select
              id="project"
              v-model="form.project_id"
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              <option :value="null">-- 无项目 --</option>
              <option v-for="project in store.projects" :key="project.id" :value="project.id">
                {{ project.name }}
              </option>
            </select>
          </div>

          <div>
            <label for="category" class="block text-sm font-medium text-gray-700 mb-2">
              分类
            </label>
            <input
              id="category"
              v-model="form.category"
              type="text"
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              placeholder="如：编程、写作、分析等"
            />
          </div>
        </div>

        <div>
          <label for="tags" class="block text-sm font-medium text-gray-700 mb-2">
            标签
          </label>
          <input
            id="tags"
            v-model="tagsInput"
            type="text"
            class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            placeholder="用逗号分隔多个标签，如：python, 代码生成, 开发"
          />
        </div>

        <!-- Markdown 编辑器 -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            内容 <span class="text-red-500">*</span>
          </label>
          <p class="text-sm text-gray-500 mb-3">
            支持 Markdown 语法，包括代码块、列表、加粗等格式
          </p>
          <div class="border border-gray-300 rounded-lg overflow-hidden" style="height: 500px;">
            <MarkdownEditor
              v-model="form.content"
              placeholder="请输入您的提示词内容，支持 Markdown 语法..."
              @save="handleSave"
            />
          </div>
        </div>

        <!-- 高级选项 -->
        <div class="border-t border-gray-200 pt-6">
          <div class="flex items-center justify-between mb-4">
            <h4 class="text-sm font-medium text-gray-900">高级选项</h4>
            <button
              type="button"
              @click="showAdvanced = !showAdvanced"
              class="text-sm text-blue-600 hover:text-blue-700"
            >
              {{ showAdvanced ? '隐藏' : '显示' }}
            </button>
          </div>

          <div v-if="showAdvanced" class="space-y-4">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label for="author" class="block text-sm font-medium text-gray-700 mb-2">
                  作者
                </label>
                <input
                  id="author"
                  v-model="form.author"
                  type="text"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  placeholder="作者姓名"
                />
              </div>

              <div>
                <label for="language" class="block text-sm font-medium text-gray-700 mb-2">
                  语言
                </label>
                <select
                  id="language"
                  v-model="form.language"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                >
                  <option value="zh">中文</option>
                  <option value="en">English</option>
                  <option value="ja">日本語</option>
                  <option value="ko">한국어</option>
                </select>
              </div>
            </div>

            <div class="flex items-center">
              <input
                id="is_template"
                v-model="form.is_template"
                type="checkbox"
                class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
              <label for="is_template" class="ml-2 block text-sm text-gray-700">
                标记为模板（其他用户可以复用此提示词）
              </label>
            </div>
          </div>
        </div>
      </div>

      <!-- 操作按钮 -->
      <div class="flex-shrink-0 p-6 border-t border-gray-200 flex items-center justify-end space-x-4">
        <button
          type="button"
          @click="emit('cancel')"
          class="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
        >
          取消
        </button>
        <button
          type="submit"
          :disabled="!form.title?.trim() || !form.content?.trim()"
          class="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {{ isEditing ? '更新' : '创建' }}
        </button>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import MarkdownEditor from './MarkdownEditor.vue'
import type { Prompt } from '@/stores'
import { useMainStore } from '@/stores'

interface Props {
  prompt?: Prompt
}

const props = defineProps<Props>()

const isEditing = computed(() => !!props.prompt?.id)

const emit = defineEmits<{
  submit: [prompt: Partial<Prompt>]
  cancel: []
  close: []
}>()

const store = useMainStore()
const showAdvanced = ref(false)
const tagsInput = ref('')

const form = ref({
  title: '',
  content: '',
  project_id: store.selectedProjectId || null,
  category: '',
  tags: '',
  author: '',
  language: 'zh',
  is_template: false
})

// 监听 props 变化，初始化表单
const lastPromptId = ref<number | undefined>(undefined)

watch(() => props.prompt, (newPrompt) => {
  if (newPrompt) {
    form.value = {
      title: newPrompt.title || '',
      content: newPrompt.content || '',
      project_id: newPrompt.project_id || null,
      category: newPrompt.category || '',
      tags: newPrompt.tags || '',
      author: newPrompt.author || '',
      language: newPrompt.language || 'zh',
      is_template: newPrompt.is_template || false
    }
    tagsInput.value = newPrompt.tags || ''
    lastPromptId.value = newPrompt.id
  } else if (lastPromptId.value) {
    // 重置表单，从编辑切换到新建时
    form.value = {
      title: '',
      content: '',
      project_id: store.selectedProjectId || null,
      category: '',
      tags: '',
      author: '',
      language: 'zh',
      is_template: false
    }
    tagsInput.value = ''
  }
  lastPromptId.value = newPrompt?.id
}, { immediate: true, deep: true })

// 监听标签输入变化
watch(tagsInput, (newVal) => {
  form.value.tags = newVal
})

const handleSave = () => {
  // 可以在这里触发一个事件或方法
  // 例如，可以自动提交表单
  handleSubmit()
}

const handleSubmit = () => {
  const { project_id, ...rest } = form.value
  const submissionData: Partial<Prompt> = {
    ...rest,
    tags: tagsInput.value,
    project_id: project_id === null ? undefined : project_id,
  }
  emit('submit', submissionData)
}
</script>

<style scoped>
/* All old styles removed */
</style> 