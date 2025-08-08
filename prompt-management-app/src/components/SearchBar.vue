<template>
  <div class="relative w-full max-w-2xl mx-auto">
    <!-- 搜索框 -->
    <div class="relative">
      <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
        <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
      </div>
      <input
        v-model="searchQuery"
        @input="handleSearch"
        @focus="showFilters = true"
        @keydown.escape="clearSearch"
        type="text"
        class="block w-full pl-10 pr-12 py-3 border border-gray-300 rounded-lg leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200"
        :placeholder="placeholder"
      />
      <div class="absolute inset-y-0 right-0 flex items-center">
        <button
          v-if="searchQuery"
          @click="clearSearch"
          class="p-2 text-gray-400 hover:text-gray-600 transition-colors duration-200"
        >
          <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
        <button
          @click="showFilters = !showFilters"
          :class="[
            'p-2 text-gray-400 hover:text-gray-600 transition-colors duration-200',
            showFilters ? 'text-blue-600' : ''
          ]"
        >
          <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 100 4m0-4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 100 4m0-4v2m0-6V4" />
          </svg>
        </button>
      </div>
    </div>

    <!-- 高级过滤器 -->
    <transition
      enter-active-class="transition ease-out duration-200"
      enter-from-class="transform opacity-0 scale-95"
      enter-to-class="transform opacity-100 scale-100"
      leave-active-class="transition ease-in duration-150"
      leave-from-class="transform opacity-100 scale-100"
      leave-to-class="transform opacity-0 scale-95"
    >
      <div v-if="showFilters" class="absolute z-10 w-full mt-2 bg-white rounded-lg shadow-lg border border-gray-200 p-4">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <!-- 分类过滤 -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">分类</label>
            <select
              v-model="filters.category"
              @change="handleSearch"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="">所有分类</option>
              <option v-for="category in categories" :key="category" :value="category">
                {{ category }}
              </option>
            </select>
          </div>

          <!-- 标签过滤 -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">标签</label>
            <div class="relative">
              <input
                v-model="filters.tags"
                @input="handleSearch"
                type="text"
                placeholder="输入标签..."
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
              <div v-if="popularTags.length" class="absolute z-20 w-full mt-1 bg-white border border-gray-200 rounded-md shadow-lg max-h-32 overflow-y-auto">
                <button
                  v-for="tag in popularTags"
                  :key="tag.name"
                  @click="selectTag(tag.name)"
                  class="w-full text-left px-3 py-2 hover:bg-gray-50 flex items-center justify-between"
                >
                  <span class="text-sm">{{ tag.name }}</span>
                  <span class="text-xs text-gray-500">{{ tag.usage_count }}</span>
                </button>
              </div>
            </div>
          </div>

          <!-- 类型过滤 -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">类型</label>
            <div class="space-y-2">
              <label class="flex items-center">
                <input
                  v-model="filters.showAll"
                  @change="handleFilterChange"
                  type="radio"
                  name="type"
                  value="all"
                  class="mr-2 text-blue-600 focus:ring-blue-500"
                />
                <span class="text-sm">全部</span>
              </label>
              <label class="flex items-center">
                <input
                  v-model="filters.showTemplatesOnly"
                  @change="handleFilterChange"
                  type="radio"
                  name="type"
                  value="templates"
                  class="mr-2 text-blue-600 focus:ring-blue-500"
                />
                <span class="text-sm">仅模板</span>
              </label>
              <label class="flex items-center">
                <input
                  v-model="filters.showPromptsOnly"
                  @change="handleFilterChange"
                  type="radio"
                  name="type"
                  value="prompts"
                  class="mr-2 text-blue-600 focus:ring-blue-500"
                />
                <span class="text-sm">仅提示词</span>
              </label>
            </div>
          </div>
        </div>

        <!-- 快速操作 -->
        <div class="mt-4 pt-4 border-t border-gray-200 flex justify-between items-center">
          <div class="flex space-x-2">
            <button
              @click="clearFilters"
              class="px-3 py-1 text-sm text-gray-600 hover:text-gray-800 transition-colors duration-200"
            >
              清空筛选
            </button>
          </div>
          <div class="text-sm text-gray-500">
            {{ searchResults.length }} 个结果
          </div>
        </div>
      </div>
    </transition>

    <!-- 搜索建议 -->
    <transition
      enter-active-class="transition ease-out duration-200"
      enter-from-class="transform opacity-0 scale-95"
      enter-to-class="transform opacity-100 scale-100"
      leave-active-class="transition ease-in duration-150"
      leave-from-class="transform opacity-100 scale-100"
      leave-to-class="transform opacity-0 scale-95"
    >
      <div v-if="showSuggestions && suggestions.length" class="absolute z-10 w-full mt-2 bg-white rounded-lg shadow-lg border border-gray-200 max-h-64 overflow-y-auto">
        <div class="p-2">
          <div class="text-xs text-gray-500 px-3 py-2 border-b">搜索建议</div>
          <button
            v-for="(suggestion, index) in suggestions"
            :key="index"
            @click="selectSuggestion(suggestion)"
            class="w-full text-left px-3 py-2 hover:bg-gray-50 rounded-md transition-colors duration-150"
          >
            <div class="flex items-center">
              <svg class="h-4 w-4 text-gray-400 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
              <span class="text-sm">{{ suggestion }}</span>
            </div>
          </button>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import { useMainStore } from '@/stores'
