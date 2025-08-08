<template>
  <div class="h-full flex flex-col">
    <div class="bg-white rounded-lg shadow-lg overflow-hidden flex flex-col h-full">
      <!-- 头部 -->
      <div class="bg-gradient-to-r from-indigo-600 to-blue-600 px-4 py-3 flex-shrink-0">
        <h2 class="text-lg font-bold text-white flex items-center">
          <svg class="h-5 w-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          版本历史: {{ prompt.title }}
        </h2>
        <p class="text-indigo-100 text-xs mt-1">
          查看和管理提示词的版本历史
        </p>
      </div>

      <div class="p-4 flex-1 overflow-y-auto">
        <!-- 当前版本 -->
        <div class="mb-4 p-3 bg-green-50 border border-green-200 rounded-lg">
          <div class="flex items-center justify-between mb-2">
            <div class="flex items-center">
              <span class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
                当前版本 v{{ prompt.version || 1 }}
              </span>
              <span class="ml-2 text-xs text-gray-600">
                {{ formatDate(prompt.updated_at || '') }}
              </span>
            </div>
          </div>
          <div class="bg-white rounded-md p-2 border max-h-20 overflow-y-auto">
            <pre class="whitespace-pre-wrap text-xs text-gray-900">{{ prompt.content }}</pre>
          </div>
        </div>

        <!-- 版本历史列表 -->
        <div class="flex-1">
          <div class="flex items-center justify-between mb-3">
            <h3 class="text-md font-medium text-gray-900 flex items-center">
              <svg class="h-4 w-4 mr-1 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
              历史版本
            </h3>
            <div class="flex-1 max-w-xs ml-4">
              <input
                v-model="searchQuery"
                type="text"
                placeholder="搜索版本名称或内容..."
                class="w-full px-2 py-1 text-xs border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
          </div>
          
          <div v-if="loading" class="text-center py-6">
            <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600 mx-auto"></div>
            <p class="mt-2 text-xs text-gray-500">加载版本历史...</p>
          </div>

          <div v-else-if="versions.length === 0" class="text-center py-6 text-gray-500">
            <svg class="mx-auto h-8 w-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <p class="mt-2 text-xs">暂无历史版本</p>
          </div>

          <div v-else class="space-y-3 max-h-65 overflow-y-auto">
            <div
              v-for="version in filteredVersions"
              :key="version.id"
              class="border border-gray-200 rounded-lg p-3 hover:border-gray-300 hover:shadow-sm transition-all duration-200"
            >
              <div class="flex items-center justify-between mb-2">
                <div class="flex items-center space-x-2">
                  <span class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
                    v{{ version.version }}
                  </span>
                  <span class="text-xs font-medium text-gray-800">
                    {{ version.name || '未命名' }}
                  </span>
                  <span class="text-xs text-gray-600">
                    {{ formatDate(version.created_at) }}
                  </span>
                  <span v-if="version.created_by" class="text-xs text-gray-500">
                    {{ version.created_by }}
                  </span>
                </div>
                <div class="flex space-x-1">
                  <button
                    @click="renameVersion(version)"
                    class="inline-flex items-center px-2 py-1 border border-gray-300 text-xs font-medium rounded text-indigo-700 hover:bg-indigo-50 transition-colors"
                  >
                    <svg class="mr-1 h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                    </svg>
                    命名
                  </button>
                  <button
                    @click="compareVersion(version)"
                    class="inline-flex items-center px-2 py-1 border border-gray-300 text-xs font-medium rounded text-gray-700 hover:bg-gray-50 transition-colors"
                  >
                    <svg class="mr-1 h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17V7m0 10a2 2 0 01-2 2H5a2 2 0 01-2-2V7a2 2 0 012-2h2a2 2 0 012 2m0 10a2 2 0 002 2h2a2 2 0 002-2M9 7a2 2 0 012-2h2a2 2 0 012 2m0 0V17m0-10a2 2 0 012 2v.01M9 7a2 2 0 012-2v.01" />
                    </svg>
                    对比
                  </button>
                  <button
                    @click="useThisVersion(version)"
                    class="inline-flex items-center px-2 py-1 border border-gray-300 text-xs font-medium rounded text-green-700 hover:bg-green-50 transition-colors"
                  >
                    <svg class="mr-1 h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    使用此版本
                  </button>
                </div>
              </div>

              <div v-if="version.change_description" class="mb-2">
                <p class="text-xs text-gray-700 bg-gray-50 rounded p-2">
                  <span class="font-medium">变更:</span> {{ version.change_description }}
                </p>
              </div>

              <div class="bg-gray-50 rounded-md p-2 max-h-16 overflow-y-auto">
                <pre class="whitespace-pre-wrap text-xs text-gray-900">{{ version.content }}</pre>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 底部按钮 -->
      <div class="px-4 py-3 bg-gray-50 flex justify-end border-t flex-shrink-0">
        <button
          @click="$emit('close')"
          class="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-xs font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 transition-colors"
        >
          关闭
        </button>
      </div>
    </div>

    <!-- 创建新版本模态框 -->
    <div v-if="showCreateVersionModal" class="fixed inset-0 z-50 overflow-y-auto">
      <div class="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" @click="showCreateVersionModal = false"></div>
        
        <div class="inline-block align-bottom bg-white rounded-lg px-4 pt-4 pb-4 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-md sm:w-full">
          <form @submit.prevent="handleCreateVersion">
            <div class="mb-3">
              <h3 class="text-md leading-6 font-medium text-gray-900 mb-1">
                创建新版本
              </h3>
              <p class="text-xs text-gray-500">
                基于当前内容创建新版本
              </p>
            </div>

            <div class="mb-3">
              <label class="block text-xs font-medium text-gray-700 mb-1">
                变更说明
              </label>
              <textarea
                v-model="newVersionData.change_description"
                rows="2"
                class="w-full px-2 py-1 text-xs border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500"
                placeholder="请描述本次变更的内容..."
              ></textarea>
            </div>

            <div class="mb-4">
              <label class="block text-xs font-medium text-gray-700 mb-1">
                创建者
              </label>
              <input
                v-model="newVersionData.created_by"
                type="text"
                class="w-full px-2 py-1 text-xs border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500"
                placeholder="请输入您的名字"
              />
            </div>

            <div class="flex justify-end space-x-2">
              <button
                type="button"
                @click="showCreateVersionModal = false"
                class="px-3 py-1 border border-gray-300 rounded-md text-xs font-medium text-gray-700 hover:bg-gray-50 transition-colors"
              >
                取消
              </button>
              <button
                type="submit"
                :disabled="isCreatingVersion"
                class="px-3 py-1 border border-transparent rounded-md shadow-sm text-xs font-medium text-white bg-blue-600 hover:bg-blue-700 disabled:opacity-50 transition-colors"
              >
                {{ isCreatingVersion ? '创建中...' : '创建版本' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- 版本对比模态框 -->
    <Teleport to="body">
      <div v-if="showCompareModal && compareVersionData" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
        <div class="w-full max-w-6xl mx-auto">
          <VersionCompareView
            :prompt="prompt"
            :versions="[compareVersionData]"
            @close="showCompareModal = false"
          />
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useMainStore } from '@/stores'
import type { Prompt, PromptVersion } from '@/services/api'
import VersionCompareView from './VersionCompareView.vue';

interface Props {
  prompt: Prompt;
}

const props = defineProps<Props>();

const emit = defineEmits<{
  (e: 'close'): void;
  (e: 'restore', version: PromptVersion): void;
}>();

const store = useMainStore()

const loading = ref(true);
const versions = ref<PromptVersion[]>([]);
const searchQuery = ref('');
const showCreateVersionModal = ref(false);
const isCreatingVersion = ref(false);
const newVersionData = ref({
  change_description: '',
  created_by: '',
});
const showCompareModal = ref(false)
const compareVersionData = ref<PromptVersion | null>(null)

const formatDate = (dateString: string) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN')
}

