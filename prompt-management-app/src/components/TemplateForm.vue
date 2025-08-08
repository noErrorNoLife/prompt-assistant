<template>
  <div class="max-w-2xl mx-auto">
    <div class="bg-white rounded-lg shadow-lg overflow-hidden">
      <!-- 头部 -->
      <div class="bg-gradient-to-r from-purple-600 to-pink-600 px-6 py-4">
        <h2 class="text-xl font-bold text-white">
          {{ isEditing ? '编辑模板' : '创建模板' }}
        </h2>
        <p class="text-purple-100 text-sm mt-1">
          创建可复用的提示词模板，支持变量替换
        </p>
      </div>

      <form @submit.prevent="handleSubmit" class="p-6 space-y-6">
        <!-- 基本信息 -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              模板标题 <span class="text-red-500">*</span>
            </label>
            <input
              v-model="formData.title"
              type="text"
              required
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500"
              placeholder="请输入模板标题"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              分类
            </label>
            <input
              v-model="formData.category"
              type="text"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500"
              placeholder="请输入分类"
            />
          </div>
        </div>

        <!-- 模板内容 -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            模板内容 <span class="text-red-500">*</span>
          </label>
          <textarea
            v-model="formData.content"
            required
            rows="8"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500"
            placeholder="请输入模板内容，使用 {{变量名}} 定义变量..."
          ></textarea>
          <p class="text-sm text-gray-500 mt-1">
            使用双大括号定义变量，如：{{用户名}}、{{主题}}
          </p>
        </div>

        <!-- 模板变量配置 -->
        <div>
          <div class="flex items-center justify-between mb-3">
            <label class="block text-sm font-medium text-gray-700">
              模板变量
            </label>
            <button
              type="button"
              @click="addVariable"
              class="inline-flex items-center px-3 py-1 border border-transparent text-sm font-medium rounded-md text-purple-600 bg-purple-100 hover:bg-purple-200"
            >
              <svg class="mr-1 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
              添加变量
            </button>
          </div>

          <div v-if="formData.template_variables.length === 0" class="text-center py-8 text-gray-500">
            <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
            </svg>
            <p class="mt-2">暂无模板变量，点击上方按钮添加</p>
          </div>

          <div v-else class="space-y-3">
            <div
              v-for="(variable, index) in formData.template_variables"
              :key="index"
              class="border border-gray-200 rounded-lg p-4"
            >
              <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
                <div>
                  <label class="block text-xs font-medium text-gray-600 mb-1">变量名</label>
                  <input
                    v-model="variable.name"
                    type="text"
                    class="w-full px-2 py-1 text-sm border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-purple-500"
                    placeholder="变量名"
                  />
                </div>
                <div>
                  <label class="block text-xs font-medium text-gray-600 mb-1">类型</label>
                  <select
                    v-model="variable.type"
                    class="w-full px-2 py-1 text-sm border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-purple-500"
                  >
                    <option value="text">文本</option>
                    <option value="textarea">多行文本</option>
                    <option value="number">数字</option>
                    <option value="select">选择</option>
                  </select>
                </div>
                <div>
                  <label class="block text-xs font-medium text-gray-600 mb-1">默认值</label>
                  <div class="flex">
                    <input
                      v-model="variable.default_value"
                      type="text"
                      class="flex-1 px-2 py-1 text-sm border border-gray-300 rounded-l focus:outline-none focus:ring-1 focus:ring-purple-500"
                      placeholder="默认值"
                    />
                    <button
                      type="button"
                      @click="removeVariable(index)"
                      class="px-2 py-1 border border-l-0 border-gray-300 rounded-r text-red-600 hover:bg-red-50"
                    >
                      <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                      </svg>
                    </button>
                  </div>
                </div>
              </div>
              <div class="mt-2 grid grid-cols-1 md:grid-cols-2 gap-3">
                <div>
                  <label class="block text-xs font-medium text-gray-600 mb-1">描述</label>
                  <input
                    v-model="variable.description"
                    type="text"
                    class="w-full px-2 py-1 text-sm border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-purple-500"
                    placeholder="变量描述"
                  />
                </div>
                <div class="flex items-center">
                  <label class="flex items-center text-sm text-gray-600">
                    <input
                      v-model="variable.is_required"
                      type="checkbox"
                      class="mr-2 text-purple-600 focus:ring-purple-500"
                    />
                    必填项
                  </label>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 标签 -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            标签
          </label>
          <input
            v-model="formData.tags"
            type="text"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500"
            placeholder="请输入标签，用逗号分隔"
          />
        </div>

        <!-- 其他选项 -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              作者
            </label>
            <input
              v-model="formData.author"
              type="text"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500"
              placeholder="作者名称"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              语言
            </label>
            <select
              v-model="formData.language"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500"
            >
              <option value="zh">中文</option>
              <option value="en">English</option>
              <option value="ja">日本語</option>
              <option value="ko">한국어</option>
            </select>
          </div>
        </div>

        <!-- 提交按钮 -->
        <div class="flex justify-end space-x-3 pt-6 border-t border-gray-200">
          <button
            type="button"
            @click="$emit('cancel')"
            class="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500"
          >
            取消
          </button>
          <button
            type="submit"
            :disabled="isSubmitting"
            class="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-purple-600 hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 disabled:opacity-50"
          >
            {{ isSubmitting ? '保存中...' : (isEditing ? '保存更改' : '创建模板') }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import type { Prompt, TemplateVariable } from '@/services/api'

interface Props {
  isEditing: boolean
  template?: Prompt
}

const props = withDefaults(defineProps<Props>(), {
  template: undefined
})

const emit = defineEmits<{
  submit: [data: any]
  cancel: []
}>()

const isSubmitting = ref(false)

const formData = reactive({
  title: '',
  content: '',
  category: '',
  tags: '',
  author: '',
  language: 'zh',
  is_template: true,
  template_variables: [] as TemplateVariable[]
})

const addVariable = () => {
  formData.template_variables.push({
    name: '',
    type: 'text',
    default_value: '',
    description: '',
    is_required: false
  })
}

const removeVariable = (index: number) => {
  formData.template_variables.splice(index, 1)
}

const handleSubmit = async () => {
  try {
    isSubmitting.value = true
    emit('submit', { ...formData })
  } finally {
    isSubmitting.value = false
  }
}

onMounted(() => {
  if (props.isEditing && props.template) {
    Object.assign(formData, {
      title: props.template.title,
      content: props.template.content,
      category: props.template.category || '',
      tags: props.template.tags || '',
      author: props.template.author || '',
      language: props.template.language || 'zh',
      is_template: true,
      template_variables: props.template.template_variables || []
    })
  }
})
</script>