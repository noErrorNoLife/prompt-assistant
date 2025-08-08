<template>
  <div class="p-4">
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-3xl font-bold text-gray-800">模块管理</h1>
      <button @click="openAddModal" class="px-4 py-2 font-bold text-white bg-green-500 rounded-lg shadow-md hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-400 focus:ring-opacity-75 transition-transform transform hover:scale-105">
        + 添加新模块
      </button>
    </div>

    <!-- 加载状态 -->
    <div v-if="mainStore.isLoading" class="text-center py-8">
      <p class="text-gray-600">正在加载...</p>
    </div>

    <!-- 错误信息 -->
    <div v-if="mainStore.errorMessage" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
      {{ mainStore.errorMessage }}
    </div>

    <!-- Modules List -->
    <div v-if="!mainStore.isLoading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div 
        v-for="module in modules" 
        :key="module.id"
        class="bg-white rounded-lg shadow-lg overflow-hidden transform hover:-translate-y-1 transition-all duration-300"
      >
        <div class="p-5">
          <div class="flex items-center justify-between mb-3">
            <h3 class="text-xl font-bold text-gray-900">{{ module.name }}</h3>
            <span 
              :class="{
                'bg-green-200 text-green-800': module.status === 'active',
                'bg-red-200 text-red-800': module.status === 'inactive',
                'bg-gray-200 text-gray-800': !module.status || module.status === 'pending'
              }"
              class="px-2 py-1 text-xs font-semibold rounded-full"
            >
              {{ getStatusText(module.status) }}
            </span>
          </div>
          <p class="text-gray-700 mb-4 h-24 overflow-hidden">{{ module.description || '暂无描述' }}</p>
          <div class="flex items-center justify-between">
            <div class="text-sm text-gray-500">
              创建时间: {{ formatDate(module.created_at) }}
            </div>
            <div class="flex space-x-2">
              <button @click="openEditModal(module)" class="text-gray-400 hover:text-blue-500 transition-colors">
                <!-- Edit Icon -->
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor"><path d="M17.414 2.586a2 2 0 00-2.828 0L7 10.172V13h2.828l7.586-7.586a2 2 0 000-2.828z" /><path fill-rule="evenodd" d="M2 6a2 2 0 012-2h4a1 1 0 010 2H4v10h10v-4a1 1 0 112 0v4a2 2 0 01-2 2H4a2 2 0 01-2-2V6z" clip-rule="evenodd" /></svg>
              </button>
              <button @click="handleDelete(module.id)" class="text-gray-400 hover:text-red-500 transition-colors">
                <!-- Delete Icon -->
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm4 0a1 1 0 012 0v6a1 1 0 11-2 0V8z" clip-rule="evenodd" /></svg>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 如果没有模块，显示空状态 -->
    <div v-if="!mainStore.isLoading && modules.length === 0" class="text-center py-12">
      <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path>
      </svg>
      <h3 class="mt-2 text-sm font-medium text-gray-900">暂无模块</h3>
      <p class="mt-1 text-sm text-gray-500">开始创建你的第一个模块吧。</p>
      <div class="mt-6">
        <button @click="openAddModal" type="button" class="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500">
          <svg class="-ml-1 mr-2 h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd" />
          </svg>
          添加新模块
        </button>
      </div>
    </div>

    <!-- Modal for Add/Edit Module -->
    <Modal :show="isModalOpen" @close="closeModal">
      <template #header>{{ modalTitle }}</template>
      <ModuleForm :module="editingModule" @submit="handleFormSubmit" @close="closeModal" />
    </Modal>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useMainStore, type Module } from '@/stores';
import Modal from '@/components/Modal.vue';
import ModuleForm from '@/components/ModuleForm.vue';

const mainStore = useMainStore();
const modules = computed(() => mainStore.modules);

const isModalOpen = ref(false);
const editingModule = ref<Module | undefined>(undefined);
const modalTitle = computed(() => editingModule.value ? '编辑模块' : '添加新模块');

// 组件挂载时获取数据
onMounted(async () => {
  await mainStore.fetchModules();
});

const openAddModal = () => {
  editingModule.value = undefined;
  isModalOpen.value = true;
};

const openEditModal = (module: Module) => {
  editingModule.value = { ...module };
  isModalOpen.value = true;
};

const closeModal = () => {
  isModalOpen.value = false;
  editingModule.value = undefined;
};

const handleFormSubmit = async (formData: Module) => {
  try {
    if (editingModule.value) {
      await mainStore.updateModule(formData);
    } else {
      await mainStore.addModule(formData);
    }
    closeModal();
  } catch (error) {
    console.error('提交表单失败:', error);
    // 这里可以添加用户友好的错误提示
  }
};

const handleDelete = async (id: number) => {
  if (confirm('你确定要删除这个模块吗？')) {
    try {
      await mainStore.deleteModule(id);
    } catch (error) {
      console.error('删除模块失败:', error);
      // 这里可以添加用户友好的错误提示
    }
  }
}

const getStatusText = (status?: string) => {
  switch (status) {
    case 'active':
      return '活跃';
    case 'inactive':
      return '停用';
    case 'pending':
      return '待激活';
    default:
      return '未知';
  }
};

const formatDate = (dateString?: string) => {
  if (!dateString) return '未知';
  const date = new Date(dateString);
  return date.toLocaleDateString('zh-CN');
};
</script>

<style scoped>
/* 在这里可以添加组件的样式 */
</style> 