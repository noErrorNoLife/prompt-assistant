<template>
  <div class="flex h-screen bg-gray-100">
    <div class="w-64 flex-shrink-0">
      <ProjectSidebar />
    </div>
    <div class="flex-1 flex flex-col overflow-hidden">
      <div class="flex-1 overflow-y-auto">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <!-- 页面头部 -->
          <div class="mb-8">
            <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-6">
              <div>
                <h1 class="text-3xl font-bold text-gray-900">提示词管理</h1>
                <p class="mt-1 text-sm text-gray-500">
                  管理和组织您的AI提示词
                </p>
              </div>
              <div class="mt-4 sm:mt-0 flex space-x-3">
                <button
                  @click="$router.push('/drafts')"
                  class="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                >
                  <svg class="-ml-1 mr-2 h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                  </svg>
                  写作模式
                </button>
                <button
                  @click="showImportExportModal = true"
                  class="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                >
                  <svg class="-ml-1 mr-2 h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 4H6a2 2 0 00-2 2v12a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-2m-4-1v8m0 0l3-3m0 3L9 8m-5 5h2.586a1 1 0 01.707.293l2.414 2.414a1 1 0 00.707.293H14" />
                  </svg>
                  导入/导出
                </button>
                <button
                  @click="showCreateModal = true"
                  class="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                >
                  <svg class="-ml-1 mr-2 h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                  </svg>
                  新建提示词
                </button>
              </div>
            </div>

            <!-- 搜索和过滤器 -->
            <div class="mb-6">
              <SearchBar @search="handleSearch" />
            </div>

            <!-- 批量操作工具栏 -->
            <div v-if="selectedPrompts.size > 0" class="mb-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
              <div class="flex items-center justify-between">
                <div class="flex items-center">
                  <span class="text-sm font-medium text-blue-900">
                    已选择 {{ selectedPrompts.size }} 个提示词
                  </span>
                  <button
                    @click="clearSelection"
                    class="ml-3 text-sm text-blue-600 hover:text-blue-700"
                  >
                    清除选择
                  </button>
                </div>
                <div class="flex space-x-2">
                  <button
                    @click="showBatchCategoryModal = true"
                    class="inline-flex items-center px-3 py-1 border border-blue-300 text-sm font-medium rounded-md text-blue-700 bg-white hover:bg-blue-50"
                  >
                    设置分类
                  </button>
                  <button
                    @click="showBatchTagModal = true"
                    class="inline-flex items-center px-3 py-1 border border-blue-300 text-sm font-medium rounded-md text-blue-700 bg-white hover:bg-blue-50"
                  >
                    添加标签
                  </button>
                  <button
                    @click="handleBatchExport"
                    class="inline-flex items-center px-3 py-1 border border-blue-300 text-sm font-medium rounded-md text-blue-700 bg-white hover:bg-blue-50"
                  >
                    导出选中
                  </button>
                  <button
                    @click="handleBatchDelete"
                    class="inline-flex items-center px-3 py-1 border border-red-300 text-sm font-medium rounded-md text-red-700 bg-white hover:bg-red-50"
                  >
                    批量删除
                  </button>
                </div>
              </div>
            </div>

            <!-- 视图切换和排序 -->
            <div class="flex items-center justify-between">
              <div class="flex space-x-4">
                <!-- 视图切换 -->
                <div class="flex rounded-lg border border-gray-300 bg-white">
                  <button
                    @click="currentView = 'all'"
                    :class="[
                      'px-3 py-2 text-sm font-medium rounded-l-lg',
                      currentView === 'all'
                        ? 'bg-blue-600 text-white'
                        : 'text-gray-700 hover:bg-gray-50'
                    ]"
                  >
                    全部 ({{ prompts.filter(p => !p.is_template).length }})
                  </button>
                  <button
                    @click="currentView = 'templates'"
                    :class="[
                      'px-3 py-2 text-sm font-medium border-l border-gray-300',
                      currentView === 'templates'
                        ? 'bg-blue-600 text-white'
                        : 'text-gray-700 hover:bg-gray-50'
                    ]"
                  >
                    模板 ({{ prompts.filter(p => p.is_template).length }})
                  </button>
                  <button
                    @click="currentView = 'favorites'"
                    :class="[
                      'px-3 py-2 text-sm font-medium rounded-r-lg border-l border-gray-300',
                      currentView === 'favorites'
                        ? 'bg-blue-600 text-white'
                        : 'text-gray-700 hover:bg-gray-50'
                    ]"
                  >
                    收藏 ({{ favoriteCount }})
                  </button>
                </div>

                <!-- 排序选择 -->
                <div class="flex items-center space-x-2">
                  <select
                    v-model="sortKey"
                    @change="handleSortChange"
                    class="px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  >
                    <option value="created_at_desc">按创建时间 (最新)</option>
                    <option value="created_at_asc">按创建时间 (最早)</option>
                    <option value="updated_at_desc">按修改时间 (最新)</option>
                    <option value="updated_at_asc">按修改时间 (最早)</option>
                    <option value="title_asc">按标题 (A-Z)</option>
                    <option value="title_desc">按标题 (Z-A)</option>
                    <option value="usage_count_desc">按使用次数 (多到少)</option>
                    <option value="usage_count_asc">按使用次数 (少到多)</option>
                  </select>
                </div>
              </div>

              <div class="text-sm text-gray-500">
                显示 {{ filteredPrompts.length }} 个结果
              </div>
            </div>
          </div>

          <!-- 提示词列表 -->
          <div v-if="loading" class="flex justify-center items-center py-12">
            <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          </div>

          <div v-else-if="filteredPrompts.length === 0" class="text-center py-12">
            <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            <h3 class="mt-4 text-lg font-medium text-gray-900">暂无提示词</h3>
            <p class="mt-2 text-sm text-gray-500">开始创建您的第一个提示词吧</p>
            <div class="mt-6">
              <button
                @click="showCreateModal = true"
                class="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                <svg class="-ml-1 mr-2 h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                </svg>
                创建提示词
              </button>
            </div>
          </div>

          <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <PromptCard
              v-for="prompt in filteredPrompts"
              :key="prompt.id"
              :prompt="prompt"
              :is-selected="selectedPrompts.has(prompt.id)"
              @click="handlePromptClick"
              @edit="handleEdit"
              @delete="handleDelete"
              @clone="handleClone"
              @duplicate="handleDuplicate"
              @versions="handleVersions"
              @select="handlePromptSelect"
              @openMoveToProject="handleOpenMoveToProjectModal"
            />
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- 模态框组件 -->
  <Modal :show="showCreateModal" @close="showCreateModal = false" max-width="6xl" :close-on-background-click="false">
    <PromptForm
      :is-editing="false"
      @submit="handleCreate"
      @cancel="showCreateModal = false"
    />
  </Modal>

  <Modal :show="showEditModal && !!selectedPrompt" @close="showEditModal = false" max-width="6xl" contentClass="h-[90vh]" :close-on-background-click="false">
    <PromptForm
      v-if="selectedPrompt"
      :is-editing="true"
      :prompt="selectedPrompt"
      @submit="handleUpdate"
      @cancel="showEditModal = false"
    />
  </Modal>

  <Modal :show="showVersionsModal && !!selectedPrompt" @close="showVersionsModal = false" max-width="6xl" contentClass="h-[90vh]">
    <VersionHistoryView
      v-if="selectedPrompt"
      :prompt="selectedPrompt"
      @close="showVersionsModal = false"
      @restore="handleVersionRestore"
    />
  </Modal>

  <ImportExportModal
    v-if="showImportExportModal"
    :selected-ids="Array.from(selectedPrompts)"
    :categories="categories"
    @close="showImportExportModal = false"
    @imported="handleImported"
  />

  <!-- 批量操作模态框 -->
  <Modal :show="showBatchCategoryModal" @close="showBatchCategoryModal = false">
    <BatchCategoryForm
      :selected-count="selectedPrompts.size"
      :categories="categories"
      @submit="handleBatchCategoryUpdate"
      @cancel="showBatchCategoryModal = false"
    />
  </Modal>

  <Modal :show="showBatchTagModal" @close="showBatchTagModal = false">
    <BatchTagForm
      v-if="popularTags"
      :selected-count="selectedPrompts.size"
      :popular-tags="popularTags"
      @submit="handleBatchTagAdd"
      @cancel="showBatchTagModal = false"
    />
  </Modal>
  
  <!-- 新增：预览模态框 -->
  <PromptPreviewModal
    :show="isPreviewModalOpen"
    :prompt="previewingPrompt"
    @close="closePreviewModal"
  />

  <MoveToProjectModal
    :show="showMoveToProjectModal"
    :prompt="promptToMove"
    @close="showMoveToProjectModal = false"
  />
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useMainStore } from '@/stores'
import { importExportApi } from '@/services/api'
import SearchBar from '@/components/SearchBar.vue'
import PromptCard from '@/components/PromptCard.vue'
import Modal from '@/components/Modal.vue'
import PromptForm from '@/components/PromptForm.vue'
import ImportExportModal from '@/components/ImportExportModal.vue'
import VersionHistoryView from '@/components/VersionHistoryView.vue'
import BatchCategoryForm from '@/components/BatchCategoryForm.vue'
import BatchTagForm from '@/components/BatchTagForm.vue'
import PromptPreviewModal from '@/components/PromptPreviewModal.vue'
import ProjectSidebar from '@/components/ProjectSidebar.vue'
import MoveToProjectModal from '@/components/MoveToProjectModal.vue'
import type { Prompt } from '@/stores'