import type { Tag } from '@/services/api'

interface Props {
  placeholder?: string
  autoFocus?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  placeholder: '搜索提示词、模板...',
  autoFocus: false
})

const emit = defineEmits<{
  search: [query: string, filters: SearchFilters]
}>()

interface SearchFilters {
  category: string
  tags: string
  showAll: boolean
  showTemplatesOnly: boolean
  showPromptsOnly: boolean
}

const store = useMainStore()

const searchQuery = ref('')
const showFilters = ref(false)
const showSuggestions = ref(false)
const filters = ref<SearchFilters>({
  category: '',
  tags: '',
  showAll: true,
  showTemplatesOnly: false,
  showPromptsOnly: false
})

const suggestions = ref<string[]>([
  '编程相关',
  '文案写作', 
  '数据分析',
  '创意设计',
  '教育培训',
  '商务沟通'
])

// 计算属性
const categories = computed(() => store.categories)
const popularTags = computed(() => store.tags.slice(0, 10))
const searchResults = computed(() => store.searchResults)

// 搜索处理
const handleSearch = () => {
  const searchParams = {
    q: searchQuery.value,
    category: filters.value.category,
    tags: filters.value.tags,
    is_template: filters.value.showTemplatesOnly ? true : 
                 filters.value.showPromptsOnly ? false : undefined
  }

  emit('search', searchQuery.value, searchParams)
  showSuggestions.value = false
}

// 过滤器变化处理
const handleFilterChange = () => {
  // 确保单选逻辑
  if (filters.value.showTemplatesOnly) {
    filters.value.showAll = false
    filters.value.showPromptsOnly = false
  } else if (filters.value.showPromptsOnly) {
    filters.value.showAll = false
    filters.value.showTemplatesOnly = false
  } else {
    filters.value.showAll = true
  }
  handleSearch()
}

// 清空搜索
const clearSearch = () => {
  searchQuery.value = ''
  handleSearch()
}

// 清空过滤器
const clearFilters = () => {
  filters.value = {
    category: '',
    tags: '',
    showAll: true,
    showTemplatesOnly: false,
    showPromptsOnly: false
  }
  handleSearch()
}

// 选择标签
const selectTag = (tagName: string) => {
  if (filters.value.tags) {
    filters.value.tags += `, ${tagName}`
  } else {
    filters.value.tags = tagName
  }
  handleSearch()
}

// 选择搜索建议
const selectSuggestion = (suggestion: string) => {
  searchQuery.value = suggestion
  showSuggestions.value = false
  handleSearch()
}

// 监听搜索框输入显示建议
watch(searchQuery, (newValue) => {
  showSuggestions.value = newValue.length > 0 && newValue.length < 3
})

// 组件挂载时获取数据
onMounted(async () => {
  await store.fetchTags()
})

// 点击外部关闭过滤器
const handleClickOutside = (event: Event) => {
  const target = event.target as HTMLElement
  if (!target.closest('.relative')) {
    showFilters.value = false
    showSuggestions.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

// 组件卸载时移除事件监听
import { onUnmounted } from 'vue'
onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
/* 自定义滚动条 */
.overflow-y-auto::-webkit-scrollbar {
  width: 4px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 2px;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 2px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>