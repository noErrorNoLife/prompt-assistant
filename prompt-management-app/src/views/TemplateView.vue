<template>
  <div class="min-h-screen bg-gray-50">
    <!-- 页面头部 -->
    <div class="bg-white shadow-sm border-b">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="py-6">
          <div class="md:flex md:items-center md:justify-between">
            <div class="flex-1 min-w-0">
              <h1 class="text-2xl font-bold leading-7 text-gray-900 sm:text-3xl sm:truncate">
                模板市场
              </h1>
              <p class="mt-1 text-sm text-gray-500">
                浏览和使用高质量的提示词模板，快速创建个性化内容
              </p>
            </div>
            <div class="mt-4 flex md:mt-0 md:ml-4">
              <button
                @click="showCreateModal = true"
                class="ml-3 inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors duration-200"
              >
                <svg class="-ml-1 mr-2 h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                </svg>
                创建模板
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 主要内容 -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- 搜索和过滤器 -->
      <div class="mb-8">
        <SearchBar
          placeholder="搜索模板..."
          @search="handleSearch"
        />
      </div>

      <!-- 模板统计 -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div class="w-8 h-8 bg-blue-500 rounded-md flex items-center justify-center">
                  <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                </div>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">总模板数</dt>
                  <dd class="text-lg font-medium text-gray-900">{{ templates.length }}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div class="w-8 h-8 bg-green-500 rounded-md flex items-center justify-center">
                  <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                </div>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">总使用次数</dt>
                  <dd class="text-lg font-medium text-gray-900">{{ totalUsage }}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div class="w-8 h-8 bg-yellow-500 rounded-md flex items-center justify-center">
                  <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                  </svg>
                </div>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">平均评分</dt>
                  <dd class="text-lg font-medium text-gray-900">{{ averageRating.toFixed(1) }}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div class="w-8 h-8 bg-purple-500 rounded-md flex items-center justify-center">
                  <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
                  </svg>
                </div>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">分类数量</dt>
                  <dd class="text-lg font-medium text-gray-900">{{ categories.length }}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 分类过滤标签 -->
      <div class="mb-6">
        <div class="flex flex-wrap gap-2">
          <button
            @click="selectedCategory = ''"
            :class="[
              'px-3 py-1 rounded-full text-sm font-medium transition-colors duration-200',
              selectedCategory === '' 
                ? 'bg-blue-600 text-white' 
                : 'bg-white text-gray-700 border border-gray-300 hover:bg-gray-50'
            ]"
          >
            全部
          </button>
          <button
            v-for="category in categories"
            :key="category"
            @click="selectedCategory = category"
            :class="[
              'px-3 py-1 rounded-full text-sm font-medium transition-colors duration-200',
              selectedCategory === category 
                ? 'bg-blue-600 text-white' 
                : 'bg-white text-gray-700 border border-gray-300 hover:bg-gray-50'
            ]"
          >
            {{ category }}
          </button>
        </div>
      </div>

      <!-- 排序选项 -->
      <div class="flex justify-between items-center mb-6">
        <div class="flex space-x-4">
          <select
            v-model="sortBy"
            class="px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          >
            <option value="usage">按使用次数排序</option>
            <option value="rating">按评分排序</option>
            <option value="created">按创建时间排序</option>
            <option value="title">按标题排序</option>
          </select>
          <select
            v-model="viewMode"
            class="px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          >
            <option value="grid">网格视图</option>
            <option value="list">列表视图</option>
          </select>
        </div>
        <div class="text-sm text-gray-500">
          显示 {{ filteredTemplates.length }} 个模板
        </div>
      </div>

      <!-- 模板列表 -->
      <div v-if="loading" class="flex justify-center items-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>

      <div v-else-if="filteredTemplates.length === 0" class="text-center py-12">
        <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
        <h3 class="mt-4 text-lg font-medium text-gray-900">暂无模板</h3>
        <p class="mt-2 text-sm text-gray-500">开始创建您的第一个模板吧</p>
        <div class="mt-6">
          <button
            @click="showCreateModal = true"
            class="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            <svg class="-ml-1 mr-2 h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
            创建模板
          </button>
        </div>
      </div>

      <!-- 网格视图 -->
      <div
        v-else-if="viewMode === 'grid'"
        class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
      >
        <TemplateCard
          v-for="template in filteredTemplates"
          :key="template.id"
          :template="template"
          @clone="handleClone"
          @edit="handleEdit"
          @delete="handleDelete"
        />
      </div>

      <!-- 列表视图 -->
      <div v-else class="bg-white shadow overflow-hidden sm:rounded-md">
        <ul class="divide-y divide-gray-200">
          <li v-for="template in filteredTemplates" :key="template.id">
            <TemplateListItem
              :template="template"
              @clone="handleClone"
              @edit="handleEdit"
              @delete="handleDelete"
            />
          </li>
        </ul>
      </div>
    </div>

    <!-- 创建模板模态框 -->
    <Modal v-if="showCreateModal" @close="showCreateModal = false">
      <TemplateForm
        :is-editing="false"
        @submit="handleCreate"
        @cancel="showCreateModal = false"
      />
    </Modal>

    <!-- 编辑模板模态框 -->
    <Modal v-if="showEditModal && selectedTemplate" @close="showEditModal = false">
      <TemplateForm
        :is-editing="true"
        :template="selectedTemplate"
        @submit="handleUpdate"
        @cancel="showEditModal = false"
      />
    </Modal>

    <!-- 克隆模板模态框 -->
    <Modal v-if="showCloneModal && selectedTemplate" @close="showCloneModal = false">
      <TemplateCloneForm
        :template="selectedTemplate"
        @submit="handleCloneSubmit"
        @cancel="showCloneModal = false"
      />
    </Modal>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useMainStore } from '@/stores'
