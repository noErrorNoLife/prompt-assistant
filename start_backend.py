#!/usr/bin/env python3
"""
Flask 后端启动脚本
运行此脚本来启动提示词管理系统的后端API服务
"""

import sys
import os
import subprocess

def check_dependencies():
    """检查并安装必要的依赖"""
    try:
        import flask
        import flask_cors
        print("✅ 依赖检查通过")
    except ImportError as e:
        print(f"❌ 缺少依赖: {e}")
        print("正在安装依赖...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
            print("✅ 依赖安装完成")
        except subprocess.CalledProcessError:
            print("❌ 依赖安装失败，请手动运行: pip install -r requirements.txt")
            return False
    return True

def main():
    """主函数"""
    print("🚀 启动提示词管理系统后端...")
    
    if not check_dependencies():
        sys.exit(1)
    
    # 设置环境变量
    os.environ['FLASK_ENV'] = 'development'
    os.environ['FLASK_DEBUG'] = '1'
    
    print("📊 数据库初始化...")
    print("🌐 启动Flask服务器在 http://localhost:5000")
    print("📝 API文档:")
    print("   - GET  /api/prompts     - 获取所有提示词")
    print("   - POST /api/prompts     - 创建新提示词")
    print("   - GET  /api/modules     - 获取所有模块")
    print("   - POST /api/modules     - 创建新模块")
    print("按 Ctrl+C 停止服务器")
    print("-" * 50)
    
    try:
        # 导入并运行Flask应用
        from app import app, init_db
        init_db()
        app.run(debug=True, port=5000, host='0.0.0.0')
    except KeyboardInterrupt:
        print("\n👋 服务器已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 