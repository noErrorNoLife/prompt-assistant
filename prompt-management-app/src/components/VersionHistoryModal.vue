<template>
  <TransitionRoot as="template" :show="open">
    <Dialog as="div" class="relative z-30" @close="$emit('close')">
      <TransitionChild as="template" enter="ease-out duration-300" enter-from="opacity-0" enter-to="opacity-100" leave="ease-in duration-200" leave-from="opacity-100" leave-to="opacity-0">
        <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" />
      </TransitionChild>

      <div class="fixed inset-0 z-10 w-screen overflow-y-auto">
        <div class="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0">
          <TransitionChild as="template" enter="ease-out duration-300" enter-from="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95" enter-to="opacity-100 translate-y-0 sm:scale-100" leave="ease-in duration-200" leave-from="opacity-100 translate-y-0 sm:scale-100" leave-to="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95">
            <DialogPanel class="relative transform overflow-hidden rounded-lg bg-white text-left shadow-xl transition-all sm:my-8 sm:w-full sm:max-w-6xl">
              <div class="bg-white px-4 pb-4 pt-5 sm:p-6 sm:pb-4">
                <div class="sm:flex sm:items-start">
                  <div class="mt-3 text-center sm:ml-4 sm:mt-0 sm:text-left w-full">
                    <DialogTitle as="h3" class="text-lg font-semibold leading-6 text-gray-900">
                      版本历史: {{ currentPrompt?.title }}
                    </DialogTitle>
                    <div class="mt-4">
                      <div class="flex justify-between mb-4">
                        <input
                          v-model="searchQuery"
                          type="text"
                          placeholder="搜索版本名称或内容..."
                          class="block w-1/3 rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                        />
                      </div>
                      <div class="grid grid-cols-1 md:grid-cols-2 gap-6" style="min-height: 60vh;">
                        <!-- 版本列表 -->
                        <div class="border rounded-md p-4 overflow-y-auto" style="max-height: 60vh;">
                          <ul role="list" class="divide-y divide-gray-200">
                            <li v-for="version in filteredVersions" :key="version.id" class="py-3 px-2 rounded-md hover:bg-gray-50">
                              <div class="flex items-center justify-between">
                                <div class="cursor-pointer" @click="toggleSelection(version.id)">
                                  <input type="checkbox" :checked="isSelected(version.id)" class="mr-3 h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-600">
                                  <span class="text-sm font-medium text-gray-900">v{{ version.version }} - {{ version.name || '未命名' }}</span>
                                  <span class="text-xs text-gray-500 ml-2">{{ formatDate(version.created_at) }}</span>
                                </div>
                                <div>
                                  <button @click="promptRename(version)" class="text-sm text-indigo-600 hover:text-indigo-900">命名</button>
                                  <button @click="useThisVersion(version)" class="text-sm text-green-600 hover:text-green-900 ml-2">使用此版本</button>
                                </div>
                              </div>
                            </li>
                          </ul>
                        </div>
                        <!-- 差异对比 -->
                        <div class="border rounded-md p-4 overflow-y-auto" style="max-height: 60vh;">
                          <h4 class="text-md font-semibold text-gray-800 mb-2">版本差异</h4>
                           <div v-if="diffHtml" v-html="diffHtml" class="diff-container"></div>
                           <div v-else class="text-gray-500 text-center py-10">
                             <p>请选择两个版本进行对比。</p>
                           </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div class="bg-gray-50 px-4 py-3 sm:flex sm:flex-row-reverse sm:px-6">
                <button type="button" class="mt-3 inline-flex w-full justify-center rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50 sm:mt-0 sm:w-auto" @click="$emit('close')">关闭</button>
              </div>
            </DialogPanel>
          </TransitionChild>
        </div>
      </div>
    </Dialog>
  </TransitionRoot>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { Dialog, DialogPanel, DialogTitle, TransitionChild, TransitionRoot } from '@headlessui/vue'
