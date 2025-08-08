<template>
  <transition name="modal-fade">
    <div v-if="show" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50" @click.self="handleBackgroundClick">
      <div :class="['bg-white rounded-lg shadow-xl transform transition-all sm:w-full relative', maxWidthClass]" role="dialog" aria-modal="true">
        <!-- Close button positioned absolutely -->
        <button @click.stop="$emit('close')" class="absolute top-4 right-4 z-10 p-1 rounded-full hover:bg-gray-200 bg-white shadow-sm">
          <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
        </button>
        
        <!-- Modal content -->
        <div :class="['w-full h-full', contentClass]">
          <slot></slot>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup lang="ts">
import { computed, onMounted, onUnmounted } from 'vue';

const props = withDefaults(defineProps<{
  show: boolean;
  maxWidth?: 'sm' | 'md' | 'lg' | 'xl' | '2xl' | '3xl' | '4xl' | '5xl' | '6xl' | '7xl';
  contentClass?: string;
  closeOnBackgroundClick?: boolean;
}>(), {
  maxWidth: 'lg',
  contentClass: '',
  closeOnBackgroundClick: true,
});

const emit = defineEmits(['close']);

const maxWidthClass = computed(() => {
  return {
    'sm': 'sm:max-w-sm',
    'md': 'sm:max-w-md',
    'lg': 'sm:max-w-lg',
    'xl': 'sm:max-w-xl',
    '2xl': 'sm:max-w-2xl',
    '3xl': 'sm:max-w-3xl',
    '4xl': 'sm:max-w-4xl',
    '5xl': 'sm:max-w-5xl',
    '6xl': 'sm:max-w-6xl',
    '7xl': 'sm:max-w-7xl',
  }[props.maxWidth];
});

const handleBackgroundClick = () => {
  if (props.closeOnBackgroundClick) {
    emit('close');
  }
};

const handleEscape = (e: KeyboardEvent) => {
  if (e.key === 'Escape') {
    emit('close');
  }
};

onMounted(() => {
  document.addEventListener('keydown', handleEscape);
});

onUnmounted(() => {
  document.removeEventListener('keydown', handleEscape);
});
</script>

<style scoped>
.modal-fade-enter-active, .modal-fade-leave-active {
  transition: opacity 0.3s ease;
}
.modal-fade-enter-from, .modal-fade-leave-to {
  opacity: 0;
}
</style> 