const store = useMainStore()

// 响应式数据
const loading = ref(false)
const currentView = ref<'all' | 'templates' | 'favorites'>('all')
const searchQuery = ref('')
const selectedPrompts = ref(new Set<number>())
const selectedPrompt = ref<Prompt | null>(null)
const promptToMove = ref<Prompt | null>(null)

// 新增：预览模态框状态
const isPreviewModalOpen = ref(false)
const previewingPrompt = ref<Prompt | null>(null)

// 模态框状态
const showCreateModal = ref(false)
const showEditModal = ref(false)
const showVersionsModal = ref(false)
const showImportExportModal = ref(false)
const showBatchCategoryModal = ref(false)
const showBatchTagModal = ref(false)
const showMoveToProjectModal = ref(false)

// 排序状态，同步 store 的排序选项
const sortKey = computed({
  get: () => `${store.sortOptions.sortBy}_${store.sortOptions.order}`,
  set: (value: string) => {
    const [sortBy, order] = value.split('_')
    store.setSort(sortBy, order)
  }
})

// 计算属性
const prompts = computed(() => store.prompts)
const categories = computed(() => store.categories)
const popularTags = computed(() => store.tags.slice(0, 10))
const favoriteCount = computed(() => prompts.value.filter(p => store.isFavorite(p.id)).length)

