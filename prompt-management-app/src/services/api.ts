// API服务类，用于与Flask后端通信
const API_BASE_URL = 'http://localhost:5000/api'

// 提示词接口类型定义
export interface Prompt {
  id: number
  title: string
  content: string
  category?: string
  tags?: string
  version?: number
  name?: string
  parent_id?: number
  is_template?: boolean
  template_variables?: TemplateVariable[]
  usage_count?: number
  rating?: number
  language?: string
  author?: string
  created_at?: string
  updated_at?: string
  project_id?: number
}

// 新增：项目接口类型定义
export interface Project {
  id: number
  name: string
  description?: string
  created_at?: string
  prompt_count?: number
}

// 模板变量接口
export interface TemplateVariable {
  name: string
  type: 'text' | 'number' | 'select' | 'textarea'
  default_value?: string
  description?: string
  is_required?: boolean
  options?: string[]
}

// 版本历史接口
export interface PromptVersion {
  id: number
  prompt_id: number
  version: number
  title: string
  content: string
  change_description?: string
  created_by?: string
  name?: string
  created_at: string
}

// 统计信息接口
export interface Stats {
  total_prompts: number
  total_templates: number
  total_modules: number
  total_favorites: number
  categories: Array<{category: string, count: number}>
  recent_prompts: Array<{id: number, title: string, created_at: string}>
}

// 标签接口
export interface Tag {
  id: number
  name: string
  color: string
  usage_count: number
  created_at: string
}

// 模块接口类型定义
export interface Module {
  id: number
  name: string
  description?: string
  status?: string
  prompts?: string
  dependencies?: string
  version?: string
  author?: string
  created_at?: string
  updated_at?: string
}

// 草稿接口类型定义
export interface Draft {
  id: number
  title?: string
  content?: string
  category?: string
  tags?: string
  project_id?: number
  project_name?: string
  author?: string
  language?: string
  auto_save_content?: string
  last_auto_save?: string
  created_at?: string
  updated_at?: string
}

// HTTP请求工具函数
async function apiRequest(endpoint: string, options: RequestInit = {}) {
  const url = `${API_BASE_URL}${endpoint}`
  const config: RequestInit = {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  }

  try {
    const response = await fetch(url, config)
    const data = await response.json()

    if (!response.ok) {
      throw new Error(data.error || `HTTP error! status: ${response.status}`)
    }

    return data
  } catch (error) {
    console.error('API request failed:', error)
    throw error
  }
}

// 提示词相关API
export const promptApi = {
  // 获取所有提示词
  async getAll(params: { sort_by?: string; order?: string; project_id?: number | null } = {}): Promise<Prompt[]> {
    const searchParams = new URLSearchParams();
    if (params.sort_by) searchParams.append('sort_by', params.sort_by);
    if (params.order) searchParams.append('order', params.order);
    if (params.project_id) searchParams.append('project_id', String(params.project_id));
    const queryString = searchParams.toString();
    return apiRequest(`/prompts${queryString ? `?${queryString}` : ''}`);
  },

  // 获取单个提示词
  async getById(id: number): Promise<Prompt> {
    return apiRequest(`/prompts/${id}`)
  },

  // 创建新提示词
  async create(prompt: Omit<Prompt, 'id' | 'created_at' | 'updated_at'>): Promise<{id: number, message: string}> {
    return apiRequest('/prompts', {
      method: 'POST',
      body: JSON.stringify(prompt),
    })
  },

  // 更新提示词
  async update(id: number, prompt: Partial<Prompt>): Promise<{message: string}> {
    return apiRequest(`/prompts/${id}`, {
      method: 'PUT',
      body: JSON.stringify(prompt),
    })
  },

  // 删除提示词
  async delete(id: number): Promise<{message: string}> {
    return apiRequest(`/prompts/${id}`, {
      method: 'DELETE',
    })
  },

  // 移动提示词到项目
  async move(promptId: number, projectId: number | null): Promise<{message: string}> {
    return apiRequest(`/prompts/${promptId}/move`, {
      method: 'PUT',
      body: JSON.stringify({ project_id: projectId }),
    })
  },

  // 获取提示词版本历史
  async getVersions(id: number): Promise<PromptVersion[]> {
    return apiRequest(`/prompts/${id}/versions`)
  },

  // 创建新版本
  async createVersion(id: number, data: {
    title: string
    content: string
    change_description?: string
    created_by?: string
    name?: string
  }): Promise<{message: string, version: number}> {
    return apiRequest(`/prompts/${id}/versions`, {
      method: 'POST',
      body: JSON.stringify(data),
    })
  },

  // 更新版本名称
  async updateVersionName(versionId: number, name: string): Promise<{message: string}> {
    return apiRequest(`/prompts/versions/${versionId}/name`, {
      method: 'PUT',
      body: JSON.stringify({ name }),
    })
  },

  // 搜索提示词
  async search(params: {
    q?: string
    category?: string
    tags?: string
    is_template?: boolean
    sort_by?: string;
    order?: string;
    project_id?: number | null;
  }): Promise<Prompt[]> {
    const searchParams = new URLSearchParams()
    if (params.q) searchParams.append('q', params.q)
    if (params.category) searchParams.append('category', params.category)
    if (params.tags) searchParams.append('tags', params.tags)
    if (params.is_template !== undefined) searchParams.append('is_template', String(params.is_template))
    if (params.sort_by) searchParams.append('sort_by', params.sort_by);
    if (params.order) searchParams.append('order', params.order);
    if (params.project_id) searchParams.append('project_id', String(params.project_id));
    
    return apiRequest(`/prompts/search?${searchParams.toString()}`)
  },

  // 收藏/取消收藏
  async addFavorite(id: number, userId = 'default'): Promise<{message: string}> {
    return apiRequest(`/prompts/${id}/favorite`, {
      method: 'POST',
      body: JSON.stringify({ user_id: userId }),
    })
  },

  async removeFavorite(id: number, userId = 'default'): Promise<{message: string}> {
    return apiRequest(`/prompts/${id}/favorite?user_id=${userId}`, {
      method: 'DELETE',
    })
  },
}

