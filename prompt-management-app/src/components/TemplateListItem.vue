<template>
  <div class="hover:bg-gray-50 transition-colors duration-200 p-6">
    <div class="flex items-center justify-between">
      <div class="flex-1 min-w-0">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="h-10 w-10 bg-gradient-to-r from-yellow-400 to-orange-500 rounded-lg flex items-center justify-center">
              <svg class="h-6 w-6 text-white" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
              </svg>
            </div>
          </div>
          <div class="ml-4 flex-1">
            <div class="flex items-center">
              <h3 class="text-lg font-medium text-gray-900">{{ template.title }}</h3>
              <span v-if="template.rating && template.rating > 0" class="ml-2 inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
                <svg class="h-3 w-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                </svg>
                {{ template.rating.toFixed(1) }}
              </span>
            </div>
            <p class="text-sm text-gray-500 mt-1 line-clamp-2">{{ template.content }}</p>
            <div class="mt-2 flex items-center text-sm text-gray-500">
              <span class="flex items-center">
                <svg class="h-4 w-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
                {{ template.usage_count || 0 }} 次使用
              </span>
              <span v-if="template.category" class="ml-4 flex items-center">
                <svg class="h-4 w-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
                </svg>
                {{ template.category }}
              </span>
            </div>
          </div>
        </div>
      </div>
      <div class="flex items-center space-x-2">
        <button
          @click="$emit('clone', template)"
          class="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
        >
          使用模板
        </button>
        <button
          @click="$emit('edit', template)"
          class="inline-flex items-center px-3 py-2 border border-gray-300 text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
        >
          编辑
        </button>
        <button
          @click="$emit('delete', template)"
          class="inline-flex items-center px-3 py-2 border border-gray-300 text-sm leading-4 font-medium rounded-md text-red-700 bg-white hover:bg-red-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
        >
          删除
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Prompt } from '@/stores'

interface Props {
  template: Prompt
}

defineProps<Props>()

defineEmits<{
  clone: [template: Prompt]
  edit: [template: Prompt]
  delete: [template: Prompt]
}>()
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>