const filteredPrompts = computed(() => {
  // 如果有搜索查询，使用搜索结果，否则使用所有提示词
  let filtered = searchQuery.value.trim() ? store.searchResults : prompts.value

  // 按视图过滤
  switch (currentView.value) {
    case 'templates':
      filtered = filtered.filter(p => p.is_template)
      break
    case 'favorites':
      filtered = filtered.filter(p => store.isFavorite(p.id))
      break
    default:
      filtered = filtered.filter(p => !p.is_template)
  }

  // 注意：现在排序由后端处理，这里不再需要前端排序逻辑
  return filtered
})

// 方法
const handleSortChange = async () => {
  // 排序改变时重新获取数据
  await store.fetchPrompts()
}

const handleSearch = async (query: string, searchParams?: any) => {
  searchQuery.value = query
  // 如果有搜索查询或过滤条件，使用搜索 API
  if (query.trim() || (searchParams && Object.keys(searchParams).some(key => searchParams[key]))) {
    await store.searchPrompts(searchParams || { q: query })
  } else {
    // 否则获取所有数据
    await store.fetchPrompts()
  }
}

const handlePromptClick = (prompt: Prompt) => {
  // 现在的点击行为是打开预览
  previewingPrompt.value = prompt
  isPreviewModalOpen.value = true
}

const handlePromptSelect = (prompt: Prompt, selected: boolean) => {
  if (selected) {
    selectedPrompts.value.add(prompt.id)
  } else {
    selectedPrompts.value.delete(prompt.id)
  }
}

const clearSelection = () => {
  selectedPrompts.value.clear()
}

const handleCreate = async (promptData: any) => {
  try {
    loading.value = true
    await store.addPrompt(promptData)
    showCreateModal.value = false
  } catch (error) {
    console.error('创建失败:', error)
  } finally {
    loading.value = false
  }
}

const handleEdit = (prompt: Prompt) => {
  selectedPrompt.value = prompt
  showEditModal.value = true
}

