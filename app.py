from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 错误处理
@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': '请求格式错误'}), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': '资源不存在'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': '服务器内部错误'}), 500

# 数据库文件路径
DB_PATH = 'prompts.db'

def init_db():
    """初始化数据库"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 创建提示词表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prompts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            category TEXT,
            tags TEXT,
            version INTEGER DEFAULT 1,
            parent_id INTEGER,
            is_template BOOLEAN DEFAULT 0,
            template_variables TEXT,
            usage_count INTEGER DEFAULT 0,
            rating REAL DEFAULT 0,
            language TEXT DEFAULT 'zh',
            author TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (parent_id) REFERENCES prompts (id)
        )
    ''')
    
    # 创建模块表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS modules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            status TEXT DEFAULT 'active',
            prompts TEXT,
            dependencies TEXT,
            version TEXT DEFAULT '1.0.0',
            author TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 创建提示词版本历史表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prompt_versions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prompt_id INTEGER NOT NULL,
            version INTEGER NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            change_description TEXT,
            created_by TEXT,
            name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (prompt_id) REFERENCES prompts (id)
        )
    ''')
    
    # 添加 name 字段（如果不存在）
    try:
        cursor.execute('ALTER TABLE prompt_versions ADD COLUMN name TEXT')
    except sqlite3.OperationalError:
        # 字段已存在，跳过
        pass
    
    # 创建模板变量表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS template_variables (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prompt_id INTEGER NOT NULL,
            variable_name TEXT NOT NULL,
            variable_type TEXT DEFAULT 'text',
            default_value TEXT,
            description TEXT,
            is_required BOOLEAN DEFAULT 0,
            FOREIGN KEY (prompt_id) REFERENCES prompts (id)
        )
    ''')
    
    # 创建收藏表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS favorites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prompt_id INTEGER NOT NULL,
            user_id TEXT DEFAULT 'default',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (prompt_id) REFERENCES prompts (id)
        )
    ''')
    
    # 创建标签表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            color TEXT DEFAULT '#3B82F6',
            usage_count INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 创建项目表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 创建草稿箱表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS drafts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            content TEXT,
            category TEXT,
            tags TEXT,
            project_id INTEGER,
            author TEXT,
            language TEXT DEFAULT 'zh',
            auto_save_content TEXT,
            last_auto_save TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (project_id) REFERENCES projects (id)
        )
    ''')

    # 为 prompts 表添加 project_id 字段
    try:
        cursor.execute('ALTER TABLE prompts ADD COLUMN project_id INTEGER REFERENCES projects(id)')
    except sqlite3.OperationalError:
        pass # 字段已存在
    
    conn.commit()
    conn.close()

def get_db_connection():
    """获取数据库连接"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# 提示词相关API
@app.route('/api/prompts', methods=['GET'])
def get_prompts():
    """获取所有提示词"""
    conn = get_db_connection()
    
    # 支持根据查询参数排序和筛选
    sort_by = request.args.get('sort_by', 'created_at')
    order = request.args.get('order', 'desc')
    project_id_str = request.args.get('project_id')

    # 允许排序的字段白名单，防止SQL注入
    allowed_sort_fields = {
        'created_at': 'created_at',
        'updated_at': 'updated_at',
        'title': 'title',
        'usage_count': 'usage_count'
    }
    sort_column = allowed_sort_fields.get(sort_by, 'created_at')
    order_clause = 'ASC' if order.lower() == 'asc' else 'DESC'

    # 构建查询
    sql = 'SELECT * FROM prompts'
    params = []
    where_clauses = []

    if project_id_str is not None and project_id_str != 'null' and project_id_str != '':
        try:
            project_id = int(project_id_str)
            where_clauses.append('project_id = ?')
            params.append(project_id)
        except (ValueError, TypeError):
            # 忽略无效的 project_id
            pass
    
    # 也可以处理 'null' 的情况，即未分配项目的提示词
    # elif project_id_str == 'null':
    #     where_clauses.append('project_id IS NULL')

    if where_clauses:
        sql += ' WHERE ' + ' AND '.join(where_clauses)

    sql += f' ORDER BY {sort_column} {order_clause}'
    
    prompts = conn.execute(sql, params).fetchall()
    conn.close()
    
    return jsonify([dict(prompt) for prompt in prompts])

