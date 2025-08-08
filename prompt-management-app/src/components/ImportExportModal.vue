<template>
  <div class="fixed inset-0 z-50 overflow-y-auto" @click.self="$emit('close')">
    <div class="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
      <!-- 背景遮罩 -->
      <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"></div>
      
      <!-- 模态框内容 -->
      <div class="inline-block align-bottom bg-white rounded-lg px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full sm:p-6">
        <div class="sm:flex sm:items-start">
          <div class="w-full">
            <!-- 头部 -->
            <div class="mb-6">
              <h3 class="text-lg leading-6 font-medium text-gray-900 mb-2">
                数据管理
              </h3>
              <p class="text-sm text-gray-500">
                导入或导出您的提示词数据
              </p>
            </div>

            <!-- 选项卡 -->
            <div class="mb-6">
              <div class="border-b border-gray-200">
                <nav class="-mb-px flex space-x-8">
                  <button
                    @click="activeTab = 'export'"
                    :class="[
                      'py-2 px-1 border-b-2 font-medium text-sm',
                      activeTab === 'export'
                        ? 'border-blue-500 text-blue-600'
                        : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                    ]"
                  >
                    导出数据
                  </button>
                  <button
                    @click="activeTab = 'import'"
                    :class="[
                      'py-2 px-1 border-b-2 font-medium text-sm',
                      activeTab === 'import'
                        ? 'border-blue-500 text-blue-600'
                        : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                    ]"
                  >
                    导入数据
                  </button>
                </nav>
              </div>
            </div>

            <!-- 导出面板 -->
            <div v-if="activeTab === 'export'" class="space-y-4">
              <!-- 导出格式选择 -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  导出格式
                </label>
                <div class="grid grid-cols-3 gap-3">
                  <label
                    v-for="format in exportFormats"
                    :key="format.value"
                    class="relative flex cursor-pointer rounded-lg border bg-white p-4 shadow-sm focus:outline-none"
                    :class="[
                      exportOptions.format === format.value
                        ? 'border-blue-600 ring-2 ring-blue-600'
                        : 'border-gray-300'
                    ]"
                  >
                    <input
                      v-model="exportOptions.format"
                      :value="format.value"
                      type="radio"
                      name="export-format"
                      class="sr-only"
                    />
                    <div class="flex flex-col items-center text-center">
                      <div class="text-2xl mb-2">{{ format.icon }}</div>
                      <div class="text-sm font-medium text-gray-900">{{ format.label }}</div>
                      <div class="text-xs text-gray-500">{{ format.description }}</div>
                    </div>
                  </label>
                </div>
              </div>

              <!-- 导出范围 -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  导出范围
                </label>
                <div class="space-y-2">
                  <label class="flex items-center">
                    <input
                      v-model="exportOptions.scope"
                      value="all"
                      type="radio"
                      class="mr-2 text-blue-600 focus:ring-blue-500"
                    />
                    <span class="text-sm">全部提示词</span>
                  </label>
                  <label class="flex items-center">
                    <input
                      v-model="exportOptions.scope"
                      value="category"
                      type="radio"
                      class="mr-2 text-blue-600 focus:ring-blue-500"
                    />
                    <span class="text-sm">按分类导出</span>
                  </label>
                  <label class="flex items-center">
                    <input
                      v-model="exportOptions.scope"
                      value="selected"
                      type="radio"
                      class="mr-2 text-blue-600 focus:ring-blue-500"
                    />
                    <span class="text-sm">选中的提示词 ({{ selectedIds.length }} 个)</span>
                  </label>
                </div>
              </div>

              <!-- 分类选择 -->
              <div v-if="exportOptions.scope === 'category'">
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  选择分类
                </label>
                <select
                  v-model="exportOptions.category"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                >
                  <option value="">请选择分类</option>
                  <option v-for="category in categories" :key="category" :value="category">
                    {{ category }}
                  </option>
                </select>
              </div>

              <!-- 导出按钮 -->
              <div class="pt-4">
                <button
                  @click="handleExport"
                  :disabled="isExporting || !canExport"
                  class="w-full inline-flex justify-center items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200"
                >
                  <svg v-if="isExporting" class="animate-spin -ml-1 mr-3 h-4 w-4" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  <svg v-else class="mr-2 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  {{ isExporting ? '导出中...' : '开始导出' }}
                </button>
              </div>
            </div>

            <!-- 导入面板 -->
            <div v-if="activeTab === 'import'" class="space-y-4">
              <!-- 文件选择区域 -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  选择文件
                </label>
                <div
                  class="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 border-dashed rounded-md hover:border-gray-400 transition-colors duration-200"
                  :class="{ 'border-blue-400 bg-blue-50': isDragOver }"
                  @drop="handleFileDrop"
                  @dragover.prevent="isDragOver = true"
                  @dragleave="isDragOver = false"
                >
                  <div class="space-y-1 text-center">
                    <svg class="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48">
                      <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                    </svg>
                    <div class="flex text-sm text-gray-600">
                      <label class="relative cursor-pointer bg-white rounded-md font-medium text-blue-600 hover:text-blue-500 focus-within:outline-none focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-blue-500">
                        <span>选择文件</span>
                        <input
                          ref="fileInput"
                          type="file"
                          accept=".json,.csv"
                          class="sr-only"
                          @change="handleFileSelect"
                        />
                      </label>
                      <p class="pl-1">或拖拽文件到此处</p>
                    </div>
                    <p class="text-xs text-gray-500">
                      支持 JSON、CSV 格式文件
                    </p>
                  </div>
                </div>
              </div>

              <!-- 选中的文件信息 -->
              <div v-if="selectedFile" class="bg-gray-50 rounded-lg p-4">
                <div class="flex items-center">
                  <svg class="h-8 w-8 text-blue-500 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  <div class="flex-1">
                    <h4 class="text-sm font-medium text-gray-900">{{ selectedFile.name }}</h4>
                    <p class="text-sm text-gray-500">{{ formatFileSize(selectedFile.size) }}</p>
                  </div>
                  <button
                    @click="clearSelectedFile"
                    class="text-gray-400 hover:text-gray-600"
                  >
                    <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                </div>
              </div>

              <!-- 导入选项 -->
              <div v-if="selectedFile">
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  导入选项
                </label>
                <div class="space-y-2">
                  <label class="flex items-center">
                    <input
                      v-model="importOptions.skipDuplicates"
                      type="checkbox"
                      class="mr-2 text-blue-600 focus:ring-blue-500"
                    />
                    <span class="text-sm">跳过重复的提示词</span>
                  </label>
                  <label class="flex items-center">
                    <input
                      v-model="importOptions.overwriteExisting"
                      type="checkbox"
                      class="mr-2 text-blue-600 focus:ring-blue-500"
                    />
                    <span class="text-sm">覆盖已存在的提示词</span>
                  </label>
                </div>
              </div>

              <!-- 导入按钮 -->
              <div v-if="selectedFile" class="pt-4">
                <button
                  @click="handleImport"
                  :disabled="isImporting"
                  class="w-full inline-flex justify-center items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200"
                >
                  <svg v-if="isImporting" class="animate-spin -ml-1 mr-3 h-4 w-4" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  <svg v-else class="mr-2 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M9 19l3 3m0 0l3-3m-3 3V10" />
                  </svg>
                  {{ isImporting ? '导入中...' : '开始导入' }}
                </button>
              </div>
            </div>

            <!-- 操作结果显示 -->
            <div v-if="operationResult" class="mt-6 p-4 rounded-lg" :class="[
              operationResult.type === 'success' ? 'bg-green-50 border border-green-200' : 'bg-red-50 border border-red-200'
            ]">
              <div class="flex">
                <div class="flex-shrink-0">
                  <svg v-if="operationResult.type === 'success'" class="h-5 w-5 text-green-400" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                  </svg>
                  <svg v-else class="h-5 w-5 text-red-400" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
                  </svg>
                </div>
                <div class="ml-3">
                  <h3 class="text-sm font-medium" :class="[
                    operationResult.type === 'success' ? 'text-green-800' : 'text-red-800'
                  ]">
                    {{ operationResult.title }}
                  </h3>
                  <div class="mt-2 text-sm" :class="[
                    operationResult.type === 'success' ? 'text-green-700' : 'text-red-700'
                  ]">
                    <p>{{ operationResult.message }}</p>
                    <div v-if="operationResult.details" class="mt-2 space-y-1">
                      <div v-for="detail in operationResult.details" :key="detail">
                        {{ detail }}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- 底部按钮 -->
            <div class="mt-6 flex justify-end">
              <button
                @click="$emit('close')"
                class="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors duration-200"
              >
                关闭
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { importExportApi } from '@/services/api'
import { useMainStore } from '@/stores'