// 模块相关API
export const moduleApi = {
  // 获取所有模块
  async getAll(): Promise<Module[]> {
    return apiRequest('/modules')
  },

  // 创建新模块
  async create(module: Omit<Module, 'id' | 'created_at' | 'updated_at'>): Promise<{id: number, message: string}> {
    return apiRequest('/modules', {
      method: 'POST',
      body: JSON.stringify(module),
    })
  },

  // 更新模块
  async update(id: number, module: Partial<Module>): Promise<{message: string}> {
    return apiRequest(`/modules/${id}`, {
      method: 'PUT',
      body: JSON.stringify(module),
    })
  },

  // 删除模块
  async delete(id: number): Promise<{message: string}> {
    return apiRequest(`/modules/${id}`, {
      method: 'DELETE',
    })
  },
}

// 模板相关API
export const templateApi = {
  // 获取所有模板
  async getAll(): Promise<Prompt[]> {
    return apiRequest('/templates')
  },

  // 克隆模板
  async clone(id: number, data: {
    title?: string
    variables?: Record<string, string>
    author?: string
  }): Promise<{id: number, message: string}> {
    return apiRequest(`/templates/${id}/clone`, {
      method: 'POST',
      body: JSON.stringify(data),
    })
  },
}

// 标签相关API
export const tagApi = {
  // 获取所有标签
  async getAll(): Promise<Tag[]> {
    return apiRequest('/tags')
  },
}

// 统计相关API
export const statsApi = {
  // 获取统计信息
  async get(): Promise<Stats> {
    return apiRequest('/stats')
  },
}

// 导入导出相关API
export const importExportApi = {
  // 导出提示词
  async exportPrompts(params: {
    format?: 'json' | 'csv' | 'markdown'
    category?: string
    ids?: number[]
  } = {}): Promise<Blob> {
    const searchParams = new URLSearchParams()
    if (params.format) searchParams.append('format', params.format)
    if (params.category) searchParams.append('category', params.category)
    if (params.ids?.length) searchParams.append('ids', params.ids.join(','))
    
    const response = await fetch(`${API_BASE_URL}/export/prompts?${searchParams.toString()}`)
    if (!response.ok) {
      throw new Error(`导出失败: ${response.statusText}`)
    }
    return response.blob()
  },

  // 导入提示词
  async importPrompts(file: File): Promise<{
    message: string
    imported_count: number
    skipped_count: number
    total_processed: number
    errors?: string[]
  }> {
    const formData = new FormData()
    formData.append('file', file)
    
    const response = await fetch(`${API_BASE_URL}/import/prompts`, {
      method: 'POST',
      body: formData,
    })
    
    const data = await response.json()
    if (!response.ok) {
      throw new Error(data.error || '导入失败')
    }
    
    return data
  },

  // 批量操作
  async batchOperation(action: string, ids: number[], extraData?: any): Promise<{
    message: string
    affected_count: number
  }> {
    return apiRequest('/prompts/batch', {
      method: 'POST',
      body: JSON.stringify({
        action,
        ids,
        ...extraData
      }),
    })
  },
}

// 项目相关API
export const projectApi = {
  // 获取所有项目
  async getAll(): Promise<Project[]> {
    return apiRequest('/projects')
  },

  // 创建新项目
  async create(project: Omit<Project, 'id' | 'created_at' | 'prompt_count'>): Promise<Project> {
    return apiRequest('/projects', {
      method: 'POST',
      body: JSON.stringify(project),
    })
  },

  // 更新项目
  async update(id: number, project: Partial<Omit<Project, 'id' | 'created_at' | 'prompt_count'>>): Promise<Project> {
    return apiRequest(`/projects/${id}`, {
      method: 'PUT',
      body: JSON.stringify(project),
    })
  },

  // 删除项目
  async delete(id: number): Promise<{ message: string }> {
    return apiRequest(`/projects/${id}`, {
      method: 'DELETE',
    })
  },
}

// 草稿箱相关API
export const draftApi = {
  // 获取所有草稿
  async getAll(): Promise<Draft[]> {
    return apiRequest('/drafts')
  },

  // 获取单个草稿
  async getById(id: number): Promise<Draft> {
    return apiRequest(`/drafts/${id}`)
  },

  // 创建新草稿
  async create(draft: Omit<Draft, 'id' | 'created_at' | 'updated_at' | 'project_name'>): Promise<{id: number, message: string}> {
    return apiRequest('/drafts', {
      method: 'POST',
      body: JSON.stringify(draft),
    })
  },

  // 更新草稿
  async update(id: number, draft: Partial<Draft>): Promise<{message: string}> {
    return apiRequest(`/drafts/${id}`, {
      method: 'PUT',
      body: JSON.stringify(draft),
    })
  },

  // 自动保存草稿
  async autoSave(id: number, content: string): Promise<{message: string}> {
    return apiRequest(`/drafts/${id}/auto-save`, {
      method: 'PUT',
      body: JSON.stringify({ content }),
    })
  },

  // 删除草稿
  async delete(id: number): Promise<{message: string}> {
    return apiRequest(`/drafts/${id}`, {
      method: 'DELETE',
    })
  },

  // 发布草稿为正式提示词
  async publish(id: number): Promise<{id: number, message: string}> {
    return apiRequest(`/drafts/${id}/publish`, {
      method: 'POST',
    })
  },
} 