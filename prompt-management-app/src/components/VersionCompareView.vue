<template>
  <div class="version-compare-view bg-white rounded-lg shadow-lg">
    <!-- 头部 -->
    <div class="border-b border-gray-200 px-6 py-4">
      <div class="flex items-center justify-between">
        <div>
          <h3 class="text-lg font-medium text-gray-900">版本对比</h3>
          <p class="text-sm text-gray-500 mt-1">
            对比 {{ promptTitle }} 的不同版本
          </p>
        </div>
        <button
          @click="$emit('close')"
          class="text-gray-400 hover:text-gray-600 transition-colors"
        >
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
    </div>

    <div class="p-6">
      <!-- 版本选择和视图切换 -->
      <div class="flex items-center justify-between mb-6">
        <div class="flex items-center space-x-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">版本 A</label>
            <select
              v-model="selectedVersionA"
              class="px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="current">当前版本</option>
              <option v-for="version in versions" :key="version.id" :value="version.id">
                v{{ version.version }} ({{ formatDate(version.created_at) }})
              </option>
            </select>
          </div>

          <div class="flex items-center">
            <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4" />
            </svg>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">版本 B</label>
            <select
              v-model="selectedVersionB"
              class="px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="current">当前版本</option>
              <option v-for="version in versions" :key="version.id" :value="version.id">
                v{{ version.version }} ({{ formatDate(version.created_at) }})
              </option>
            </select>
          </div>
        </div>

        <div class="flex items-center space-x-2">
          <button
            @click="viewMode = 'side-by-side'"
            :class="[
              'px-3 py-2 text-sm font-medium rounded-md',
              viewMode === 'side-by-side'
                ? 'bg-blue-100 text-blue-700'
                : 'text-gray-500 hover:text-gray-700'
            ]"
          >
            并排对比
          </button>
          <button
            @click="viewMode = 'inline'"
            :class="[
              'px-3 py-2 text-sm font-medium rounded-md',
              viewMode === 'inline'
                ? 'bg-blue-100 text-blue-700'
                : 'text-gray-500 hover:text-gray-700'
            ]"
          >
            行内对比
          </button>
        </div>
      </div>

      <!-- 比较结果 -->
      <div v-if="!isComparing">
        <!-- 并排对比视图 -->
        <div v-if="viewMode === 'side-by-side'" class="grid grid-cols-2 gap-6">
          <div>
            <div class="bg-gray-50 px-4 py-2 text-sm font-medium text-gray-700 border border-gray-200 rounded-t-lg">
              {{ getVersionLabel(selectedVersionA) }}
            </div>
            <div class="border border-t-0 border-gray-200 rounded-b-lg p-4 bg-white min-h-96 max-h-96 overflow-y-auto">
              <div v-html="sideByDiffHtmlA" class="text-sm font-mono whitespace-pre-wrap"></div>
            </div>
          </div>

          <div>
            <div class="bg-gray-50 px-4 py-2 text-sm font-medium text-gray-700 border border-gray-200 rounded-t-lg">
              {{ getVersionLabel(selectedVersionB) }}
            </div>
            <div class="border border-t-0 border-gray-200 rounded-b-lg p-4 bg-white min-h-96 max-h-96 overflow-y-auto">
              <div v-html="sideByDiffHtmlB" class="text-sm font-mono whitespace-pre-wrap"></div>
            </div>
          </div>
        </div>

        <!-- 行内对比视图 -->
        <div v-else class="border border-gray-200 rounded-lg">
          <div class="bg-gray-50 px-4 py-2 text-sm font-medium text-gray-700 border-b border-gray-200">
            {{ getVersionLabel(selectedVersionA) }} vs {{ getVersionLabel(selectedVersionB) }}
          </div>
          <div class="p-4 bg-white max-h-96 overflow-y-auto">
            <div v-html="inlineDiffHtml" class="text-sm font-mono"></div>
          </div>
        </div>

        <!-- 统计信息 -->
        <div class="mt-6 grid grid-cols-3 gap-4">
          <div class="bg-green-50 border border-green-200 rounded-lg p-4 text-center">
            <div class="text-2xl font-bold text-green-600">{{ stats.additions }}</div>
            <div class="text-sm text-green-700">新增</div>
          </div>
          <div class="bg-red-50 border border-red-200 rounded-lg p-4 text-center">
            <div class="text-2xl font-bold text-red-600">{{ stats.deletions }}</div>
            <div class="text-sm text-red-700">删除</div>
          </div>
          <div class="bg-blue-50 border border-blue-200 rounded-lg p-4 text-center">
            <div class="text-2xl font-bold text-blue-600">{{ stats.modifications }}</div>
            <div class="text-sm text-blue-700">修改</div>
          </div>
        </div>
      </div>

      <!-- 加载状态 -->
      <div v-else class="flex justify-center items-center py-12">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        <span class="ml-3 text-gray-600">正在比较版本...</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import type { Prompt, PromptVersion } from '@/services/api'

