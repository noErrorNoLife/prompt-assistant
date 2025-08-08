<template>
  <div class="p-4 sm:p-6 lg:p-8">
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-3xl font-bold text-gray-800">我的提示词</h1>
      <button @click="openAddModal" class="px-4 py-2 font-bold text-white bg-blue-500 rounded-lg shadow-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-opacity-75 transition-transform transform hover:scale-105">
        + 添加新提示词
      </button>
    </div>

    <!-- 加载状态 -->
    <div v-if="mainStore.loading" class="text-center py-8">
      <p class="text-gray-600">正在加载...</p>
    </div>

    <!-- 错误信息 -->
    <div v-if="mainStore.error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
      {{ mainStore.error }}
    </div>

    <!-- Prompts List -->
    <div v-if="!mainStore.loading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
      <PromptCard
        v-for="prompt in prompts"
        :key="prompt.id"
        :prompt="prompt"
        @click="openPreviewModal"
        @edit="openEditModal"
        @delete="handleDelete"
        @versions="openVersionsModal"
        @clone="handleClone"
      />
    </div>

    <!-- Modal for Add/Edit Prompt -->
    <Modal :show="isModalOpen" @close="closeModal" max-width="5xl" content-class="p-0" :close-on-background-click="false">
      <PromptForm :prompt="editingPrompt" @submit="handleFormSubmit" @cancel="closeModal" />
    </Modal>
    
    <!-- Modal for Version History -->
    <VersionHistoryModal
      :open="isVersionsModalOpen"
      :prompt-id="selectedPromptId"
      @close="closeVersionsModal"
      @version-switched="handleVersionSwitched"
    />
    
    <!-- Modal for Prompt Preview -->
    <PromptPreviewModal
      :show="isPreviewModalOpen"
      :prompt="selectedPrompt"
      @close="closePreviewModal"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue';
import { useMainStore } from '@/stores';
import type { Prompt } from '@/services/api';
import Modal from '@/components/Modal.vue';
import PromptForm from '@/components/PromptForm.vue';
import PromptCard from '@/components/PromptCard.vue';
import VersionHistoryModal from '@/components/VersionHistoryModal.vue';
import PromptPreviewModal from '@/components/PromptPreviewModal.vue';

const mainStore = useMainStore();
const prompts = computed(() => mainStore.prompts.filter(p => !p.parent_id));

const isModalOpen = ref(false);
const editingPrompt = ref<Prompt | undefined>(undefined);

const isVersionsModalOpen = ref(false);
const selectedPromptId = ref<string | null>(null);

const isPreviewModalOpen = ref(false);
const selectedPrompt = ref<Prompt | null>(null);

watch(isPreviewModalOpen, (newValue, oldValue) => {
  console.log(`[DEBUG] isPreviewModalOpen 状态变化: 从 ${oldValue} 变为 ${newValue}`);
  if (newValue) {
    console.log('[DEBUG] 模态框状态变为开启，当前选中的Prompt:', selectedPrompt.value?.title);
  } else {
    console.log('[DEBUG] 模态框状态变为关闭。');
  }
});

onMounted(async () => {
  await mainStore.fetchPrompts();
});

const openAddModal = () => {
  editingPrompt.value = undefined;
  isModalOpen.value = true;
};

const openEditModal = (prompt: Prompt) => {
  editingPrompt.value = { ...prompt };
  isModalOpen.value = true;
};

const closeModal = () => {
  isModalOpen.value = false;
  editingPrompt.value = undefined;
};

const openPreviewModal = (prompt: Prompt) => {
  console.log('[DEBUG] Action: openPreviewModal - 开始执行。触发预览的Prompt:', prompt.title);
  selectedPrompt.value = prompt;
  console.log('[DEBUG] State Change: selectedPrompt 已被设置。');
  isPreviewModalOpen.value = true;
  console.log('[DEBUG] State Change: isPreviewModalOpen 已被设置为 true。');
};

const closePreviewModal = () => {
  console.log('[DEBUG] Action: closePreviewModal - 开始执行。');
  isPreviewModalOpen.value = false;
  selectedPrompt.value = null;
  console.log('[DEBUG] State Change: isPreviewModalOpen 已被设置为 false 且 selectedPrompt 已被清除。');
};

const handleFormSubmit = async (formData: Partial<Prompt>) => {
  const data = { ...formData };
  if (data.id) {
    await mainStore.updatePrompt(data as Prompt);
  } else {
    await mainStore.addPrompt(data as Prompt);
  }
  closeModal();
};

const handleDelete = async (prompt: Prompt) => {
  if (confirm('你确定要删除这个提示词及其所有历史版本吗？')) {
    await mainStore.deletePrompt(prompt.id);
  }
};

const openVersionsModal = (prompt: Prompt) => {
  selectedPromptId.value = prompt.id.toString();
  isVersionsModalOpen.value = true;
};

const closeVersionsModal = () => {
  isVersionsModalOpen.value = false;
  selectedPromptId.value = null;
};

const handleVersionSwitched = async () => {
  await mainStore.fetchPrompts();
};

const handleClone = async (prompt: Prompt) => {
  // Logic to handle cloning
  console.log('Cloning prompt:', prompt.title);
  // Example:
  // const newPromptData = { ...prompt, title: `${prompt.title} (Copy)` };
  // delete newPromptData.id;
  // await mainStore.addPrompt(newPromptData);
};
</script> 