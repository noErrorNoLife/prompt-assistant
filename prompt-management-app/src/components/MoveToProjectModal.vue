<template>
  <Modal :show="show" @close="close" max-width="md">
    <div class="p-6">
      <h2 class="text-lg font-medium text-gray-900">移动提示词</h2>
      <p class="mt-1 text-sm text-gray-500">
        将 "<span class="font-semibold">{{ prompt?.title }}</span>" 移动到...
      </p>

      <div class="mt-4 max-h-60 overflow-y-auto">
        <ul class="divide-y divide-gray-200">
          <li
            v-for="project in projectsWithNone"
            :key="project.id ?? 'none'"
            @click="moveToProject(project.id)"
            class="p-3 flex items-center justify-between cursor-pointer hover:bg-gray-50"
            :class="{ 'bg-blue-50': prompt?.project_id === project.id }"
          >
            <span class="text-sm font-medium text-gray-800">{{ project.name }}</span>
            <svg v-if="prompt?.project_id === project.id || (prompt?.project_id === null && project.id === null)" class="w-5 h-5 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
            </svg>
          </li>
        </ul>
      </div>

      <div class="mt-6 flex justify-end">
        <button @click="close" class="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50">
          取消
        </button>
      </div>
    </div>
  </Modal>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useMainStore } from '@/stores'
import type { Prompt } from '@/stores'
import Modal from './Modal.vue'

interface Props {
  show: boolean
  prompt: Prompt | null
}

const props = defineProps<Props>()

const emit = defineEmits<{
  (e: 'close'): void
}>()

const store = useMainStore()

const projectsWithNone = computed(() => {
  return [
    { id: null, name: '-- 无项目 --' },
    ...store.projects,
  ]
})

const moveToProject = async (projectId: number | null) => {
  if (props.prompt) {
    await store.movePromptToProject(props.prompt.id, projectId)
    close()
  }
}

const close = () => {
  emit('close')
}
</script> 