interface Props {
  prompt: Prompt
  versions: PromptVersion[]
}

const props = defineProps<Props>()

const emit = defineEmits<{
  close: []
}>()

const selectedVersionA = ref<'current' | number>('current')
const selectedVersionB = ref<'current' | number>(props.versions[0]?.id || 'current')
const viewMode = ref<'side-by-side' | 'inline'>('side-by-side')
const isComparing = ref(false)

const promptTitle = computed(() => props.prompt.title)

const versionAContent = computed(() => {
  if (selectedVersionA.value === 'current') {
    return props.prompt.content
  }
  const version = props.versions.find(v => v.id === selectedVersionA.value)
  return version?.content || ''
})

const versionBContent = computed(() => {
  if (selectedVersionB.value === 'current') {
    return props.prompt.content
  }
  const version = props.versions.find(v => v.id === selectedVersionB.value)
  return version?.content || ''
})

interface DiffItem {
  type: 'equal' | 'delete' | 'insert'
  text: string
}

interface AlignedLine {
  type: 'equal' | 'delete' | 'insert' | 'change'
  lineA?: string
  lineB?: string
}

// Line-level diff using LCS
const getAlignedDiff = (textA: string, textB: string): AlignedLine[] => {
  const linesA = textA.replace(/\r\n/g, '\n').split('\n');
  const linesB = textB.replace(/\r\n/g, '\n').split('\n');
  const n = linesA.length;
  const m = linesB.length;

  const dp = Array.from({ length: n + 1 }, () => Array(m + 1).fill(0));
  for (let i = 1; i <= n; i++) {
    for (let j = 1; j <= m; j++) {
      if (linesA[i - 1] === linesB[j - 1]) {
        dp[i][j] = dp[i - 1][j - 1] + 1;
      } else {
        dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
      }
    }
  }

  const rawDiff: AlignedLine[] = [];
  let i = n;
  let j = m;
  while (i > 0 || j > 0) {
    if (i > 0 && j > 0 && linesA[i - 1] === linesB[j - 1]) {
      rawDiff.unshift({ type: 'equal', lineA: linesA[i - 1], lineB: linesB[j - 1] });
      i--;
      j--;
    } else if (j > 0 && (i === 0 || dp[i][j - 1] >= dp[i - 1][j])) {
      rawDiff.unshift({ type: 'insert', lineB: linesB[j - 1] });
      j--;
    } else if (i > 0) {
      rawDiff.unshift({ type: 'delete', lineA: linesA[i - 1] });
      i--;
    }
  }

  const processedDiff: AlignedLine[] = [];
  for (let k = 0; k < rawDiff.length; k++) {
    const current = rawDiff[k];
    const next = rawDiff[k + 1];
    if (current.type === 'delete' && next?.type === 'insert') {
      processedDiff.push({ type: 'change', lineA: current.lineA, lineB: next.lineB });
      k++;
    } else {
      processedDiff.push(current);
    }
  }
  return processedDiff;
};

// Character-level diff using LCS
const getCharacterDiff = (textA: string, textB: string): DiffItem[] => {
  const charsA = textA.split('');
  const charsB = textB.split('');
  const n = charsA.length;
  const m = charsB.length;
  const dp = Array.from({ length: n + 1 }, () => Array(m + 1).fill(0));

  for (let i = 1; i <= n; i++) {
    for (let j = 1; j <= m; j++) {
      if (charsA[i - 1] === charsB[j - 1]) {
        dp[i][j] = dp[i - 1][j - 1] + 1;
      } else {
        dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
      }
    }
  }

  const diff: DiffItem[] = [];
  let i = n;
  let j = m;
  while (i > 0 || j > 0) {
    if (i > 0 && j > 0 && charsA[i - 1] === charsB[j - 1]) {
      diff.unshift({ type: 'equal', text: charsA[i - 1] });
      i--; j--;
    } else if (j > 0 && (i === 0 || dp[i][j - 1] >= dp[i - 1][j])) {
      diff.unshift({ type: 'insert', text: charsB[j - 1] });
      j--;
    } else if (i > 0) {
      diff.unshift({ type: 'delete', text: charsA[i - 1] });
      i--;
    }
  }
  return diff;
};

const escapeHtml = (text: string) => {
  const div = document.createElement('div')
  div.textContent = text
  return div.innerHTML
}

const renderCharDiff = (lineA = '', lineB = '') => {
  const charDiff = getCharacterDiff(lineA, lineB)
  const html = { a: '', b: '' }

  charDiff.forEach(item => {
    if (item.type === 'equal') {
      html.a += escapeHtml(item.text)
      html.b += escapeHtml(item.text)
    } else if (item.type === 'delete') {
      html.a += `<span class="diff-char-deleted">${escapeHtml(item.text)}</span>`
    } else if (item.type === 'insert') {
      html.b += `<span class="diff-char-inserted">${escapeHtml(item.text)}</span>`
    }
  })
  return html
}