import SearchBar from '@/components/SearchBar.vue'
import Modal from '@/components/Modal.vue'
import TemplateCard from '@/components/TemplateCard.vue'
import TemplateListItem from '@/components/TemplateListItem.vue'
import TemplateForm from '@/components/TemplateForm.vue'
import TemplateCloneForm from '@/components/TemplateCloneForm.vue'
import type { Prompt } from '@/stores'

const store = useMainStore()

// 响应式数据
const loading = ref(false)
const selectedCategory = ref('')
const sortBy = ref('usage')
const viewMode = ref('grid')
const searchQuery = ref('')
const showCreateModal = ref(false)
const showEditModal = ref(false)
const showCloneModal = ref(false)
const selectedTemplate = ref<Prompt | null>(null)

// 计算属性
const templates = computed(() => store.templates)

const categories = computed(() => {
  const categorySet = new Set<string>()
  templates.value.forEach(template => {
    if (template.category) {
      categorySet.add(template.category)
    }
  })
  return Array.from(categorySet).sort()
})

const totalUsage = computed(() => {
  return templates.value.reduce((sum, template) => sum + (template.usage_count || 0), 0)
})

const averageRating = computed(() => {
  const templatesWithRating = templates.value.filter(t => t.rating && t.rating > 0)
  if (templatesWithRating.length === 0) return 0
  const sum = templatesWithRating.reduce((sum, template) => sum + (template.rating || 0), 0)
  return sum / templatesWithRating.length
})

const filteredTemplates = computed(() => {
  let filtered = templates.value

  // 按分类过滤
  if (selectedCategory.value) {
    filtered = filtered.filter(template => template.category === selectedCategory.value)
  }

  // 按搜索关键词过滤
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(template =>
      template.title.toLowerCase().includes(query) ||
      template.content.toLowerCase().includes(query) ||
      (template.tags && template.tags.toLowerCase().includes(query))
    )
  }

  // 排序
  return filtered.slice().sort((a, b) => {
    switch (sortBy.value) {
      case 'usage':
        return (b.usage_count || 0) - (a.usage_count || 0)
      case 'rating':
        return (b.rating || 0) - (a.rating || 0)
      case 'created':
        return new Date(b.created_at || '').getTime() - new Date(a.created_at || '').getTime()
      case 'title':
        return a.title.localeCompare(b.title)
      default:
        return 0
    }
  })
})

// 方法
const handleSearch = (query: string) => {
  searchQuery.value = query
}

const handleCreate = async (templateData: any) => {
  try {
    loading.value = true
    await store.addPrompt({
      ...templateData,
      is_template: true
    })
    showCreateModal.value = false
    await store.fetchTemplates()
  } catch (error) {
    console.error('创建模板失败:', error)
  } finally {
    loading.value = false
  }
}

const handleEdit = (template: Prompt) => {
  selectedTemplate.value = template
  showEditModal.value = true
}

const handleUpdate = async (templateData: any) => {
  if (!selectedTemplate.value) return

  try {
    loading.value = true
    await store.updatePrompt({
      ...selectedTemplate.value,
      ...templateData
    })
    showEditModal.value = false
    selectedTemplate.value = null
    await store.fetchTemplates()
  } catch (error) {
    console.error('更新模板失败:', error)
  } finally {
    loading.value = false
  }
}

const handleClone = (template: Prompt) => {
  selectedTemplate.value = template
  showCloneModal.value = true
}

const handleCloneSubmit = async (cloneData: any) => {
  if (!selectedTemplate.value) return

  try {
    loading.value = true
    await store.cloneTemplate(selectedTemplate.value.id, cloneData)
    showCloneModal.value = false
    selectedTemplate.value = null
  } catch (error) {
    console.error('克隆模板失败:', error)
  } finally {
    loading.value = false
  }
}

const handleDelete = async (template: Prompt) => {
  if (!confirm('确定要删除这个模板吗？这个操作无法撤销。')) {
    return
  }

  try {
    loading.value = true
    await store.deletePrompt(template.id)
    await store.fetchTemplates()
  } catch (error) {
    console.error('删除模板失败:', error)
  } finally {
    loading.value = false
  }
}

// 生命周期
onMounted(async () => {
  loading.value = true
  try {
    await store.fetchTemplates()
  } catch (error) {
    console.error('获取模板列表失败:', error)
  } finally {
    loading.value = false
  }
})

// 监听排序变化
watch([sortBy, selectedCategory], () => {
  // 触发重新计算 filteredTemplates
})
</script>

<style scoped>
/* 页面特定样式 */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>