const handleUpdate = async (promptData: any) => {
  if (!selectedPrompt.value) return

  try {
    loading.value = true
    // 将更新数据合并到响应式对象中，而不是创建一个新对象
    const updatedPrompt = Object.assign(selectedPrompt.value, promptData);
    await store.updatePrompt(updatedPrompt)
    showEditModal.value = false
    selectedPrompt.value = null
  } catch (error) {
    console.error('更新失败:', error)
  } finally {
    loading.value = false
  }
}

const handleDelete = async (prompt: Prompt) => {
  if (!confirm(`确定要删除提示词"${prompt.title}"吗？`)) {
    return
  }

  try {
    loading.value = true
    await store.deletePrompt(prompt.id)
  } catch (error) {
    console.error('删除失败:', error)
  } finally {
    loading.value = false
  }
}

const handleClone = async (prompt: Prompt) => {
  // 如果是模板，使用模板克隆功能
  if (prompt.is_template) {
    // 这里可以打开模板克隆模态框
    console.log('克隆模板:', prompt.title)
  }
}

const handleDuplicate = async (prompt: Prompt) => {
  try {
    loading.value = true
    await store.addPrompt({
      title: `${prompt.title} (副本)`,
      content: prompt.content,
      category: prompt.category,
      tags: prompt.tags,
      author: prompt.author
    })
  } catch (error) {
    console.error('复制失败:', error)
  } finally {
    loading.value = false
  }
}

const handleVersions = (prompt: Prompt) => {
  selectedPrompt.value = prompt
  showVersionsModal.value = true
}

const handleVersionRestore = async (versionData: any) => {
  if (!selectedPrompt.value) return

  try {
    loading.value = true
    // 直接更新内容，不创建新版本
    await store.updatePromptContent(selectedPrompt.value.id, versionData.content)
    
    // 手动更新 selectedPrompt 的内容以在UI上即时反映
    selectedPrompt.value.content = versionData.content

    showVersionsModal.value = false
    // 不需要重置 selectedPrompt.value
    // selectedPrompt.value = null
  } catch (error) {
    console.error('从历史版本恢复失败:', error)
  } finally {
    loading.value = false
  }
}

const handleImported = async (count: number) => {
  await store.fetchPrompts()
  console.log(`成功导入 ${count} 个提示词`)
}

const handleBatchExport = () => {
  showImportExportModal.value = true
}

const handleBatchDelete = async () => {
  const count = selectedPrompts.value.size
  if (!confirm(`确定要删除选中的 ${count} 个提示词吗？此操作无法撤销。`)) {
    return
  }

  try {
    loading.value = true
    await importExportApi.batchOperation('delete', Array.from(selectedPrompts.value))
    await store.fetchPrompts()
    clearSelection()
  } catch (error) {
    console.error('批量删除失败:', error)
  } finally {
    loading.value = false
  }
}

const handleBatchCategoryUpdate = async (category: string) => {
  try {
    loading.value = true
    await importExportApi.batchOperation('update_category', Array.from(selectedPrompts.value), { category })
    await store.fetchPrompts()
    clearSelection()
    showBatchCategoryModal.value = false
  } catch (error) {
    console.error('批量更新分类失败:', error)
  } finally {
    loading.value = false
  }
}

const handleBatchTagAdd = async (tag: string) => {
  try {
    loading.value = true
    await importExportApi.batchOperation('add_tag', Array.from(selectedPrompts.value), { tag })
    await store.fetchPrompts()
    clearSelection()
    showBatchTagModal.value = false
  } catch (error) {
    console.error('批量添加标签失败:', error)
  } finally {
    loading.value = false
  }
}

const closePreviewModal = () => {
  isPreviewModalOpen.value = false
  previewingPrompt.value = null
}

const handleOpenMoveToProjectModal = (prompt: Prompt) => {
  promptToMove.value = prompt
  showMoveToProjectModal.value = true
}

// 生命周期
onMounted(async () => {
  loading.value = true
  try {
    await Promise.all([
      store.fetchPrompts(),
      store.fetchProjects()
    ])
  } catch (error) {
    console.error("加载初始数据失败:", error)
    store.error = '加载初始数据失败'
  } finally {
    loading.value = false
  }
})

// 监听视图切换，清除选择
watch(currentView, () => {
  clearSelection()
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