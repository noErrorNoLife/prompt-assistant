# 系统诊断脚本 - 收集Node.js/npm相关信息
$reportFile = "system_report_$(Get-Date -Format 'yyyyMMdd_HHmmss').txt"

Write-Host "正在收集系统信息..." -ForegroundColor Green

# 创建报告文件
@"
========================================
系统诊断报告
生成时间: $(Get-Date)
========================================

"@ | Out-File -FilePath $reportFile -Encoding UTF8

# 1. 系统基本信息
@"
=== 系统基本信息 ===
操作系统: $((Get-WmiObject Win32_OperatingSystem).Caption)
系统架构: $env:PROCESSOR_ARCHITECTURE
PowerShell版本: $($PSVersionTable.PSVersion)
用户名: $env:USERNAME
计算机名: $env:COMPUTERNAME

"@ | Out-File -FilePath $reportFile -Append -Encoding UTF8

# 2. 环境变量
@"
=== 关键环境变量 ===
PATH: $env:PATH

NVM_HOME: $env:NVM_HOME
NVM_SYMLINK: $env:NVM_SYMLINK
NODE_PATH: $env:NODE_PATH
NPM_CONFIG_PREFIX: $env:NPM_CONFIG_PREFIX

"@ | Out-File -FilePath $reportFile -Append -Encoding UTF8

# 3. 命令可用性检查
@"
=== 命令可用性检查 ===
"@ | Out-File -FilePath $reportFile -Append -Encoding UTF8

# 检查各种命令
$commands = @('node', 'npm', 'npx', 'nvm')
foreach ($cmd in $commands) {
    try {
        $version = & $cmd --version 2>$null
        "✓ $cmd 可用: $version" | Out-File -FilePath $reportFile -Append -Encoding UTF8
    }
    catch {
        "✗ $cmd 不可用" | Out-File -FilePath $reportFile -Append -Encoding UTF8
    }
}

# 4. 检查nvm相关目录
@"

=== NVM 相关目录检查 ===
"@ | Out-File -FilePath $reportFile -Append -Encoding UTF8

if ($env:NVM_HOME) {
    "NVM_HOME 目录: $env:NVM_HOME" | Out-File -FilePath $reportFile -Append -Encoding UTF8
    if (Test-Path $env:NVM_HOME) {
        "✓ NVM_HOME 目录存在" | Out-File -FilePath $reportFile -Append -Encoding UTF8
        "NVM 目录内容:" | Out-File -FilePath $reportFile -Append -Encoding UTF8
        Get-ChildItem $env:NVM_HOME -ErrorAction SilentlyContinue | Out-File -FilePath $reportFile -Append -Encoding UTF8
        
        # 检查Node版本目录
        $nodeVersions = Get-ChildItem "$env:NVM_HOME\v*" -Directory -ErrorAction SilentlyContinue
        if ($nodeVersions) {
            "`nNode 版本目录:" | Out-File -FilePath $reportFile -Append -Encoding UTF8
            foreach ($version in $nodeVersions) {
                "  $($version.Name):" | Out-File -FilePath $reportFile -Append -Encoding UTF8
                $nodePath = Join-Path $version.FullName "node.exe"
                $npmPath = Join-Path $version.FullName "npm.cmd"
                $npxPath = Join-Path $version.FullName "npx.cmd"
                
                "    node.exe: $(if (Test-Path $nodePath) { '✓ 存在' } else { '✗ 不存在' })" | Out-File -FilePath $reportFile -Append -Encoding UTF8
                "    npm.cmd: $(if (Test-Path $npmPath) { '✓ 存在' } else { '✗ 不存在' })" | Out-File -FilePath $reportFile -Append -Encoding UTF8
                "    npx.cmd: $(if (Test-Path $npxPath) { '✓ 存在' } else { '✗ 不存在' })" | Out-File -FilePath $reportFile -Append -Encoding UTF8
            }
        }
    } else {
        "✗ NVM_HOME 目录不存在" | Out-File -FilePath $reportFile -Append -Encoding UTF8
    }
} else {
    "✗ NVM_HOME 环境变量未设置" | Out-File -FilePath $reportFile -Append -Encoding UTF8
}

