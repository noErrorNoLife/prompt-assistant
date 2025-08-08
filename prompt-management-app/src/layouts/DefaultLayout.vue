<template>
  <div class="flex h-screen bg-gray-100">
    <!-- Sidebar -->
    <aside class="w-64 bg-white shadow-md">
      <div class="p-4">
        <h1 class="text-xl font-bold">Prompt Mgt</h1>
      </div>
      <nav class="mt-4">
        <ul>
          <li>
            <router-link to="/" class="block px-4 py-2 text-gray-700 hover:bg-gray-200">首页</router-link>
          </li>
          <li>
            <router-link to="/drafts" class="block px-4 py-2 text-gray-700 hover:bg-gray-200">📝 草稿箱</router-link>
          </li>
          <li>
            <router-link to="/prompts" class="block px-4 py-2 text-gray-700 hover:bg-gray-200">我的提示词</router-link>
          </li>
          <li>
            <router-link to="/modules" class="block px-4 py-2 text-gray-700 hover:bg-gray-200">模块管理</router-link>
          </li>
           <li>
            <router-link to="/templates" class="block px-4 py-2 text-gray-700 hover:bg-gray-200">模板市场</router-link>
          </li>
        </ul>
      </nav>
    </aside>

    <!-- Main Content -->
    <main class="flex-1 p-8 overflow-y-auto">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
</script> 