interface Props {
  selectedIds?: number[]
  categories?: string[]
}

const props = withDefaults(defineProps<Props>(), {
  selectedIds: () => [],
  categories: () => []
})

const emit = defineEmits<{
  close: []
  imported: [count: number]
}>()

const store = useMainStore()

// 响应式数据
const activeTab = ref<'export' | 'import'>('export')
const isExporting = ref(false)
const isImporting = ref(false)
const isDragOver = ref(false)
const selectedFile = ref<File | null>(null)
const fileInput = ref<HTMLInputElement>()
const operationResult = ref<{
  type: 'success' | 'error'
  title: string
  message: string
  details?: string[]
} | null>(null)

// 导出选项
const exportOptions = ref({
  format: 'json' as 'json' | 'csv' | 'markdown',
  scope: 'all' as 'all' | 'category' | 'selected',
  category: ''
})

// 导入选项
const importOptions = ref({
  skipDuplicates: true,
  overwriteExisting: false
})

// 导出格式配置
const exportFormats = [
  {
    value: 'json',
    label: 'JSON',
    description: '结构化数据',
    icon: '📄'
  },
  {
    value: 'csv',
    label: 'CSV',
    description: '表格格式',
    icon: '📊'
  },
  {
    value: 'markdown',
    label: 'Markdown',
    description: '文档格式',
    icon: '📝'
  }
]

