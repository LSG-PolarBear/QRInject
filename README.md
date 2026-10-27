# 🎯 QRInject - 照片二维码替换与注入工具

**QRInject** 是一款基于 `PyQt5` 开发的桌面级工具，专为安全测试、红队演练、授权营销测试等场景设计。
它能够将自定义的二维码以**拖拽、缩放、任意排版**的方式无缝注入到目标照片中，并支持一键智能识别、精准覆盖原有的旧二维码。

> **核心应用场景**：二维码替换（Social Engineering）、海报链接注入、自定义名片与卡片生成。



## ✨ 核心功能

- **🎯 一键识别与替换（核心）**：导入目标海报/照片，点击「识别原图二维码」，程序会自动解析出旧链接，并将你设定的新二维码**精准覆盖**在原位置（自动放大 1.2 倍，完美遮挡旧码边缘）。
- **🖼️ 自由拖拽与缩放**：生成新二维码后，按住鼠标**左键**即可自由拖拽；拖拽四角小方块可等比缩放，完美匹配任何尺寸。
- **🎨 深度视觉定制**：支持自定义前景色、背景色。支持“背景透明”模式，让二维码与图片场景深度融合。
- **🛡️ 防漏边机制**：内置「外围白边」选项（默认开启），强制在二维码四周生成安全白边，彻底杜绝旧码残留或底层图案干扰扫码的问题。
- **🏷️ 中心 Logo 注入**：支持在二维码中心嵌入自定义图标/头像，程序会自动处理安全间距，不影响扫码。
- **💾 自动备份恢复**：具备退出拦截与自动备份机制。若误关软件，下次启动可一键恢复上次的排版状态，防止心血白费。



## 🛠️ 环境安装

请确保已安装 Python 3.6+ 环境。在命令行中执行以下命令安装依赖：

```bash
pip install PyQt5 qrcode[pil] Pillow opencv-python numpy

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 🎯 QRInject - Photo QR Code Replacement & Injection Tool

**QRInject** is a desktop-level tool built with `PyQt5`, specifically designed for scenarios such as security testing, red team exercises, and authorized marketing tests.
It can seamlessly inject custom QR codes into target photos via **drag-and-drop, scaling, and arbitrary layout**, and supports one-click smart detection to precisely overlay and replace existing old QR codes.

> **Core Use Cases**: QR code replacement (Social Engineering), poster link injection, custom business card and card generation.

## ✨ Core Features

- **🎯 One-Click Detection & Replacement (Core)**: Import the target poster/photo and click "Detect Original QR Code". The program will automatically parse the old link and **precisely overlay** your new QR code onto the original position (auto-scaled by 1.2x to perfectly cover the edges of the old code).
- **🖼️ Free Drag & Drop Scaling**: Once the new QR code is generated, hold the **left mouse button** to drag it freely; drag the small corner squares to scale proportionally to perfectly match any size.
- **🎨 In-Depth Visual Customization**: Supports custom foreground and background colors. The "Transparent Background" mode allows the QR code to blend seamlessly with the image scene.
- **🛡️ Anti-Bleed Margin Mechanism**: Built-in "Outer White Margin" option (enabled by default) forces a safe white margin around the QR code, completely preventing old code remnants or background patterns from interfering with scanning.
- **🏷️ Center Logo Injection**: Supports embedding custom icons/avatars in the center of the QR code. The program automatically handles safe spacing without affecting scanning.
- **💾 Auto-Backup & Recovery**: Features exit interception and auto-backup mechanisms. If the software is closed by mistake, the previous layout state can be restored with one click on the next launch, preventing loss of work.

## 🛠️ Environment Setup

Please ensure Python 3.6+ is installed. Execute the following command in the command line to install dependencies:

```bash
pip install PyQt5 qrcode[pil] Pillow opencv-python numpy
