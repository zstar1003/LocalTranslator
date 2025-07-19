# LocalTranslator（本地翻译器）

<div align="center">
  <img src="ui/logo_with_txt.png" width="500" alt="FreePDF">
  <h4>
    <a href="README.md">🇨🇳 中文</a>
    <span> | </span>
    <a href="README_EN.md">🇬🇧 English</a>
  </h4>
</div>

## ✨ 功能特点

- 🤖 **AI驱动翻译**：基于T5 transformer模型，提供高质量翻译
- 🌐 **多语言支持**：支持中文、英文和俄语互译
- 💻 **离线运行**：完全离线工作，无需网络连接
- 🎨 **现代化界面**：简洁直观的界面，支持深色/浅色主题
- ⚡ **实时字数统计**：显示字符计数并提供视觉警告
- 📝 **智能输入限制**：自动管理文本长度以获得最佳性能
- 🔄 **双向翻译**：支持任意语言对之间的互译

## 🚀 快速开始

### 系统要求

- Windows 10/11 (64位)
- Python 3.8或更高版本
- 至少4GB内存
- 2GB可用磁盘空间

### 安装方法

#### 方法1：下载预编译可执行文件
1. 从[发布页面](https://github.com/zstar1003/LocalTranslator/releases)下载最新版本
2. 运行安装程序并按照向导完成安装
3. 从桌面或开始菜单启动LocalTranslator

#### 方法2：从源代码运行
1. 克隆仓库：
```bash
git clone https://github.com/zstar1003/LocalTranslator.git
cd LocalTranslator
```

2. 安装依赖：
```bash
uv sync
```

3. 下载AI模型：
```bash
python download_models.py
```

4. 运行应用程序：
```bash
python main.py
```

## 📖 使用指南

1. **选择源语言**：选择输入文本的语言
2. **选择目标语言**：选择要翻译成的语言
3. **输入文本**：在输入区域键入或粘贴文本
4. **监控字数**：注意字符计数器（500字符限制）
5. **翻译**：点击"翻译"按钮获取结果
6. **复制结果**：使用复制按钮将翻译结果复制到剪贴板

### 支持的语言对

- 中文 ↔ 英文
- 中文 ↔ 俄文
- 英文 ↔ 俄文

## 🛠️ 从源代码构建

### 构建可执行文件

1. 安装构建依赖：
```bash
pip install -r requirements-build.txt
```

2. 运行构建脚本：
```bash
package_all.bat
```

3. 可执行文件将生成在`dist/`目录中

### 创建安装程序

1. 安装[NSIS](https://nsis.sourceforge.io/Download)
2. 将NSIS添加到PATH环境变量
3. 运行安装程序创建脚本：
```bash
create_installer.bat
```

## 🎨 界面介绍

### 主要功能
- **输入面板**：带有实时字数统计的文本输入区域
- **输出面板**：翻译结果及复制功能
- **语言选择**：源语言和目标语言的下拉菜单
- **主题切换**：在浅色和深色主题间切换
- **进度指示器**：显示翻译进度

### 字符限制系统
- **绿色(0-400字符)**：正常操作
- **橙色(400-500字符)**：接近限制
- **红色(500+字符)**：超出限制，将被截断

## 🔧 技术细节

### 架构
- **前端**：使用PyQt6实现跨平台GUI
- **后端**：基于Transformers库和T5模型
- **模型**：`utrobinmv/t5_translate_en_ru_zh_small_1024`
- **线程处理**：异步翻译防止UI冻结

### 性能
- **模型大小**：约1GB
- **内存使用**：运行期间2-4GB
- **翻译速度**：典型文本1-3秒
- **支持文本长度**：每次翻译最多500字符

## 📁 项目结构

```
LocalTranslator/
├── main.py# 应用程序入口点
├── translator/# 主应用程序包
│├── translator_app.py# 主GUI应用程序
│├── translation_thread.py # 翻译工作线程
│├── config.py# 配置常量
│└── themes.py# UI主题定义
├── ui/# UI资源
│└── logo.png# 应用程序标志
├── models/# AI模型文件
├── build.spec# PyInstaller构建配置
└── installer.nsi# NSIS安装程序脚本
```

## 🤝 参与贡献

欢迎贡献！请随时提交Pull Request。

1. Fork本仓库
2. 创建您的功能分支（`git checkout -b feature/AmazingFeature`）
3. 提交您的更改（`git commit -m 'Add some AmazingFeature'`）
4. 推送到分支（`git push origin feature/AmazingFeature`）
5. 打开Pull Request

## 🙏 致谢

- [Hugging Face Transformers](https://huggingface.co/transformers/) 提供ML框架
- [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) 提供GUI框架
- [T5 Model](https://huggingface.co/utrobinmv/t5_translate_en_ru_zh_small_1024) 提供翻译能力

## 📞 支持

如果您遇到任何问题或有疑问：

1. 查看[问题](https://github.com/zstar1003/LocalTranslator/issues)页面
2. 如果问题未被报告，请创建新问题
3. 提供有关您的系统和问题的详细信息

---
