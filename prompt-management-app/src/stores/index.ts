import { defineStore } from 'pinia'
import { 
  promptApi, 
  projectApi,
  moduleApi, 
  templateApi,
  tagApi,
  statsApi,
  draftApi,
  type Prompt as ApiPrompt, 
  type Module as ApiModule,
  type PromptVersion,
  type Tag,
  type Stats,
  type TemplateVariable,
  type Project,
  type Draft
} from '@/services/api'

// 为了保持兼容性，我们重新定义前端使用的Prompt接口
export interface Prompt {
  id: number;
  title: string;
  content: string;
  category?: string;
  tags?: string;
  project_id?: number;
  version?: number;
  name?: string;
  parent_id?: number;
  is_template?: boolean;
  template_variables?: TemplateVariable[];
  usage_count?: number;
  rating?: number;
  language?: string;
  author?: string;
  created_at?: string;
  updated_at?: string;
}

export interface Module {
  id: number;
  name: string;
  description?: string;
  status?: string;
  prompts?: string;
  dependencies?: string;
  version?: string;
  author?: string;
  created_at?: string;
  updated_at?: string;
}

export const useMainStore = defineStore('main', {
  state: () => ({
    prompts: [] as Prompt[],
    projects: [] as Project[],
    modules: [] as Module[],
    templates: [] as Prompt[],
    drafts: [] as Draft[],
    tags: [] as Tag[],
    stats: null as Stats | null,
    favorites: new Set<number>(),
    searchResults: [] as Prompt[],
    currentView: 'all' as 'all' | 'templates' | 'favorites',
    loading: false,
    error: null as string | null,
    selectedProjectId: null as number | null,
    sortOptions: {
      sortBy: 'created_at',
      order: 'desc'
    },
  }),
  actions: {
    // 项目相关操作
    async fetchProjects() {
      try {
        this.loading = true
        this.error = null
        this.projects = await projectApi.getAll()
      } catch (error) {
        this.error = error instanceof Error ? error.message : '获取项目失败'
        console.error('Failed to fetch projects:', error)
      } finally {
        this.loading = false
      }
    },
    async addProject(project: Omit<Project, 'id'>) {
      try {
        this.loading = true
        this.error = null
        const newProject = await projectApi.create(project)
        this.projects.push(newProject)
      } catch (error) {
        this.error = error instanceof Error ? error.message : '创建项目失败'
        console.error('Failed to create project:', error)
        throw error
      } finally {
        this.loading = false
      }
    },
    async updateProject(id: number, project: Partial<Project>) {
      try {
        this.loading = true
        this.error = null
        const updatedProject = await projectApi.update(id, project)
        const index = this.projects.findIndex(p => p.id === id)
        if (index !== -1) {
          this.projects[index] = { ...this.projects[index], ...updatedProject }
        }
      } catch (error) {
        this.error = error instanceof Error ? error.message : '更新项目失败'
        console.error('Failed to update project:', error)
        throw error
      } finally {
        this.loading = false
      }
    },
    async deleteProject(id: number) {
      try {
        this.loading = true
        this.error = null
        await projectApi.delete(id)
        this.projects = this.projects.filter(p => p.id !== id)
        if (this.selectedProjectId === id) {
          this.selectedProjectId = null
        }
      } catch (error) {
        this.error = error instanceof Error ? error.message : '删除项目失败'
        console.error('Failed to delete project:', error)
        throw error
      } finally {
        this.loading = false
      }
    },
    async selectProject(projectId: number | null) {
      this.selectedProjectId = projectId
      await this.fetchPrompts()
    },

    async movePromptToProject(promptId: number, projectId: number | null) {
      try {
        this.loading = true
        this.error = null
        await promptApi.move(promptId, projectId)
        // 移动成功后，如果当前项目视图受到影响，则移除该提示词
        const promptIndex = this.prompts.findIndex(p => p.id === promptId)
        if (promptIndex !== -1) {
          const prompt = this.prompts[promptIndex]
          if (prompt.project_id !== projectId && this.selectedProjectId !== null) {
             this.prompts.splice(promptIndex, 1)
          } else {
            // 或者直接更新其 project_id
            this.prompts[promptIndex].project_id = projectId || undefined
          }
        }
        // 更新项目计数（模拟）
        await this.fetchProjects() 
      } catch (error) {
        this.error = error instanceof Error ? error.message : '移动提示词失败'
        console.error('Failed to move prompt:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    // 提示词相关操作
    async fetchPrompts() {
      try {
        this.loading = true
        this.error = null
        this.prompts = await promptApi.getAll({ 
          sort_by: this.sortOptions.sortBy, 
          order: this.sortOptions.order,
          project_id: this.selectedProjectId,
        })
      } catch (error) {
        this.error = error instanceof Error ? error.message : '获取提示词失败'
        console.error('Failed to fetch prompts:', error)
      } finally {
        this.loading = false
      }
    },

    async addPrompt(prompt: Omit<Prompt, 'id' | 'created_at' | 'updated_at'>) {
      try {
        this.loading = true
        this.error = null
        const result = await promptApi.create(prompt)
        // 重新获取最新数据
        await this.fetchPrompts()
        return result
      } catch (error) {
        this.error = error instanceof Error ? error.message : '创建提示词失败'
        console.error('Failed to create prompt:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async deletePrompt(id: number) {
      try {
        this.loading = true
        this.error = null
        await promptApi.delete(id)
        // 从本地状态中移除
        this.prompts = this.prompts.filter(p => p.id !== id)
      } catch (error) {
        this.error = error instanceof Error ? error.message : '删除提示词失败'
        console.error('Failed to delete prompt:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async updatePrompt(prompt: Prompt) {
      try {
        this.loading = true
        this.error = null
        // 更新操作实际上是创建一个新版本
        const newVersion = await promptApi.createVersion(prompt.id, {
          title: prompt.title,
          content: prompt.content,
          change_description: '常规更新'
        })
        await this.fetchPrompts()
        return newVersion
      } catch (error) {
        this.error = error instanceof Error ? error.message : '更新提示词失败'
        console.error('Failed to update prompt:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async updatePromptContent(promptId: number, content: string) {
      try {
        this.loading = true;
        this.error = null;
        await promptApi.update(promptId, { content });
        // 找到本地的prompt并更新
        const index = this.prompts.findIndex(p => p.id === promptId);
        if (index !== -1) {
          this.prompts[index].content = content;
          this.prompts[index].updated_at = new Date().toISOString();
        }
        // 如果在搜索结果中，也更新
        const searchIndex = this.searchResults.findIndex(p => p.id === promptId);
        if (searchIndex !== -1) {
          this.searchResults[searchIndex].content = content;
          this.searchResults[searchIndex].updated_at = new Date().toISOString();
        }
      } catch (error) {
        this.error = error instanceof Error ? error.message : '更新提示词内容失败';
        console.error('Failed to update prompt content:', error);
        throw error;
      } finally {
        this.loading = false;
      }
    },

    // 模块相关操作
    async fetchModules() {
      try {
        this.loading = true
        this.error = null
        this.modules = await moduleApi.getAll()
      } catch (error) {
        this.error = error instanceof Error ? error.message : '获取模块失败'
        console.error('Failed to fetch modules:', error)
      } finally {
        this.loading = false
      }
    },

    async addModule(module: Omit<Module, 'id' | 'created_at' | 'updated_at'>) {
      try {
        this.loading = true
        this.error = null
        const result = await moduleApi.create(module)
        // 重新获取最新数据
        await this.fetchModules()
        return result
      } catch (error) {
        this.error = error instanceof Error ? error.message : '创建模块失败'
        console.error('Failed to create module:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async deleteModule(id: number) {
      try {
        this.loading = true
        this.error = null
        await moduleApi.delete(id)
        // 从本地状态中移除
        this.modules = this.modules.filter(m => m.id !== id)
      } catch (error) {
        this.error = error instanceof Error ? error.message : '删除模块失败'
        console.error('Failed to delete module:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async updateModule(module: Module) {
      try {
        this.loading = true
        this.error = null
        await moduleApi.update(module.id, module)
        // 重新获取最新数据
        await this.fetchModules()
      } catch (error) {
        this.error = error instanceof Error ? error.message : '更新模块失败'
        console.error('Failed to update module:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    // 模板相关操作
    async fetchTemplates() {
      try {
        this.loading = true
        this.error = null
        this.templates = await templateApi.getAll()
      } catch (error) {
        this.error = error instanceof Error ? error.message : '获取模板失败'
        console.error('Failed to fetch templates:', error)
      } finally {
        this.loading = false
      }
    },

    async cloneTemplate(id: number, data: {
      title?: string
      variables?: Record<string, string>
      author?: string
    }) {
      try {
        this.loading = true
        this.error = null
        const result = await templateApi.clone(id, data)
        await this.fetchPrompts()
        return result
      } catch (error) {
        this.error = error instanceof Error ? error.message : '克隆模板失败'
        console.error('Failed to clone template:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    // 版本控制相关操作
    async fetchPromptVersionsFromApi(id: number): Promise<PromptVersion[]> {
      try {
        this.loading = true
        this.error = null
        return await promptApi.getVersions(id)
      } catch (error) {
        this.error = error instanceof Error ? error.message : '获取版本历史失败'
        console.error('Failed to get prompt versions:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async createPromptVersion(id: number, data: {
      title: string
      content: string
      change_description?: string
      created_by?: string
    }) {
      try {
        this.loading = true
        this.error = null
        const result = await promptApi.createVersion(id, data)
        await this.fetchPrompts()
        return result
      } catch (error) {
        this.error = error instanceof Error ? error.message : '创建版本失败'
        console.error('Failed to create version:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    // 搜索相关操作
    async searchPrompts(params: {
      q?: string
      category?: string
      tags?: string
      is_template?: boolean
    }) {
      try {
        this.loading = true
        this.error = null
        const searchParams = {
          ...params,
          project_id: this.selectedProjectId,
          sort_by: this.sortOptions.sortBy,
          order: this.sortOptions.order,
        }
        this.searchResults = await promptApi.search(searchParams)
      } catch (error) {
        this.error = error instanceof Error ? error.message : '搜索提示词失败'
        console.error('Failed to search prompts:', error)
      } finally {
        this.loading = false
      }
    },

    // 收藏相关操作
    async toggleFavorite(id: number) {
      try {
        if (this.favorites.has(id)) {
          await promptApi.removeFavorite(id)
          this.favorites.delete(id)
        } else {
          await promptApi.addFavorite(id)
          this.favorites.add(id)
        }
      } catch (error) {
        this.error = error instanceof Error ? error.message : '收藏操作失败'
        console.error('Failed to toggle favorite:', error)
        throw error
      }
    },

    // 标签相关操作
    async fetchTags() {
      try {
        this.loading = true
        this.error = null
        this.tags = await tagApi.getAll()
      } catch (error) {
        this.error = error instanceof Error ? error.message : '获取标签失败'
        console.error('Failed to fetch tags:', error)
      } finally {
        this.loading = false
      }
    },

    // 统计相关操作
    async fetchStats() {
      try {
        this.loading = true
        this.error = null
        this.stats = await statsApi.get()
      } catch (error) {
        this.error = error instanceof Error ? error.message : '获取统计信息失败'
        console.error('Failed to fetch stats:', error)
      } finally {
        this.loading = false
      }
    },

    // 视图切换
    setCurrentView(view: 'all' | 'templates' | 'favorites') {
      this.currentView = view
    },

    // 清除错误
    clearError() {
      this.error = null
    },

    // 增加一个方法来更新排序选项并重新获取数据
    async setSort(sortBy: string, order: string) {
      this.sortOptions.sortBy = sortBy;
      this.sortOptions.order = order;
      // 触发数据重新获取，由组件决定具体行为
      // 例如，组件可以监听这个变化然后调用 fetchPrompts 或 searchPrompts
    },

    // 草稿相关操作
    async fetchDrafts() {
      try {
        this.loading = true
        this.error = null
        this.drafts = await draftApi.getAll()
      } catch (error) {
        this.error = error instanceof Error ? error.message : '获取草稿失败'
        console.error('Failed to fetch drafts:', error)
      } finally {
        this.loading = false
      }
    },

    async addDraft(draft: Omit<Draft, 'id' | 'created_at' | 'updated_at' | 'project_name'>) {
      try {
        this.loading = true
        this.error = null
        const result = await draftApi.create(draft)
        await this.fetchDrafts() // 重新获取列表
        return result
      } catch (error) {
        this.error = error instanceof Error ? error.message : '创建草稿失败'
        console.error('Failed to create draft:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async updateDraft(id: number, draft: Partial<Draft>) {
      try {
        this.loading = true
        this.error = null
        await draftApi.update(id, draft)
        await this.fetchDrafts() // 重新获取列表
      } catch (error) {
        this.error = error instanceof Error ? error.message : '更新草稿失败'
        console.error('Failed to update draft:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async deleteDraft(id: number) {
      try {
        this.loading = true
        this.error = null
        await draftApi.delete(id)
        this.drafts = this.drafts.filter(d => d.id !== id)
      } catch (error) {
        this.error = error instanceof Error ? error.message : '删除草稿失败'
        console.error('Failed to delete draft:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async publishDraft(id: number) {
      try {
        this.loading = true
        this.error = null
        const result = await draftApi.publish(id)
        // 移除已发布的草稿
        this.drafts = this.drafts.filter(d => d.id !== id)
        // 重新获取提示词列表
        await this.fetchPrompts()
        return result
      } catch (error) {
        this.error = error instanceof Error ? error.message : '发布草稿失败'
        console.error('Failed to publish draft:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async autoSaveDraft(id: number, content: string) {
      try {
        await draftApi.autoSave(id, content)
        // 更新本地状态中的自动保存内容
        const draftIndex = this.drafts.findIndex(d => d.id === id)
        if (draftIndex !== -1) {
          this.drafts[draftIndex].auto_save_content = content
          this.drafts[draftIndex].last_auto_save = new Date().toISOString()
        }
      } catch (error) {
        this.error = error instanceof Error ? error.message : '自动保存失败'
        console.error('Failed to auto-save draft:', error)
        throw error
      }
    },

    // 版本控制相关操作
    async updatePromptVersionName(versionId: number, name: string) {
      try {
        this.loading = true;
        this.error = null;
        await promptApi.updateVersionName(versionId, name);
      } catch (error) {
        this.error = error instanceof Error ? error.message : '更新版本名称失败';
        console.error('Failed to update prompt version name:', error);
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async revertToVersion(prompt: Prompt) {
      try {
        if (!prompt.parent_id && !prompt.version) return; // Cannot revert root or non-versioned prompt
        const parentId = prompt.parent_id || prompt.id;
        const newVersion = await promptApi.createVersion(parentId, {
          title: prompt.title,
          content: prompt.content,
          change_description: `从版本 ${prompt.version} 恢复`
        });
        await this.fetchPrompts();
        return newVersion;
      } catch (error) {
        this.error = error instanceof Error ? error.message : '恢复版本失败';
        console.error('Failed to revert to version:', error);
        throw error;
      }
    },

    async switchToVersion(promptId: number, version: Prompt) {
      try {
        this.loading = true;
        this.error = null;
        
        // 直接更新当前提示词的内容为选中版本的内容
        const updateData = {
          title: version.title,
          content: version.content,
          category: version.category,
          tags: version.tags
        };
        
        await promptApi.update(promptId, updateData);
        await this.fetchPrompts();
        
        return { success: true };
      } catch (error) {
        this.error = error instanceof Error ? error.message : '切换版本失败';
        console.error('Failed to switch to version:', error);
        throw error;
      } finally {
        this.loading = false;
      }
    },

  },
  getters: {
    // 获取加载状态
    isLoading: (state) => state.loading,
    // 获取错误信息
    errorMessage: (state) => state.error,
    
    // 根据当前视图过滤提示词
    filteredPrompts: (state) => {
      switch (state.currentView) {
        case 'templates':
          return state.prompts.filter(p => p.is_template)
        case 'favorites':
          return state.prompts.filter(p => state.favorites.has(p.id))
        default:
          return state.prompts.filter(p => !p.is_template)
      }
    },

    // 获取分类列表
    categories: (state) => {
      const categories = new Set<string>()
      state.prompts.forEach(p => {
        if (p.category && p.category.trim()) {
          categories.add(p.category.trim())
        }
      })
      return Array.from(categories).sort()
    },

    // 获取最受欢迎的模板
    popularTemplates: (state) => {
      return state.templates
        .slice()
        .sort((a, b) => (b.usage_count || 0) - (a.usage_count || 0))
        .slice(0, 6)
    },

    // 检查是否收藏
    isFavorite: (state) => (id: number) => state.favorites.has(id),

    getPromptById: (state) => (id: number | string) => {
      const promptId = typeof id === 'string' ? parseInt(id, 10) : id;
      return state.prompts.find(p => p.id === promptId);
    },

    // 获取一个 prompt 的所有版本
    getPromptVersions: (state) => (promptId: number) => {
      const prompt = state.prompts.find(p => p.id === promptId);
      if (!prompt) return [];
      
      const parentId = prompt.parent_id || prompt.id;
      return state.prompts
        .filter(p => p.id === parentId || p.parent_id === parentId)
        .sort((a, b) => (b.version || 0) - (a.version || 0));
    },
  }
}) 