import { useMainStore } from '@/stores'
import type { Prompt } from '@/stores'
import * as Diff from 'diff'
import { html as diff2html } from 'diff2html';
import 'diff2html/bundles/css/diff2html.min.css';

const props = defineProps<{
  open: boolean
  promptId: string | null
}>()

const emit = defineEmits(['close', 'version-switched'])

const store = useMainStore()
const searchQuery = ref('')
const selectedVersionIds = ref<number[]>([])
const diffHtml = ref<string | null>(null)

const currentPrompt = computed(() => {
  if (!props.promptId) return null
  return store.getPromptById(props.promptId)
})

const versions = computed(() => {
  if (!currentPrompt.value) return []
  return store.getPromptVersions(currentPrompt.value.id).sort((a, b) => (b.version || 0) - (a.version || 0))
})

const filteredVersions = computed(() => {
  if (!searchQuery.value) return versions.value
  const lowerCaseQuery = searchQuery.value.toLowerCase()
  return versions.value.filter(v =>
    (v.name && v.name.toLowerCase().includes(lowerCaseQuery)) ||
    (v.content && v.content.toLowerCase().includes(lowerCaseQuery))
  )
})

const isSelected = (versionId: number) => selectedVersionIds.value.includes(versionId)

const toggleSelection = (versionId: number) => {
  const index = selectedVersionIds.value.indexOf(versionId)
  if (index > -1) {
    selectedVersionIds.value.splice(index, 1)
  } else {
    if (selectedVersionIds.value.length < 2) {
      selectedVersionIds.value.push(versionId)
    } else {
      // 简单地替换最后一个
      selectedVersionIds.value.splice(1, 1, versionId)
    }
  }
}

const generateDiff = () => {
  if (selectedVersionIds.value.length !== 2) {
    diffHtml.value = null
    return
  }
  const [id1, id2] = selectedVersionIds.value
  const version1 = versions.value.find(v => v.id === id1)
  const version2 = versions.value.find(v => v.id === id2)

  if (!version1 || !version2) return

  // 保证版本顺序
  const [oldVersion, newVersion] = (version1.version || 0) < (version2.version || 0) ? [version1, version2] : [version2, version1]

  const diffString = Diff.createTwoFilesPatch(
    `v${oldVersion.version} - ${oldVersion.name || 'untitled'}`,
    `v${newVersion.version} - ${newVersion.name || 'untitled'}`,
    oldVersion.content,
    newVersion.content
  );

  diffHtml.value = diff2html(diffString, {
    drawFileList: false,
    matching: 'lines',
    outputFormat: 'side-by-side',
    renderNothingWhenEmpty: true,
  });
}

const promptRename = async (version: any) => {
  const newName = prompt('请输入新的版本名称:', version.name || '')
  if (newName !== null && newName.trim() !== '') {
    try {
      await store.updatePromptVersionName(version.id, newName.trim())
      // 重新加载版本历史
      await loadVersions()
    } catch (error) {
      console.error('更新版本名称失败:', error)
    }
  }
}

const useThisVersion = async (version: Prompt) => {
  if (confirm(`你确定要切换到 v${version.version} - ${version.name || '未命名'} 版本吗？这将替换当前提示词的内容。`)) {
    await store.switchToVersion(currentPrompt.value!.id, version)
    emit('version-switched', version)
    emit('close')
  }
}

const formatDate = (dateString?: string) => {
  if (!dateString) return '未知日期'
  return new Date(dateString).toLocaleString()
}

watch(selectedVersionIds, generateDiff, { deep: true })

watch(() => props.open, (isOpen) => {
  if (!isOpen) {
    selectedVersionIds.value = []
    diffHtml.value = null
    searchQuery.value = ''
  }
})
</script>

<style>
.diff-container .d2h-file-header {
  display: none;
}
.diff-container .d2h-diff-table {
  width: 100%;
}
</style> 