<template>
  <div class="h-full bg-gray-50 border-r border-gray-200 flex flex-col">
    <div class="p-4 border-b border-gray-200">
      <h2 class="text-base font-semibold text-gray-800">项目空间</h2>
    </div>
    
    <div class="flex-grow overflow-y-auto p-2">
      <ul class="space-y-1">
        <li>
          <a
            href="#"
            @click.prevent="handleSelectProject(null)"
            class="flex items-center px-3 py-2 text-sm font-medium rounded-md"
            :class="
              store.selectedProjectId === null
                ? 'bg-blue-100 text-blue-700'
                : 'text-gray-700 hover:bg-gray-200'
            "
          >
            <svg class="w-5 h-5 mr-3 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path></svg>
            <span>所有提示词</span>
          </a>
        </li>
        
        <li v-for="project in store.projects" :key="project.id">
          <a
            href="#"
            @click.prevent="handleSelectProject(project.id)"
            class="group flex items-center px-3 py-2 text-sm font-medium rounded-md"
            :class="
              store.selectedProjectId === project.id
                ? 'bg-blue-100 text-blue-700'
                : 'text-gray-700 hover:bg-gray-200'
            "
          >
            <svg class="w-5 h-5 mr-3 text-gray-400 group-hover:text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"></path></svg>
            <span class="flex-1 whitespace-nowrap">{{ project.name }}</span>
            <span class="inline-flex justify-center items-center px-2 text-xs font-medium text-gray-600 bg-gray-200 rounded-full">{{ project.prompt_count || 0 }}</span>
          </a>
        </li>
      </ul>
    </div>

    <div class="flex-shrink-0 p-4 border-t border-gray-200">
      <button
        @click="showCreateProjectModal = true"
        class="w-full inline-flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
      >
        <svg class="w-5 h-5 mr-2 -ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path></svg>
        新建项目
      </button>
    </div>
    
    <!-- 新建项目模态框 (暂未实现功能) -->
    <div v-if="showCreateProjectModal" class="fixed inset-0 bg-black bg-opacity-50 z-40" @click="showCreateProjectModal = false"></div>
    <div v-if="showCreateProjectModal" class="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white rounded-lg shadow-xl z-50 w-full max-w-md p-6">
      <h3 class="text-lg font-medium leading-6 text-gray-900 mb-4">新建项目</h3>
      <form @submit.prevent="handleCreateProject">
        <div>
          <label for="project-name" class="block text-sm font-medium text-gray-700">项目名称</label>
          <div class="mt-1">
            <input
              type="text"
              v-model="newProjectName"
              id="project-name"
              class="block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
              placeholder="请输入项目名称"
              required
            />
          </div>
        </div>
        <div class="mt-5 sm:mt-6 sm:grid sm:grid-cols-2 sm:gap-3 sm:grid-flow-row-dense">
          <button
            type="submit"
            class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-blue-600 text-base font-medium text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:col-start-2 sm:text-sm"
          >
            创建项目
          </button>
          <button
            type="button"
            @click="showCreateProjectModal = false"
            class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:mt-0 sm:col-start-1 sm:text-sm"
          >
            取消
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useMainStore } from '@/stores'

const store = useMainStore()
const showCreateProjectModal = ref(false)
const newProjectName = ref('')

const handleSelectProject = (projectId: number | null) => {
  store.selectProject(projectId)
}

const handleCreateProject = async () => {
  if (!newProjectName.value.trim()) return
  try {
    await store.addProject({ name: newProjectName.value })
    showCreateProjectModal.value = false
    newProjectName.value = ''
  } catch (error) {
    console.error('Failed to create project:', error)
    // Optionally: show an error message to the user
  }
}

onMounted(async () => {
  try {
    await store.fetchProjects()
  } catch (error) {
    console.error('Failed to fetch projects on mount:', error)
  }
})
</script> 