@app.route('/api/prompts', methods=['POST'])
def create_prompt():
    """创建新提示词"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': '请求数据不能为空'}), 400
    
    # 支持 'name' 和 'title' 两种字段名
    title = data.get('title') or data.get('name')
    if not title or not title.strip():
        return jsonify({'error': '标题不能为空'}), 400
    
    if 'content' not in data or not data['content'] or not data['content'].strip():
        return jsonify({'error': '内容不能为空'}), 400
    
    # 处理tags字段 - 支持数组和字符串两种格式
    tags = data.get('tags', '')
    if isinstance(tags, list):
        tags = ','.join(str(tag).strip() for tag in tags if tag)
    elif not isinstance(tags, str):
        tags = str(tags)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO prompts (title, content, category, tags, version, parent_id, 
                           is_template, template_variables, language, author, project_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (title.strip(), data['content'].strip(), 
          data.get('category', '').strip() if data.get('category') else '', 
          tags.strip(),
          data.get('version', 1),
          data.get('parent_id'),
          data.get('is_template', False),
          json.dumps(data.get('template_variables', [])),
          data.get('language', 'zh'),
          data.get('author', ''),
          data.get('project_id'),
         ))
    
    prompt_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return jsonify({'id': prompt_id, 'message': '提示词创建成功'}), 201

@app.route('/api/prompts/<int:prompt_id>', methods=['GET'])
def get_prompt(prompt_id):
    """获取单个提示词"""
    conn = get_db_connection()
    prompt = conn.execute('SELECT * FROM prompts WHERE id = ?', (prompt_id,)).fetchone()
    conn.close()
    
    if prompt is None:
        return jsonify({'error': '提示词不存在'}), 404
    
    return jsonify(dict(prompt))

@app.route('/api/prompts/<int:prompt_id>', methods=['PUT'])
def update_prompt(prompt_id):
    """更新提示词"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': '请求数据不能为空'}), 400
    
    # 验证必需字段
    title = data.get('title') or data.get('name')
    if title is not None and not title.strip():
        return jsonify({'error': '标题不能为空'}), 400
    
    if 'content' in data and not data['content'].strip():
        return jsonify({'error': '内容不能为空'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 首先检查提示词是否存在
    existing_prompt = cursor.execute('SELECT * FROM prompts WHERE id = ?', (prompt_id,)).fetchone()
    if not existing_prompt:
        conn.close()
        return jsonify({'error': '提示词不存在'}), 404
    
    # 构建更新字段，只更新提供的字段
    update_fields = []
    update_values = []
    
    if title is not None:
        update_fields.append('title = ?')
        update_values.append(title)
        
    if data.get('content') is not None:
        update_fields.append('content = ?')
        update_values.append(data['content'])

    # 允许更新 project_id
    if 'project_id' in data:
        update_fields.append('project_id = ?')
        update_values.append(data['project_id'])

    if not update_fields:
        # 如果没有提供任何可更新的字段
        conn.close()
        return jsonify({'message': '没有提供可更新的字段'}), 200
        
    # 添加 updated_at
    update_fields.append('updated_at = ?')
    update_values.append(datetime.utcnow().isoformat())
    
    sql = f"UPDATE prompts SET {', '.join(update_fields)} WHERE id = ?"
    cursor.execute(sql, update_values + [prompt_id])
    
    conn.commit()
    conn.close()
    
    return jsonify({'message': '提示词更新成功'})

@app.route('/api/prompts/<int:prompt_id>', methods=['DELETE'])
def delete_prompt(prompt_id):
    """删除提示词"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM prompts WHERE id = ?', (prompt_id,))
    
    if cursor.rowcount == 0:
        conn.close()
        return jsonify({'error': '提示词不存在'}), 404
    
    conn.commit()
    conn.close()
    
    return jsonify({'message': '提示词删除成功'})

# 模块相关API
@app.route('/api/modules', methods=['GET'])
def get_modules():
    """获取所有模块"""
    conn = get_db_connection()
    modules = conn.execute('SELECT * FROM modules ORDER BY created_at DESC').fetchall()
    conn.close()
    
    return jsonify([dict(module) for module in modules])

@app.route('/api/modules', methods=['POST'])
def create_module():
    """创建新模块"""
    data = request.get_json()
    
    if not data or 'name' not in data:
        return jsonify({'error': '模块名称不能为空'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO modules (name, description, status)
        VALUES (?, ?, ?)
    ''', (data['name'], data.get('description', ''), data.get('status', 'active')))
    
    module_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return jsonify({'id': module_id, 'message': '模块创建成功'}), 201

@app.route('/api/modules/<int:module_id>', methods=['PUT'])
def update_module(module_id):
    """更新模块"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': '请求数据不能为空'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE modules 
        SET name = ?, description = ?, status = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    ''', (data.get('name'), data.get('description'), data.get('status'), module_id))
    
    if cursor.rowcount == 0:
        conn.close()
        return jsonify({'error': '模块不存在'}), 404
    
    conn.commit()
    conn.close()
    
    return jsonify({'message': '模块更新成功'})

@app.route('/api/modules/<int:module_id>', methods=['DELETE'])
def delete_module(module_id):
    """删除模块"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM modules WHERE id = ?', (module_id,))
    
    if cursor.rowcount == 0:
        conn.close()
        return jsonify({'error': '模块不存在'}), 404
    
    conn.commit()
    conn.close()
    
    return jsonify({'message': '模块删除成功'})

# 版本控制相关API
@app.route('/api/prompts/<int:prompt_id>/versions', methods=['GET'])
def get_prompt_versions(prompt_id):
    """获取提示词版本历史"""
    conn = get_db_connection()
    versions = conn.execute('''
        SELECT * FROM prompt_versions WHERE prompt_id = ? 
        ORDER BY version DESC
    ''', (prompt_id,)).fetchall()
    conn.close()
    
    return jsonify([dict(version) for version in versions])

@app.route('/api/prompts/<int:prompt_id>/versions', methods=['POST'])
def create_prompt_version(prompt_id):
    """创建新版本"""
    data = request.get_json()
    
    if not data or 'title' not in data or 'content' not in data:
        return jsonify({'error': '标题和内容不能为空'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 获取当前最大版本号
    current_version = cursor.execute('''
        SELECT MAX(version) FROM prompts WHERE id = ? OR parent_id = ?
    ''', (prompt_id, prompt_id)).fetchone()[0] or 1
    
    new_version = current_version + 1
    
    # 创建版本历史记录
    cursor.execute('''
        INSERT INTO prompt_versions (prompt_id, version, title, content, change_description, created_by, name)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (prompt_id, new_version, data['title'], data['content'], 
          data.get('change_description', ''), data.get('created_by', ''), data.get('name', '')))
    
    # 更新主提示词
    cursor.execute('''
        UPDATE prompts SET title = ?, content = ?, version = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    ''', (data['title'], data['content'], new_version, prompt_id))
    
    conn.commit()
    conn.close()
    
    return jsonify({'message': '版本创建成功', 'version': new_version}), 201

@app.route('/api/prompts/versions/<int:version_id>/name', methods=['PUT'])
def update_version_name(version_id):
    """更新版本名称"""
    data = request.get_json()
    
    if not data or 'name' not in data:
        return jsonify({'error': '名称不能为空'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 更新版本名称
    cursor.execute('''
        UPDATE prompt_versions SET name = ? WHERE id = ?
    ''', (data['name'], version_id))
    
    if cursor.rowcount == 0:
        conn.close()
        return jsonify({'error': '版本不存在'}), 404
    
    conn.commit()
    conn.close()
    
    return jsonify({'message': '版本名称更新成功'}), 200

# 模板相关API
@app.route('/api/templates', methods=['GET'])
def get_templates():
    """获取所有模板"""
    conn = get_db_connection()
    templates = conn.execute('''
        SELECT * FROM prompts WHERE is_template = 1 
        ORDER BY usage_count DESC, created_at DESC
    ''').fetchall()
    conn.close()
    
    return jsonify([dict(template) for template in templates])

@app.route('/api/templates/<int:template_id>/clone', methods=['POST'])
def clone_template(template_id):
    """克隆模板创建新提示词"""
    data = request.get_json()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 获取模板信息
    template = cursor.execute('SELECT * FROM prompts WHERE id = ? AND is_template = 1', 
                            (template_id,)).fetchone()
    
    if not template:
        conn.close()
        return jsonify({'error': '模板不存在'}), 404
    
    # 处理模板变量替换
    content = template['content']
    template_vars = json.loads(template['template_variables'] or '[]')
    
    for var in template_vars:
        if var['name'] in data.get('variables', {}):
            placeholder = f"{{{{{var['name']}}}}}"
            content = content.replace(placeholder, data['variables'][var['name']])
    
    # 创建新提示词
    cursor.execute('''
        INSERT INTO prompts (title, content, category, tags, parent_id, author)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (data.get('title', template['title'] + ' (副本)'), content,
          template['category'], template['tags'], template_id, 
          data.get('author', '')))
    
    # 增加模板使用次数
    cursor.execute('UPDATE prompts SET usage_count = usage_count + 1 WHERE id = ?', 
                  (template_id,))
    
    new_prompt_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return jsonify({'id': new_prompt_id, 'message': '基于模板创建成功'}), 201

# 收藏相关API
@app.route('/api/prompts/<int:prompt_id>/favorite', methods=['POST'])
def add_favorite(prompt_id):
    """添加收藏"""
    data = request.get_json()
    user_id = data.get('user_id', 'default')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 检查是否已收藏
    existing = cursor.execute('''
        SELECT id FROM favorites WHERE prompt_id = ? AND user_id = ?
    ''', (prompt_id, user_id)).fetchone()
    
    if existing:
        conn.close()
        return jsonify({'error': '已经收藏过了'}), 400
    
    cursor.execute('''
        INSERT INTO favorites (prompt_id, user_id) VALUES (?, ?)
    ''', (prompt_id, user_id))
    
    conn.commit()
    conn.close()
    
    return jsonify({'message': '收藏成功'}), 201

@app.route('/api/prompts/<int:prompt_id>/favorite', methods=['DELETE'])
def remove_favorite(prompt_id):
    """取消收藏"""
    user_id = request.args.get('user_id', 'default')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        DELETE FROM favorites WHERE prompt_id = ? AND user_id = ?
    ''', (prompt_id, user_id))
    
    conn.commit()
    conn.close()
    
    return jsonify({'message': '取消收藏成功'})

# 搜索和过滤API
@app.route('/api/prompts/search', methods=['GET'])
def search_prompts():
    """搜索提示词"""
    query = request.args.get('q', '')
    category = request.args.get('category', '')
    tags = request.args.get('tags', '')
    is_template = request.args.get('is_template', '')
    
    conn = get_db_connection()
    
    sql = 'SELECT * FROM prompts WHERE 1=1'
    params = []
    
    if query:
        sql += ' AND (title LIKE ? OR content LIKE ?)'
        params.extend([f'%{query}%', f'%{query}%'])
    
    if category:
        sql += ' AND category = ?'
        params.append(category)
    
    if tags:
        sql += ' AND tags LIKE ?'
        params.append(f'%{tags}%')
    
    if is_template:
        sql += ' AND is_template = ?'
        params.append(1 if is_template.lower() == 'true' else 0)
    
    # 处理排序参数
    sort_by = request.args.get('sort_by', 'created_at')
    order = request.args.get('order', 'desc')
    allowed_sort_fields = {
        'created_at': 'created_at',
        'updated_at': 'updated_at',
        'title': 'title',
        'usage_count': 'usage_count'
    }
    sort_column = allowed_sort_fields.get(sort_by, 'created_at')
    order_clause = 'ASC' if order.lower() == 'asc' else 'DESC'

    sql += f' ORDER BY {sort_column} {order_clause}'
    
    prompts = conn.execute(sql, params).fetchall()
    conn.close()
    
    return jsonify([dict(prompt) for prompt in prompts])

# 标签管理API
@app.route('/api/tags', methods=['GET'])
def get_tags():
    """获取所有标签"""
    conn = get_db_connection()
    tags = conn.execute('SELECT * FROM tags ORDER BY usage_count DESC').fetchall()
    conn.close()
    
    return jsonify([dict(tag) for tag in tags])

# 统计API
@app.route('/api/stats', methods=['GET'])
def get_stats():
    """获取统计信息"""
    conn = get_db_connection()
    
    stats = {
        'total_prompts': conn.execute('SELECT COUNT(*) FROM prompts').fetchone()[0],
        'total_templates': conn.execute('SELECT COUNT(*) FROM prompts WHERE is_template = 1').fetchone()[0],
        'total_modules': conn.execute('SELECT COUNT(*) FROM modules').fetchone()[0],
        'total_favorites': conn.execute('SELECT COUNT(*) FROM favorites').fetchone()[0],
        'categories': [dict(row) for row in conn.execute('''
            SELECT category, COUNT(*) as count 
            FROM prompts 
            WHERE category != '' 
            GROUP BY category 
            ORDER BY count DESC
        ''').fetchall()],
        'recent_prompts': [dict(row) for row in conn.execute('''
            SELECT id, title, created_at 
            FROM prompts 
            ORDER BY created_at DESC 
            LIMIT 5
        ''').fetchall()]
    }
    
    conn.close()
    return jsonify(stats)

# 导入导出相关API
@app.route('/api/export/prompts', methods=['GET'])
def export_prompts():
    """导出提示词"""
    format_type = request.args.get('format', 'json')
    category = request.args.get('category', '')
    ids = request.args.get('ids', '')
    
    conn = get_db_connection()
    
    # 构建查询条件
    sql = 'SELECT * FROM prompts WHERE 1=1'
    params = []
    
    if category:
        sql += ' AND category = ?'
        params.append(category)
    
    if ids:
        id_list = [int(id.strip()) for id in ids.split(',') if id.strip().isdigit()]
        if id_list:
            placeholders = ','.join(['?'] * len(id_list))
            sql += f' AND id IN ({placeholders})'
            params.extend(id_list)
    
    prompts = conn.execute(sql, params).fetchall()
    conn.close()
    
    # 转换为字典列表
    prompts_data = [dict(prompt) for prompt in prompts]
    
    if format_type == 'csv':
        import csv
        import io
        
        output = io.StringIO()
        if prompts_data:
            writer = csv.DictWriter(output, fieldnames=prompts_data[0].keys())
            writer.writeheader()
            writer.writerows(prompts_data)
        
        response = app.response_class(
            output.getvalue(),
            mimetype='text/csv',
            headers={"Content-Disposition": "attachment;filename=prompts.csv"}
        )
        return response
    
    elif format_type == 'markdown':
        markdown_content = "# 提示词导出\n\n"
        for prompt in prompts_data:
            markdown_content += f"## {prompt['title']}\n\n"
            markdown_content += f"**分类**: {prompt.get('category', '未分类')}\n\n"
            markdown_content += f"**标签**: {prompt.get('tags', '无')}\n\n"
            markdown_content += f"**内容**:\n```\n{prompt['content']}\n```\n\n"
            markdown_content += "---\n\n"
        
        response = app.response_class(
            markdown_content,
            mimetype='text/markdown',
            headers={"Content-Disposition": "attachment;filename=prompts.md"}
        )
        return response
    
    else:  # JSON format
        export_data = {
            'export_info': {
                'timestamp': datetime.now().isoformat(),
                'total_count': len(prompts_data),
                'format': 'json',
                'version': '1.0'
            },
            'prompts': prompts_data
        }
        
        response = app.response_class(
            json.dumps(export_data, indent=2, ensure_ascii=False),
            mimetype='application/json',
            headers={"Content-Disposition": "attachment;filename=prompts.json"}
        )
        return response

@app.route('/api/import/prompts', methods=['POST'])
def import_prompts():
    """导入提示词"""
    if 'file' not in request.files:
        return jsonify({'error': '未选择文件'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': '未选择文件'}), 400
    
    try:
        content = file.read().decode('utf-8')
        filename = file.filename.lower()
        
        imported_count = 0
        skipped_count = 0
        errors = []
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if filename.endswith('.json'):
            # JSON格式导入
            data = json.loads(content)
            
            # 兼容不同格式的JSON
            if 'prompts' in data:
                prompts_data = data['prompts']
            elif isinstance(data, list):
                prompts_data = data
            else:
                prompts_data = [data]
            
            for prompt_data in prompts_data:
                try:
                    # 检查是否已存在
                    existing = cursor.execute(
                        'SELECT id FROM prompts WHERE title = ? AND content = ?',
                        (prompt_data.get('title', ''), prompt_data.get('content', ''))
                    ).fetchone()
                    
                    if existing:
                        skipped_count += 1
                        continue
                    
                    # 插入新提示词
                    cursor.execute('''
                        INSERT INTO prompts (title, content, category, tags, author, language, is_template)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        prompt_data.get('title', '未命名'),
                        prompt_data.get('content', ''),
                        prompt_data.get('category', ''),
                        prompt_data.get('tags', ''),
                        prompt_data.get('author', ''),
                        prompt_data.get('language', 'zh'),
                        prompt_data.get('is_template', False)
                    ))
                    
                    imported_count += 1
                    
                except Exception as e:
                    errors.append(f"导入提示词失败: {str(e)}")
        
        elif filename.endswith('.csv'):
            # CSV格式导入
            import csv
            import io
            
            csv_data = csv.DictReader(io.StringIO(content))
            
            for row in csv_data:
                try:
                    # 检查是否已存在
                    existing = cursor.execute(
                        'SELECT id FROM prompts WHERE title = ? AND content = ?',
                        (row.get('title', ''), row.get('content', ''))
                    ).fetchone()
                    
                    if existing:
                        skipped_count += 1
                        continue
                    
                    # 插入新提示词
                    cursor.execute('''
                        INSERT INTO prompts (title, content, category, tags, author, language, is_template)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        row.get('title', '未命名'),
                        row.get('content', ''),
                        row.get('category', ''),
                        row.get('tags', ''),
                        row.get('author', ''),
                        row.get('language', 'zh'),
                        row.get('is_template', '').lower() in ['true', '1', 'yes']
                    ))
                    
                    imported_count += 1
                    
                except Exception as e:
                    errors.append(f"导入提示词失败: {str(e)}")
        
        else:
            conn.close()
            return jsonify({'error': '不支持的文件格式，请使用 JSON 或 CSV 格式'}), 400
        
        conn.commit()
        conn.close()
        
        result = {
            'message': '导入完成',
            'imported_count': imported_count,
            'skipped_count': skipped_count,
            'total_processed': imported_count + skipped_count
        }
        
        if errors:
            result['errors'] = errors
        
        return jsonify(result)
        
    except json.JSONDecodeError:
        return jsonify({'error': 'JSON 格式错误'}), 400
    except Exception as e:
        return jsonify({'error': f'导入失败: {str(e)}'}), 500

# 批量操作API
@app.route('/api/prompts/batch', methods=['POST'])
def batch_operations():
    """批量操作提示词"""
    data = request.get_json()
    
    if not data or 'action' not in data or 'ids' not in data:
        return jsonify({'error': '缺少必要参数'}), 400
    
    action = data['action']
    ids = data['ids']
    
    if not isinstance(ids, list) or not ids:
        return jsonify({'error': 'ids 必须是非空数组'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        if action == 'delete':
            # 批量删除
            placeholders = ','.join(['?'] * len(ids))
            cursor.execute(f'DELETE FROM prompts WHERE id IN ({placeholders})', ids)
            affected_rows = cursor.rowcount
            
        elif action == 'update_category':
            # 批量更新分类
            category = data.get('category', '')
            placeholders = ','.join(['?'] * len(ids))
            cursor.execute(
                f'UPDATE prompts SET category = ?, updated_at = CURRENT_TIMESTAMP WHERE id IN ({placeholders})',
                [category] + ids
            )
            affected_rows = cursor.rowcount
            
        elif action == 'add_tag':
            # 批量添加标签
            tag = data.get('tag', '')
            if not tag:
                return jsonify({'error': '标签不能为空'}), 400
            
            affected_rows = 0
            for prompt_id in ids:
                prompt = cursor.execute('SELECT tags FROM prompts WHERE id = ?', (prompt_id,)).fetchone()
                if prompt:
                    current_tags = prompt['tags'] or ''
                    tags_list = [t.strip() for t in current_tags.split(',') if t.strip()]
                    
                    if tag not in tags_list:
                        tags_list.append(tag)
                        new_tags = ', '.join(tags_list)
                        cursor.execute(
                            'UPDATE prompts SET tags = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
                            (new_tags, prompt_id)
                        )
                        affected_rows += cursor.rowcount
        
        elif action == 'toggle_template':
            # 批量切换模板状态
            placeholders = ','.join(['?'] * len(ids))
            cursor.execute(
                f'UPDATE prompts SET is_template = NOT is_template, updated_at = CURRENT_TIMESTAMP WHERE id IN ({placeholders})',
                ids
            )
            affected_rows = cursor.rowcount
            
        else:
            return jsonify({'error': '不支持的操作'}), 400
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'message': f'批量操作完成',
            'affected_count': affected_rows
        })
        
    except Exception as e:
        conn.close()
        return jsonify({'error': f'批量操作失败: {str(e)}'}), 500

# 项目相关API
@app.route('/api/projects', methods=['GET'])
def get_projects():
    """获取所有项目以及它们的提示词数量"""
    conn = get_db_connection()
    sql = """
        SELECT p.id, p.name, p.description, p.created_at, COUNT(pr.id) as prompt_count
        FROM projects p
        LEFT JOIN prompts pr ON p.id = pr.project_id
        GROUP BY p.id
        ORDER BY p.created_at DESC
    """
    projects = conn.execute(sql).fetchall()
    conn.close()
    return jsonify([dict(p) for p in projects])

@app.route('/api/projects', methods=['POST'])
def create_project():
    """创建新项目"""
    data = request.get_json()
    if not data or not data.get('name') or not data.get('name').strip():
        return jsonify({'error': '项目名称不能为空'}), 400
    
    name = data['name'].strip()
    description = data.get('description', '')

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO projects (name, description) VALUES (?, ?)', (name, description))
        project_id = cursor.lastrowid
        conn.commit()
        # 返回完整的新项目对象
        new_project = {
            'id': project_id,
            'name': name,
            'description': description,
            'created_at': datetime.utcnow().isoformat(),
            'prompt_count': 0
        }
        return jsonify(new_project), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': '项目名称已存在'}), 409
    finally:
        conn.close()

@app.route('/api/projects/<int:project_id>', methods=['PUT'])
def update_project(project_id):
    """更新项目"""
    data = request.get_json()
    if not data or not data.get('name') or not data.get('name').strip():
        return jsonify({'error': '项目名称不能为空'}), 400
        
    name = data['name'].strip()
    description = data.get('description', '')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('UPDATE projects SET name = ?, description = ? WHERE id = ?', (name, description, project_id))
        if cursor.rowcount == 0:
            return jsonify({'error': '项目不存在'}), 404
        conn.commit()
        # 返回更新后的项目对象
        updated_project = {
            'id': project_id,
            'name': name,
            'description': description,
        }
        return jsonify(updated_project), 200
    except sqlite3.IntegrityError:
        return jsonify({'error': '项目名称已存在'}), 409
    finally:
        conn.close()


@app.route('/api/projects/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
    """删除项目"""
    conn = get_db_connection()
    cursor = conn.cursor()
    # 检查项目是否存在
    project = cursor.execute('SELECT * FROM projects WHERE id = ?', (project_id,)).fetchone()
    if not project:
        conn.close()
        return jsonify({'error': '项目不存在'}), 404
        
    # 将属于该项目的提示词的 project_id 设置为 NULL
    cursor.execute('UPDATE prompts SET project_id = NULL WHERE project_id = ?', (project_id,))
    # 删除项目
    cursor.execute('DELETE FROM projects WHERE id = ?', (project_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': '项目删除成功'}), 200


@app.route('/api/prompts/<int:prompt_id>/move', methods=['PUT'])
def move_prompt(prompt_id):
    """移动提示词到另一个项目"""
    data = request.get_json()
    # project_id 可以是 null
    project_id = data.get('project_id')

    if project_id is not None:
        try:
            # 验证 project_id 是否有效（如果不是 null）
            conn_check = get_db_connection()
            if conn_check.execute('SELECT id FROM projects WHERE id = ?', (project_id,)).fetchone() is None:
                conn_check.close()
                return jsonify({'error': '目标项目不存在'}), 404
            conn_check.close()
        except (ValueError, TypeError):
             return jsonify({'error': '无效的项目ID'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE prompts SET project_id = ? WHERE id = ?', (project_id, prompt_id))
    if cursor.rowcount == 0:
        conn.close()
        return jsonify({'error': '提示词不存在'}), 404
    
    conn.commit()
    conn.close()
    return jsonify({'message': '提示词移动成功'})

# 草稿箱相关API
@app.route('/api/drafts', methods=['GET'])
def get_drafts():
    """获取所有草稿"""
    conn = get_db_connection()
    drafts = conn.execute('''
        SELECT d.*, p.name as project_name 
        FROM drafts d 
        LEFT JOIN projects p ON d.project_id = p.id 
        ORDER BY d.updated_at DESC
    ''').fetchall()
    conn.close()
    return jsonify([dict(draft) for draft in drafts])

@app.route('/api/drafts', methods=['POST'])
def create_draft():
    """创建新草稿"""
    data = request.get_json()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO drafts (title, content, category, tags, project_id, author, language)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        data.get('title', ''),
        data.get('content', ''),
        data.get('category', ''),
        data.get('tags', ''),
        data.get('project_id'),
        data.get('author', ''),
        data.get('language', 'zh')
    ))
    
    draft_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return jsonify({'id': draft_id, 'message': '草稿创建成功'}), 201

@app.route('/api/drafts/<int:draft_id>', methods=['GET'])
def get_draft(draft_id):
    """获取单个草稿"""
    conn = get_db_connection()
    draft = conn.execute('''
        SELECT d.*, p.name as project_name 
        FROM drafts d 
        LEFT JOIN projects p ON d.project_id = p.id 
        WHERE d.id = ?
    ''', (draft_id,)).fetchone()
    conn.close()
    
    if draft is None:
        return jsonify({'error': '草稿不存在'}), 404
    
    return jsonify(dict(draft))

@app.route('/api/drafts/<int:draft_id>', methods=['PUT'])
def update_draft(draft_id):
    """更新草稿"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': '请求数据不能为空'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 检查草稿是否存在
    existing_draft = cursor.execute('SELECT * FROM drafts WHERE id = ?', (draft_id,)).fetchone()
    if not existing_draft:
        conn.close()
        return jsonify({'error': '草稿不存在'}), 404
    
    # 构建更新字段
    update_fields = []
    update_values = []
    
    for field in ['title', 'content', 'category', 'tags', 'project_id', 'author', 'language']:
        if field in data:
            update_fields.append(f'{field} = ?')
            update_values.append(data[field])
    
    if update_fields:
        update_fields.append('updated_at = ?')
        update_values.append(datetime.utcnow().isoformat())
        
        sql = f"UPDATE drafts SET {', '.join(update_fields)} WHERE id = ?"
        cursor.execute(sql, update_values + [draft_id])
    
    conn.commit()
    conn.close()
    
    return jsonify({'message': '草稿更新成功'})

@app.route('/api/drafts/<int:draft_id>/auto-save', methods=['PUT'])
def auto_save_draft(draft_id):
    """自动保存草稿内容"""
    data = request.get_json()
    
    if not data or 'content' not in data:
        return jsonify({'error': '内容不能为空'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE drafts 
        SET auto_save_content = ?, last_auto_save = ?
        WHERE id = ?
    ''', (data['content'], datetime.utcnow().isoformat(), draft_id))
    
    if cursor.rowcount == 0:
        conn.close()
        return jsonify({'error': '草稿不存在'}), 404
    
    conn.commit()
    conn.close()
    
    return jsonify({'message': '自动保存成功'})

@app.route('/api/drafts/<int:draft_id>', methods=['DELETE'])
def delete_draft(draft_id):
    """删除草稿"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM drafts WHERE id = ?', (draft_id,))
    
    if cursor.rowcount == 0:
        conn.close()
        return jsonify({'error': '草稿不存在'}), 404
    
    conn.commit()
    conn.close()
    
    return jsonify({'message': '草稿删除成功'})

@app.route('/api/drafts/<int:draft_id>/publish', methods=['POST'])
def publish_draft(draft_id):
    """将草稿发布为正式提示词"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 获取草稿信息
    draft = cursor.execute('SELECT * FROM drafts WHERE id = ?', (draft_id,)).fetchone()
    if not draft:
        conn.close()
        return jsonify({'error': '草稿不存在'}), 404
    
    # 使用最新的自动保存内容或正式内容
    content = draft['auto_save_content'] if draft['auto_save_content'] else draft['content']
    
    # 创建正式提示词
    cursor.execute('''
        INSERT INTO prompts (title, content, category, tags, project_id, author, language)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        draft['title'] or '未命名提示词',
        content,
        draft['category'],
        draft['tags'],
        draft['project_id'],
        draft['author'],
        draft['language']
    ))
    
    prompt_id = cursor.lastrowid
    
    # 删除草稿
    cursor.execute('DELETE FROM drafts WHERE id = ?', (draft_id,))
    
    conn.commit()
    conn.close()
    
    return jsonify({'id': prompt_id, 'message': '草稿发布成功'}), 201

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000) 