// 过滤版本列表
const filteredVersions = computed(() => {
  if (!searchQuery.value.trim()) {
    return versions.value
  }
  
  const query = searchQuery.value.toLowerCase()
  return versions.value.filter(version => 
    (version.name && version.name.toLowerCase().includes(query)) ||
    (version.content && version.content.toLowerCase().includes(query)) ||
    (version.change_description && version.change_description.toLowerCase().includes(query))
  )
})

const loadVersions = async () => {
  try {
    loading.value = true
    versions.value = await store.fetchPromptVersionsFromApi(props.prompt.id)
  } catch (error) {
    console.error('加载版本历史失败:', error)
  } finally {
    loading.value = false
  }
}

const renameVersion = async (version: PromptVersion) => {
  const newName = prompt('请输入新的版本名称:', version.name || '')
  if (newName !== null && newName.trim() !== '') {
    try {
      await store.updatePromptVersionName(version.id, newName.trim())
      // 重新加载版本历史
      await loadVersions()
    } catch (error) {
      console.error('更新版本名称失败:', error)
      alert('更新版本名称失败: ' + (error instanceof Error ? error.message : '未知错误'))
    }
  }
}

const compareVersion = (version: PromptVersion) => {
  compareVersionData.value = version
  showCompareModal.value = true
}

const useThisVersion = async (version: PromptVersion) => {
  if (!confirm(`确定要切换到版本 v${version.version} - ${version.name || '未命名'} 吗？这将替换当前提示词的内容。`)) {
    return
  }

  try {
    emit('restore', version)
    emit('close')
  } catch (error) {
    console.error('切换版本失败:', error)
    alert('切换版本失败: ' + (error instanceof Error ? error.message : '未知错误'))
  }
}

onMounted(() => {
  loadVersions()
})
</script>