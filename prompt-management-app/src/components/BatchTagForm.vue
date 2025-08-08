<template>
  <div class="max-w-md mx-auto">
    <div class="bg-white rounded-lg shadow-lg overflow-hidden">
      <!-- 头部 -->
      <div class="bg-gradient-to-r from-purple-600 to-pink-600 px-6 py-4">
        <h2 class="text-xl font-bold text-white">
          批量添加标签
        </h2>
        <p class="text-purple-100 text-sm mt-1">
          为选中的 {{ selectedCount }} 个提示词添加标签
        </p>
      </div>

      <form @submit.prevent="handleSubmit" class="p-6">
        <div class="mb-6">
          <label class="block text-sm font-medium text-gray-700 mb-2">
            选择或输入标签
          </label>
          
          <!-- 热门标签 -->
          <div v-if="popularTags.length > 0" class="mb-4">
            <p class="text-xs text-gray-500 mb-2">热门标签:</p>
            <div class="flex flex-wrap gap-2">
              <button
                v-for="tag in popularTags"
                :key="tag.id"
                type="button"
                @click="selectTag(tag.name)"
                class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium transition-colors duration-200"
                :class="[
                  selectedTags.includes(tag.name)
                    ? 'bg-purple-100 text-purple-800 border border-purple-300'
                    : 'bg-gray-100 text-gray-700 border border-gray-300 hover:bg-gray-200'
                ]"
              >
                {{ tag.name }}
                <span class="ml-1 text-xs opacity-75">({{ tag.usage_count }})</span>
                <svg v-if="selectedTags.includes(tag.name)" class="ml-1 h-3 w-3" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                </svg>
              </button>
            </div>
          </div>

          <!-- 自定义标签输入 -->
          <div>
            <p class="text-xs text-gray-500 mb-2">输入新标签:</p>
            <input
              v-model="customTag"
              type="text"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500"
              placeholder="请输入标签名称，回车添加"
              @keydown.enter.prevent="addCustomTag"
            />
            <p class="text-xs text-gray-500 mt-1">
              输入后按回车键添加，或用逗号分隔多个标签
            </p>
          </div>
        </div>

        <!-- 已选择的标签 -->
        <div v-if="selectedTags.length > 0" class="mb-6">
          <p class="text-sm font-medium text-gray-700 mb-2">已选择的标签:</p>
          <div class="flex flex-wrap gap-2">
            <span
              v-for="tag in selectedTags"
              :key="tag"
              class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-purple-100 text-purple-800 border border-purple-300"
            >
              {{ tag }}
              <button
                type="button"
                @click="removeTag(tag)"
                class="ml-1 inline-flex items-center justify-center w-4 h-4 rounded-full text-purple-600 hover:bg-purple-200 focus:outline-none"
              >
                <svg class="h-3 w-3" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
                </svg>
              </button>
            </span>
          </div>
        </div>

        <!-- 操作说明 -->
        <div class="mb-6 p-3 bg-yellow-50 border border-yellow-200 rounded-md">
          <div class="flex">
            <svg class="h-5 w-5 text-yellow-400 mr-2 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
            </svg>
            <div>
              <p class="text-sm text-yellow-800">
                <strong>注意:</strong> 这些标签会添加到所有选中的提示词中，不会覆盖现有标签。
              </p>
            </div>
          </div>
        </div>

        <!-- 提交按钮 -->
        <div class="flex justify-end space-x-3">
          <button
            type="button"
            @click="$emit('cancel')"
            class="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500"
          >
            取消
          </button>
          <button
            type="submit"
            :disabled="selectedTags.length === 0 || isSubmitting"
            class="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-purple-600 hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {{ isSubmitting ? '添加中...' : `添加 ${selectedTags.length} 个标签` }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { Tag } from '@/services/api'

interface Props {
  selectedCount: number
  popularTags: Tag[]
}

const props = defineProps<Props>()

const emit = defineEmits<{
  submit: [tag: string]
  cancel: []
}>()

const selectedTags = ref<string[]>([])
const customTag = ref('')
const isSubmitting = ref(false)

const selectTag = (tagName: string) => {
  const index = selectedTags.value.indexOf(tagName)
  if (index > -1) {
    selectedTags.value.splice(index, 1)
  } else {
    selectedTags.value.push(tagName)
  }
}

const removeTag = (tagName: string) => {
  const index = selectedTags.value.indexOf(tagName)
  if (index > -1) {
    selectedTags.value.splice(index, 1)
  }
}

const addCustomTag = () => {
  if (!customTag.value.trim()) return

  // 支持逗号分隔的多个标签
  const tags = customTag.value.split(',').map(tag => tag.trim()).filter(tag => tag)
  
  tags.forEach(tag => {
    if (!selectedTags.value.includes(tag)) {
      selectedTags.value.push(tag)
    }
  })

  customTag.value = ''
}

const handleSubmit = async () => {
  if (selectedTags.value.length === 0) return

  try {
    isSubmitting.value = true
    
    // 对于每个选中的标签，发送一个添加请求
    for (const tag of selectedTags.value) {
      emit('submit', tag)
    }
    
  } finally {
    isSubmitting.value = false
  }
}
</script>