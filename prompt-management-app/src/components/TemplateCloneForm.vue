<template>
  <div class="max-w-4xl mx-auto">
    <div class="bg-white rounded-lg shadow-lg overflow-hidden">
      <!-- 头部 -->
      <div class="bg-gradient-to-r from-blue-600 to-purple-600 px-6 py-4">
        <h2 class="text-xl font-bold text-white flex items-center">
          <svg class="h-6 w-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
          使用模板: {{ template.title }}
        </h2>
        <p class="text-blue-100 text-sm mt-1">自定义变量值并生成个性化内容</p>
      </div>

      <div class="p-6">
        <!-- 模板预览 -->
        <div class="mb-6">
          <h3 class="text-lg font-medium text-gray-900 mb-3">模板预览</h3>
          <div class="bg-gray-50 rounded-lg p-4 border">
            <pre class="whitespace-pre-wrap text-sm text-gray-700 font-mono">{{ previewContent }}</pre>
          </div>
        </div>

        <!-- 变量配置 -->
        <div v-if="templateVariables.length" class="mb-6">
          <h3 class="text-lg font-medium text-gray-900 mb-3">自定义变量</h3>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div
              v-for="variable in templateVariables"
              :key="variable.name"
              class="border border-gray-200 rounded-lg p-4 hover:border-blue-300 transition-colors duration-200"
            >
              <label class="block text-sm font-medium text-gray-700 mb-2">
                {{ variable.name }}
                <span v-if="variable.is_required" class="text-red-500">*</span>
              </label>
              
              <p v-if="variable.description" class="text-xs text-gray-500 mb-2">
                {{ variable.description }}
              </p>

              <!-- 文本输入 -->
              <input
                v-if="variable.type === 'text'"
                v-model="variableValues[variable.name]"
                type="text"
                :placeholder="variable.default_value"
                :required="variable.is_required"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm"
              />

              <!-- 数字输入 -->
              <input
                v-else-if="variable.type === 'number'"
                v-model.number="variableValues[variable.name]"
                type="number"
                :placeholder="variable.default_value"
                :required="variable.is_required"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm"
              />

              <!-- 多行文本 -->
              <textarea
                v-else-if="variable.type === 'textarea'"
                v-model="variableValues[variable.name]"
                :placeholder="variable.default_value"
                :required="variable.is_required"
                rows="3"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm resize-vertical"
              ></textarea>

              <!-- 选择框 -->
              <select
                v-else-if="variable.type === 'select'"
                v-model="variableValues[variable.name]"
                :required="variable.is_required"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm"
              >
                <option value="">请选择...</option>
                <option
                  v-for="option in variable.options"
                  :key="option"
                  :value="option"
                >
                  {{ option }}
                </option>
              </select>

              <!-- 默认值显示 -->
              <div v-if="variable.default_value" class="mt-1 text-xs text-gray-500">
                默认值: {{ variable.default_value }}
              </div>
            </div>
          </div>
        </div>

        <!-- 生成配置 -->
        <div class="mb-6">
          <h3 class="text-lg font-medium text-gray-900 mb-3">生成设置</h3>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                标题
              </label>
              <input
                v-model="formData.title"
                type="text"
                placeholder="为生成的内容设置标题"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                作者
              </label>
              <input
                v-model="formData.author"
                type="text"
                placeholder="您的名字"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
          </div>
        </div>

        <!-- 实时预览 -->
        <div class="mb-6">
          <h3 class="text-lg font-medium text-gray-900 mb-3 flex items-center">
            <svg class="h-5 w-5 mr-2 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
            </svg>
            实时预览
          </h3>
          <div class="bg-green-50 border border-green-200 rounded-lg p-4">
            <pre class="whitespace-pre-wrap text-sm text-gray-800 font-mono leading-relaxed">{{ generatedContent }}</pre>
          </div>
        </div>

        <!-- 操作按钮 -->
        <div class="flex items-center justify-between pt-6 border-t border-gray-200">
          <div class="flex space-x-3">
            <button
              @click="resetForm"
              type="button"
              class="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors duration-200"
            >
              <svg class="h-4 w-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              重置
            </button>
            
            <button
              @click="copyGenerated"
              type="button"
              class="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors duration-200"
            >
              <svg class="h-4 w-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
              </svg>
              复制内容
            </button>
          </div>

          <div class="flex space-x-3">
            <button
              @click="$emit('cancel')"
              type="button"
              class="inline-flex items-center px-6 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors duration-200"
            >
              取消
            </button>
            
            <button
              @click="handleSubmit"
              :disabled="!isValid || isSubmitting"
              type="button"
              class="inline-flex items-center px-6 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200"
            >
              <svg v-if="isSubmitting" class="animate-spin -ml-1 mr-2 h-4 w-4" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              {{ isSubmitting ? '创建中...' : '创建提示词' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, watch, onMounted } from 'vue'
import type { Prompt, TemplateVariable } from '@/services/api'

interface Props {
  template: Prompt
}

const props = defineProps<Props>()

const emit = defineEmits<{
  submit: [data: {
    title: string
    variables: Record<string, any>
    author: string
  }]
  cancel: []
}>()

// 响应式数据
const isSubmitting = ref(false)
const variableValues = reactive<Record<string, any>>({})
const formData = reactive({
  title: '',
  author: ''
})

// 计算属性
const templateVariables = computed((): TemplateVariable[] => {
  if (!props.template.template_variables) return []
  return Array.isArray(props.template.template_variables) 
    ? props.template.template_variables 
    : []
})

const previewContent = computed(() => {
  return props.template.content
})

const generatedContent = computed(() => {
  let content = props.template.content
  
  // 替换所有变量
  templateVariables.value.forEach(variable => {
    const value = variableValues[variable.name] || variable.default_value || `{${variable.name}}`
    const pattern = new RegExp(`\\{\\{${variable.name}\\}\\}`, 'g')
    content = content.replace(pattern, String(value))
  })
  
  return content
})

const isValid = computed(() => {
  // 检查必需变量是否已填写
  return templateVariables.value.every(variable => {
    if (variable.is_required) {
      const value = variableValues[variable.name]
      return value !== undefined && value !== null && value !== ''
    }
    return true
  })
})

// 方法
const resetForm = () => {
  // 重置变量值为默认值
  templateVariables.value.forEach(variable => {
    if (variable.default_value) {
      variableValues[variable.name] = variable.default_value
    } else {
      delete variableValues[variable.name]
    }
  })
  
  // 重置表单数据
  formData.title = `${props.template.title} (副本)`
  formData.author = ''
}

const copyGenerated = async () => {
  try {
    await navigator.clipboard.writeText(generatedContent.value)
    showSuccessMessage('内容已复制到剪贴板')
  } catch (error) {
    console.error('复制失败:', error)
    // 降级方案
    const textArea = document.createElement('textarea')
    textArea.value = generatedContent.value
    document.body.appendChild(textArea)
    textArea.select()
    document.execCommand('copy')
    document.body.removeChild(textArea)
    showSuccessMessage('内容已复制到剪贴板')
  }
}

const handleSubmit = async () => {
  if (!isValid.value) return

  try {
    isSubmitting.value = true
    
    const submitData = {
      title: formData.title || `${props.template.title} (副本)`,
      variables: { ...variableValues },
      author: formData.author
    }
    
    emit('submit', submitData)
  } catch (error) {
    console.error('提交失败:', error)
  } finally {
    isSubmitting.value = false
  }
}

const showSuccessMessage = (message: string) => {
  // 这里可以集成全局消息提示组件
  console.log(message)
}

// 监听模板变化，初始化变量值
watch(() => props.template, (newTemplate) => {
  if (newTemplate) {
    resetForm()
  }
}, { immediate: true })

// 组件挂载时初始化
onMounted(() => {
  resetForm()
})
</script>

<style scoped>
/* 动画效果 */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

/* 变量配置卡片悬浮效果 */
.border:hover {
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.1);
}

/* 实时预览区域样式 */
.bg-green-50 {
  background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
}

/* 代码字体优化 */
.font-mono {
  font-family: 'SF Mono', 'Monaco', 'Inconsolata', 'Roboto Mono', 'Source Code Pro', monospace;
  line-height: 1.6;
}

/* 滚动条样式 */
.overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>