// 计算属性
const canExport = computed(() => {
  if (exportOptions.value.scope === 'category' && !exportOptions.value.category) {
    return false
  }
  if (exportOptions.value.scope === 'selected' && props.selectedIds.length === 0) {
    return false
  }
  return true
})

// 方法
const handleExport = async () => {
  try {
    isExporting.value = true
    operationResult.value = null

    const params: any = {
      format: exportOptions.value.format
    }

    if (exportOptions.value.scope === 'category') {
      params.category = exportOptions.value.category
    } else if (exportOptions.value.scope === 'selected') {
      params.ids = props.selectedIds
    }

    const blob = await importExportApi.exportPrompts(params)
    
    // 下载文件
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `prompts_${new Date().toISOString().split('T')[0]}.${exportOptions.value.format}`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)

    operationResult.value = {
      type: 'success',
      title: '导出成功',
      message: '提示词数据已成功导出到您的下载文件夹'
    }

  } catch (error) {
    console.error('导出失败:', error)
    operationResult.value = {
      type: 'error',
      title: '导出失败',
      message: error instanceof Error ? error.message : '未知错误'
    }
  } finally {
    isExporting.value = false
  }
}

const handleFileSelect = (event: Event) => {
  const target = event.target as HTMLInputElement
  if (target.files && target.files[0]) {
    selectedFile.value = target.files[0]
    operationResult.value = null
  }
}

const handleFileDrop = (event: DragEvent) => {
  event.preventDefault()
  isDragOver.value = false
  
  if (event.dataTransfer?.files && event.dataTransfer.files[0]) {
    selectedFile.value = event.dataTransfer.files[0]
    operationResult.value = null
  }
}

const clearSelectedFile = () => {
  selectedFile.value = null
  if (fileInput.value) {
    fileInput.value.value = ''
  }
  operationResult.value = null
}

const handleImport = async () => {
  if (!selectedFile.value) return

  try {
    isImporting.value = true
    operationResult.value = null

    const result = await importExportApi.importPrompts(selectedFile.value)

    operationResult.value = {
      type: 'success',
      title: '导入完成',
      message: '提示词数据已成功导入',
      details: [
        `导入成功: ${result.imported_count} 个`,
        `跳过重复: ${result.skipped_count} 个`,
        `总计处理: ${result.total_processed} 个`
      ]
    }

    if (result.errors && result.errors.length > 0) {
      operationResult.value.details!.push(`错误: ${result.errors.length} 个`)
    }

    // 通知父组件刷新数据
    emit('imported', result.imported_count)

    // 清空文件选择
    clearSelectedFile()

  } catch (error) {
    console.error('导入失败:', error)
    operationResult.value = {
      type: 'error',
      title: '导入失败',
      message: error instanceof Error ? error.message : '未知错误'
    }
  } finally {
    isImporting.value = false
  }
}

const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

// 组件挂载时获取分类数据
onMounted(() => {
  // 如果没有传入categories，从store获取
  if (props.categories.length === 0) {
    // 这里可以触发获取分类数据
  }
})
</script>

<style scoped>
/* 拖拽动画效果 */
.border-dashed {
  transition: all 0.2s ease-in-out;
}

/* 文件拖拽悬浮效果 */
.border-blue-400 {
  background-color: rgba(59, 130, 246, 0.05);
}

/* 选项卡切换动画 */
.border-b-2 {
  transition: all 0.2s ease-in-out;
}

/* 加载动画 */
@keyframes spin {
  to { transform: rotate(360deg); }
}

.animate-spin {
  animation: spin 1s linear infinite;
}
</style>