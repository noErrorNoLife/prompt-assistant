<template>
  <teleport to="body" v-if="show && prompt">
    <div class="fixed inset-0 bg-black bg-opacity-50 z-40" @click="close"></div>
    <transition name="slide-fade">
      <div class="fixed top-0 right-0 w-full max-w-2xl h-full bg-white shadow-xl z-50 flex flex-col">
        <div class="flex justify-between items-center p-4 border-b">
          <div class="flex items-center">
            <h2 class="text-lg font-semibold text-gray-800">Prompt 预览</h2>
            <button @click="renderMarkdown = !renderMarkdown" class="ml-4 text-gray-500 hover:text-gray-700 focus:outline-none" title="切换视图">
              <svg v-if="renderMarkdown" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path></svg>
              <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.542-7 .527-1.664 1.373-3.16 2.458-4.425L12 12l1.875 6.825z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15a3 3 0 100-6 3 3 0 000 6z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M1.958 8.042l1.414-1.414M20.625 17.5l1.414-1.414M17.5 6.375l1.414 1.414M5 18.042l-1.414 1.414"></path></svg>
            </button>
          </div>
          <button @click="close" class="text-gray-500 hover:text-gray-800">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
          </button>
        </div>
        <div class="p-6 flex-grow overflow-y-auto">
          <div v-if="prompt">
            <h3 class="text-xl font-bold mb-4">{{ prompt.title }}</h3>
            <div v-if="renderMarkdown" class="prose max-w-none" v-html="renderedMarkdown"></div>
            <div v-else>
              <pre class="whitespace-pre-wrap text-sm font-mono bg-gray-100 p-4 rounded-md overflow-x-auto">{{ prompt.content }}</pre>
            </div>
          </div>
          <div v-else class="text-center text-gray-500">
            <p>没有可预览的 Prompt。</p>
          </div>
        </div>
        <div class="p-4 border-t bg-gray-50">
          <button @click="close" type="button" class="px-4 py-2 bg-gray-200 text-gray-800 rounded-md hover:bg-gray-300">关闭</button>
        </div>
      </div>
    </transition>
  </teleport>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import { marked } from 'marked';
import type { Prompt } from '@/services/api';

interface Props {
  show: boolean;
  prompt: Prompt | null;
}

const props = defineProps<Props>();

const emit = defineEmits<{
  (e: 'close'): void;
}>();

const renderMarkdown = ref(true);

const renderedMarkdown = computed(() => {
  if (props.prompt && props.prompt.content) {
    return marked(props.prompt.content);
  }
  return '';
});

const close = () => {
  emit('close');
};
</script>

<style scoped>
.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.3s ease-out;
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateX(100%);
  opacity: 0;
}
</style> 