const diffResult = computed(() => getAlignedDiff(versionAContent.value, versionBContent.value))

const stats = computed(() => {
  const s = { additions: 0, deletions: 0, modifications: 0 }
  diffResult.value.forEach(item => {
    if (item.type === 'insert') s.additions++
    if (item.type === 'delete') s.deletions++
    if (item.type === 'change') s.modifications++
  })
  return s
})

const sideByDiffHtmlA = computed(() => {
  if (versionAContent.value === versionBContent.value) return escapeHtml(versionAContent.value)
  return diffResult.value.map(item => {
    if (item.type === 'equal') return `<div>${escapeHtml(item.lineA!)}</div>`
    if (item.type === 'delete') return `<div class="diff-line-deleted">${escapeHtml(item.lineA!)}</div>`
    if (item.type === 'change') {
      const charHtml = renderCharDiff(item.lineA, item.lineB)
      return `<div class="diff-line-changed">${charHtml.a}</div>`
    }
    return '<div class="diff-line-empty">&nbsp;</div>'
  }).join('')
})

const sideByDiffHtmlB = computed(() => {
  if (versionAContent.value === versionBContent.value) return escapeHtml(versionBContent.value)
  return diffResult.value.map(item => {
    if (item.type === 'equal') return `<div>${escapeHtml(item.lineB!)}</div>`
    if (item.type === 'insert') return `<div class="diff-line-inserted">${escapeHtml(item.lineB!)}</div>`
    if (item.type === 'change') {
      const charHtml = renderCharDiff(item.lineA, item.lineB)
      return `<div class="diff-line-changed">${charHtml.b}</div>`
    }
    return '<div class="diff-line-empty">&nbsp;</div>'
  }).join('')
})

const inlineDiffHtml = computed(() => {
  if (versionAContent.value === versionBContent.value) return '<div>两个版本内容相同</div>'
  return diffResult.value.map(item => {
    if (item.type === 'equal') return `<div><span class="diff-marker-inline"> </span>${escapeHtml(item.lineA!)}</div>`
    if (item.type === 'delete') return `<div class="diff-line-deleted"><span class="diff-marker-inline">-</span>${escapeHtml(item.lineA!)}</div>`
    if (item.type === 'insert') return `<div class="diff-line-inserted"><span class="diff-marker-inline">+</span>${escapeHtml(item.lineB!)}</div>`
    if (item.type === 'change') {
      const charHtml = renderCharDiff(item.lineA, item.lineB)
      return `<div class="diff-line-deleted"><span class="diff-marker-inline">-</span>${charHtml.a}</div>` +
             `<div class="diff-line-inserted"><span class="diff-marker-inline">+</span>${charHtml.b}</div>`
    }
    return ''
  }).join('')
})

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const getVersionLabel = (versionId: 'current' | number) => {
  if (versionId === 'current') {
    return '当前版本'
  }
  const version = props.versions.find(v => v.id === versionId)
  return version ? `v${version.version}` : '未知版本'
}

watch([selectedVersionA, selectedVersionB], () => {
  if (selectedVersionA.value !== selectedVersionB.value) {
    isComparing.value = true
    setTimeout(() => {
      isComparing.value = false
    }, 300)
  }
})
</script>

<style scoped>
/* Use :deep() to apply styles to v-html content */
:deep(.diff-line-deleted), :deep(.diff-line-inserted), :deep(.diff-line-changed), :deep(.diff-line-empty) {
  padding: 0.1em 0.4em;
  min-height: 1.5em; /* Ensure empty lines are visible */
}

/* Line-level highlighting */
:deep(.diff-line-deleted) { background-color: #ffebe9; }
:deep(.diff-line-inserted) { background-color: #e6ffed; }
:deep(.diff-line-changed) { background-color: #fffacd; } /* Light yellow for changed lines */
:deep(.diff-line-empty) { background-color: #f1f5f9; }

/* Character-level highlighting */
:deep(.diff-char-deleted) {
  background-color: #ffcdd2;
  text-decoration: line-through;
}
:deep(.diff-char-inserted) {
  background-color: #c8e6c9;
  font-weight: bold;
}

/* Inline mode markers */
:deep(.diff-marker-inline) {
  display: inline-block;
  width: 1.2em;
  text-align: center;
  user-select: none;
}
:deep(.diff-line-deleted .diff-marker-inline) { color: #d32f2f; }
:deep(.diff-line-inserted .diff-marker-inline) { color: #388e3c; }

/* Font and scrollbar styles from before */
:deep(.font-mono) {
  font-family: 'Consolas', 'Monaco', 'Courier New', 'Menlo', monospace;
  line-height: 1.6;
}
.overflow-y-auto::-webkit-scrollbar { width: 6px; }
.overflow-y-auto::-webkit-scrollbar-track { background: #f1f5f9; border-radius: 3px; }
.overflow-y-auto::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 3px; }
.overflow-y-auto::-webkit-scrollbar-thumb:hover { background: #94a3b8; }
</style> 