# 5. 检查符号链接目录
if ($env:NVM_SYMLINK) {
    "`nNVM_SYMLINK 目录: $env:NVM_SYMLINK" | Out-File -FilePath $reportFile -Append -Encoding UTF8
    if (Test-Path $env:NVM_SYMLINK) {
        "✓ NVM_SYMLINK 目录存在" | Out-File -FilePath $reportFile -Append -Encoding UTF8
        "符号链接目录内容:" | Out-File -FilePath $reportFile -Append -Encoding UTF8
        Get-ChildItem $env:NVM_SYMLINK -ErrorAction SilentlyContinue | Out-File -FilePath $reportFile -Append -Encoding UTF8
    } else {
        "✗ NVM_SYMLINK 目录不存在" | Out-File -FilePath $reportFile -Append -Encoding UTF8
    }
}

# 6. 检查可能的Node.js安装位置
@"

=== 其他可能的 Node.js 安装位置 ===
"@ | Out-File -FilePath $reportFile -Append -Encoding UTF8

$possiblePaths = @(
    "${env:ProgramFiles}\nodejs",
    "${env:ProgramFiles(x86)}\nodejs",
    "${env:APPDATA}\npm",
    "${env:LOCALAPPDATA}\npm"
)

foreach ($path in $possiblePaths) {
    if (Test-Path $path) {
        "✓ 发现: $path" | Out-File -FilePath $reportFile -Append -Encoding UTF8
        try {
            Get-ChildItem $path -ErrorAction SilentlyContinue | Select-Object Name, Length, LastWriteTime | Out-File -FilePath $reportFile -Append -Encoding UTF8
        } catch {
            "  (无法读取目录内容)" | Out-File -FilePath $reportFile -Append -Encoding UTF8
        }
    } else {
        "✗ 未发现: $path" | Out-File -FilePath $reportFile -Append -Encoding UTF8
    }
}

# 7. PATH变量详细分析
@"

=== PATH 变量详细分析 ===
"@ | Out-File -FilePath $reportFile -Append -Encoding UTF8

$pathEntries = $env:PATH -split ';'
for ($i = 0; $i -lt $pathEntries.Count; $i++) {
    $entry = $pathEntries[$i].Trim()
    if ($entry -match 'nvm|node|npm') {
        "$($i+1). $entry $(if (Test-Path $entry) { '✓' } else { '✗' })" | Out-File -FilePath $reportFile -Append -Encoding UTF8
    }
}

# 8. 检查注册表中的Node.js信息
@"

=== 注册表信息 ===
"@ | Out-File -FilePath $reportFile -Append -Encoding UTF8

try {
    $nodeRegPath = "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*"
    $nodeApps = Get-ItemProperty $nodeRegPath -ErrorAction SilentlyContinue | Where-Object { $_.DisplayName -like "*Node*" -or $_.DisplayName -like "*npm*" }
    if ($nodeApps) {
        "已安装的 Node.js 相关程序:" | Out-File -FilePath $reportFile -Append -Encoding UTF8
        $nodeApps | Select-Object DisplayName, DisplayVersion, InstallLocation | Out-File -FilePath $reportFile -Append -Encoding UTF8
    } else {
        "注册表中未找到 Node.js 相关程序" | Out-File -FilePath $reportFile -Append -Encoding UTF8
    }
} catch {
    "无法读取注册表信息: $($_.Exception.Message)" | Out-File -FilePath $reportFile -Append -Encoding UTF8
}

@"

========================================
报告生成完成
文件位置: $((Get-Location).Path)\$reportFile
========================================
"@ | Out-File -FilePath $reportFile -Append -Encoding UTF8

Write-Host "报告已生成: $reportFile" -ForegroundColor Green
Write-Host "请检查报告内容以诊断问题" -ForegroundColor Yellow

# 显示报告摘要
Write-Host "`n=== 快速摘要 ===" -ForegroundColor Cyan
Write-Host "Node.js 可用: $(if (Get-Command node -ErrorAction SilentlyContinue) { '✓' } else { '✗' })"
Write-Host "npm 可用: $(if (Get-Command npm -ErrorAction SilentlyContinue) { '✓' } else { '✗' })"
Write-Host "nvm 可用: $(if (Get-Command nvm -ErrorAction SilentlyContinue) { '✓' } else { '✗' })"
Write-Host "NVM_HOME: $env:NVM_HOME"
Write-Host "NVM_SYMLINK: $env:NVM_SYMLINK"