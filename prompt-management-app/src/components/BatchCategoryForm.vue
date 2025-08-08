<template>
  <div class="max-w-md mx-auto">
    <div class="bg-white rounded-lg shadow-lg overflow-hidden">
      <!-- 头部 -->
      <div class="bg-gradient-to-r from-blue-600 to-indigo-600 px-6 py-4">
        <h2 class="text-xl font-bold text-white">
          批量设置分类
        </h2>
        <p class="text-blue-100 text-sm mt-1">
          为选中的 {{ selectedCount }} 个提示词设置分类
        </p>
      </div>

      <form @submit.prevent="handleSubmit" class="p-6">
        <div class="mb-6">
          <label class="block text-sm font-medium text-gray-700 mb-2">
            选择分类
          </label>
          <div class="space-y-2">
            <!-- 现有分类选项 -->
            <div v-if="categories.length > 0">
              <p class="text-xs text-gray-500 mb-2">选择现有分类:</p>
              <div class="grid grid-cols-2 gap-2">
                <label
                  v-for="category in categories"
                  :key="category"
                  class="flex items-center p-2 border border-gray-200 rounded-md hover:bg-gray-50 cursor-pointer"
                  :class="{ 'border-blue-500 bg-blue-50': selectedCategory === category }"
                >
                  <input
                    v-model="selectedCategory"
                    :value="category"
                    type="radio"
                    name="category"
                    class="mr-2 text-blue-600 focus:ring-blue-500"
                  />
                  <span class="text-sm">{{ category }}</span>
                </label>
              </div>
            </div>

            <!-- 分隔线 -->
            <div v-if="categories.length > 0" class="relative my-4">
              <div class="absolute inset-0 flex items-center">
                <div class="w-full border-t border-gray-300"></div>
              </div>
              <div class="relative flex justify-center text-sm">
                <span class="px-2 bg-white text-gray-500">或</span>
              </div>
            </div>

            <!-- 自定义分类 -->
            <div>
              <p class="text-xs text-gray-500 mb-2">输入新分类:</p>
              <input
                v-model="customCategory"
                type="text"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                placeholder="请输入新的分类名称"
                @input="handleCustomInput"
              />
            </div>

            <!-- 清除分类选项 -->
            <div class="pt-2">
              <label class="flex items-center p-2 border border-gray-200 rounded-md hover:bg-gray-50 cursor-pointer">
                <input
                  v-model="clearCategory"
                  type="checkbox"
                  class="mr-2 text-red-600 focus:ring-red-500"
                  @change="handleClearChange"
                />
                <span class="text-sm text-red-600">清除分类</span>
              </label>
            </div>
          </div>
        </div>

        <!-- 预览 -->
        <div v-if="finalCategory || clearCategory" class="mb-6 p-3 bg-gray-50 border border-gray-200 rounded-md">
          <p class="text-sm text-gray-600 mb-1">将要应用的操作:</p>
          <p class="text-sm font-medium">
            <span v-if="clearCategory" class="text-red-600">清除所有选中提示词的分类</span>
            <span v-else class="text-blue-600">将所有选中提示词的分类设置为: {{ finalCategory }}</span>
          </p>
        </div>

        <!-- 提交按钮 -->
        <div class="flex justify-end space-x-3">
          <button
            type="button"
            @click="$emit('cancel')"
            class="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            取消
          </button>
          <button
            type="submit"
            :disabled="!canSubmit || isSubmitting"
            class="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {{ isSubmitting ? '应用中...' : '应用更改' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'

interface Props {
  selectedCount: number
  categories: string[]
}

const props = defineProps<Props>()

const emit = defineEmits<{
  submit: [category: string]
  cancel: []
}>()

const selectedCategory = ref('')
const customCategory = ref('')
const clearCategory = ref(false)
const isSubmitting = ref(false)

// 计算最终的分类值
const finalCategory = computed(() => {
  if (clearCategory.value) return ''
  return customCategory.value || selectedCategory.value
})

// 检查是否可以提交
const canSubmit = computed(() => {
  return clearCategory.value || finalCategory.value.trim() !== ''
})

// 处理自定义分类输入
const handleCustomInput = () => {
  if (customCategory.value) {
    selectedCategory.value = ''
    clearCategory.value = false
  }
}

// 处理清除分类变化
const handleClearChange = () => {
  if (clearCategory.value) {
    selectedCategory.value = ''
    customCategory.value = ''
  }
}

// 监听现有分类选择
watch(selectedCategory, (newValue) => {
  if (newValue) {
    customCategory.value = ''
    clearCategory.value = false
  }
})

const handleSubmit = async () => {
  if (!canSubmit.value) return

  try {
    isSubmitting.value = true
    emit('submit', finalCategory.value)
  } finally {
    isSubmitting.value = false
  }
}
</script>