<template>
  <form @submit.prevent="handleSubmit" class="space-y-4">
    <div>
      <label for="name" class="block text-sm font-medium text-gray-700">模块名称</label>
      <input
        id="name"
        v-model="formData.name"
        type="text"
        required
        class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
        placeholder="输入模块名称"
      />
    </div>

    <div>
      <label for="description" class="block text-sm font-medium text-gray-700">模块描述</label>
      <textarea
        id="description"
        v-model="formData.description"
        rows="3"
        class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
        placeholder="输入模块描述"
      />
    </div>

    <div>
      <label for="status" class="block text-sm font-medium text-gray-700">状态</label>
      <select
        id="status"
        v-model="formData.status"
        class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
      >
        <option value="active">活跃</option>
        <option value="inactive">停用</option>
        <option value="pending">待激活</option>
      </select>
    </div>

    <div class="flex justify-end space-x-3 pt-4">
      <button
        type="button"
        @click="$emit('close')"
        class="inline-flex justify-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
      >
        取消
      </button>
      <button
        type="submit"
        class="inline-flex justify-center rounded-md border border-transparent bg-indigo-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
      >
        {{ module ? '更新' : '创建' }}
      </button>
    </div>
  </form>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';
import type { Module } from '@/stores';

const props = defineProps<{
  module?: Module;
}>();

const emit = defineEmits<{
  submit: [module: Module];
  close: [];
}>();

const formData = ref<Module>({
  id: 0,
  name: '',
  description: '',
  status: 'active',
});

// 当传入的module发生变化时，更新表单数据
watch(
  () => props.module,
  (newModule) => {
    if (newModule) {
      formData.value = { ...newModule };
    } else {
      formData.value = {
        id: 0,
        name: '',
        description: '',
        status: 'active',
      };
    }
  },
  { immediate: true }
);

const handleSubmit = () => {
  emit('submit', formData.value);
};
</script> 