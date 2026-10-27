import sys
import os
import json
from datetime import datetime

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QFrame, QGridLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy, QGraphicsDropShadowEffect,
    QColorDialog, QFileDialog, QGraphicsView, QGraphicsScene, 
    QGraphicsObject, QGraphicsPixmapItem, QMessageBox, QCheckBox, QGraphicsItem,
    QMenu, QAction
)
from PyQt5.QtCore import Qt, QSettings, QRectF, QPointF, QSizeF, pyqtSignal
from PyQt5.QtGui import QColor, QPixmap, QImage, QPainter, QBrush, QPen

import qrcode
from qrcode.constants import ERROR_CORRECT_H
from PIL import Image, ImageDraw
import cv2
import numpy as np


# ==================== QSS 样式 ====================
LIGHT_QSS = """
QWidget { background-color: #eef1f7; color: #1e293b; font-family: "Microsoft YaHei", sans-serif; font-size: 14px; }
QLabel { background: transparent; }
QFrame#card { background-color: #ffffff; border-radius: 16px; }
QLabel#title { font-size: 22px; font-weight: bold; color: #1e293b; }
QLabel#subtitle { font-size: 13px; color: #64748b; }
QLabel#fieldLabel { font-size: 13px; font-weight: bold; color: #64748b; margin-top: 5px; }
QLabel#hint { font-size: 12px; color: #64748b; }
QFrame#divider { background-color: #eef1f7; border: none; max-height: 1px; }

QLineEdit { background-color: #f8fafc; border: 2px solid #e2e8f0; border-radius: 10px; padding: 10px 14px; color: #1e293b; }
QLineEdit:focus { border-color: #4f7cff; }

QPushButton { border-radius: 10px; font-size: 14px; font-weight: bold; }
QPushButton#primaryBtn { color: #ffffff; border: none; padding: 12px 0; background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #4f7cff, stop:1 #3d6bf0); }
QPushButton#primaryBtn:hover { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #6a90ff, stop:1 #4f7cff); }
QPushButton#secondaryBtn { color: #4f7cff; background: transparent; border: 2px solid #4f7cff; padding: 12px 0; }
QPushButton#secondaryBtn:hover { background: #eef3ff; }
QPushButton#secondaryBtn:disabled { color: #b6c0cf; border-color: #e2e8f0; }
QPushButton#themeBtn { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; font-size: 16px; color: #1e293b; padding: 0; }
QPushButton#themeBtn:hover { border-color: #4f7cff; }

QPushButton#fileBtn { background: #f8fafc; border: 2px solid #e2e8f0; border-radius: 10px; padding: 8px 12px; font-weight: normal; color: #1e293b; text-align: left; }
QPushButton#fileBtn:hover { border-color: #4f7cff; }

QPushButton#smallBtn { background: transparent; border: 1px solid #e2e8f0; border-radius: 8px; padding: 6px 0; color: #1e293b; font-weight: normal; font-size: 12px; }
QPushButton#smallBtn:hover { border-color: #4f7cff; color: #4f7cff; }

QPushButton#logoBtn { background: #f8fafc; border: 1px dashed #e2e8f0; border-radius: 10px; padding: 8px 12px; font-weight: normal; color: #64748b; text-align: center; }
QPushButton#logoBtn:hover { border-color: #4f7cff; color: #4f7cff; }

QPushButton#dangerBtn { background: #fff1f2; border: 1px solid #fecdd3; border-radius: 10px; padding: 8px 12px; font-weight: normal; color: #e11d48; text-align: center; font-size: 13px; }
QPushButton#dangerBtn:hover { background: #ffe4e6; border-color: #fda4af; }

QCheckBox { color: #1e293b; font-size: 13px; spacing: 8px; margin-top: 5px; }
QCheckBox::indicator { width: 18px; height: 18px; border-radius: 5px; border: 2px solid #e2e8f0; background: #f8fafc; }
QCheckBox::indicator:checked { background: #4f7cff; border-color: #4f7cff; }

QFrame#tipsBox { background-color: #f8fafc; border-radius: 8px; }
QGraphicsView { background-color: #f8fafc; border: 2px dashed #cbd5e1; border-radius: 14px; }
"""

DARK_QSS = """
QWidget { background-color: #0f172a; color: #f1f5f9; font-family: "Microsoft YaHei", sans-serif; font-size: 14px; }
QLabel { background: transparent; }
QFrame#card { background-color: #1e293b; border-radius: 16px; }
QLabel#title { font-size: 22px; font-weight: bold; color: #f1f5f9; }
QLabel#subtitle { font-size: 13px; color: #94a3b8; }
QLabel#fieldLabel { font-size: 13px; font-weight: bold; color: #94a3b8; margin-top: 5px; }
QLabel#hint { font-size: 12px; color: #94a3b8; }
QFrame#divider { background-color: #334155; border: none; max-height: 1px; }

QLineEdit { background-color: #0f172a; border: 2px solid #334155; border-radius: 10px; padding: 10px 14px; color: #f1f5f9; }
QLineEdit:focus { border-color: #5b8cff; }

QPushButton { border-radius: 10px; font-size: 14px; font-weight: bold; }
QPushButton#primaryBtn { color: #ffffff; border: none; padding: 12px 0; background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #5b8cff, stop:1 #4a7ae8); }
QPushButton#primaryBtn:hover { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #6f9bff, stop:1 #5b8cff); }
QPushButton#secondaryBtn { color: #5b8cff; background: transparent; border: 2px solid #5b8cff; padding: 12px 0; }
QPushButton#secondaryBtn:hover { background: #263449; }
QPushButton#secondaryBtn:disabled { color: #64748b; border-color: #334155; }
QPushButton#themeBtn { background: #0f172a; border: 1px solid #334155; border-radius: 10px; font-size: 16px; color: #f1f5f9; padding: 0; }
QPushButton#themeBtn:hover { border-color: #5b8cff; }

QPushButton#fileBtn { background: #0f172a; border: 2px solid #334155; border-radius: 10px; padding: 8px 12px; font-weight: normal; color: #f1f5f9; text-align: left; }
QPushButton#fileBtn:hover { border-color: #5b8cff; }

QPushButton#smallBtn { background: transparent; border: 1px solid #334155; border-radius: 8px; padding: 6px 0; color: #f1f5f9; font-weight: normal; font-size: 12px; }
QPushButton#smallBtn:hover { border-color: #5b8cff; color: #5b8cff; }

QPushButton#logoBtn { background: #0f172a; border: 1px dashed #334155; border-radius: 10px; padding: 8px 12px; font-weight: normal; color: #94a3b8; text-align: center; }
QPushButton#logoBtn:hover { border-color: #5b8cff; color: #5b8cff; }

QPushButton#dangerBtn { background: rgba(225, 29, 72, 0.1); border: 1px solid rgba(225, 29, 72, 0.3); border-radius: 10px; padding: 8px 12px; font-weight: normal; color: #fda4af; text-align: center; font-size: 13px; }
QPushButton#dangerBtn:hover { background: rgba(225, 29, 72, 0.2); border-color: rgba(225, 29, 72, 0.5); }

QCheckBox { color: #f1f5f9; font-size: 13px; spacing: 8px; margin-top: 5px; }
QCheckBox::indicator { width: 18px; height: 18px; border-radius: 5px; border: 2px solid #334155; background: #0f172a; }
QCheckBox::indicator:checked { background: #5b8cff; border-color: #5b8cff; }

QFrame#tipsBox { background-color: #0f172a; border-radius: 8px; }
QGraphicsView { background-color: #0f172a; border: 2px dashed #334155; border-radius: 14px; }
"""


# ==================== 画布：可拖拽、可边角缩放的图元 ====================
class ResizablePixmapItem(QGraphicsObject):
    deleted = pyqtSignal()

    def __init__(self, pixmap, parent=None):
        super().__init__(parent)
        self._pixmap = pixmap
        self.orig_w = pixmap.width()
        self.orig_h = pixmap.height()
        self._rect = QRectF(0, 0, self.orig_w, self.orig_h)
        
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setAcceptHoverEvents(True)
        
        self.handle_size = 14
        self.min_size = 40
        self.active_handle = None
        self.drag_start_pos = None
        self.orig_rect = None
        self.orig_pos = None

    def boundingRect(self):
        return self._rect.adjusted(-self.handle_size, -self.handle_size, self.handle_size, self.handle_size)

    def paint(self, painter, option, widget):
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        painter.drawPixmap(self._rect.toRect(), self._pixmap)
        
        if self.isSelected():
            pen = QPen(QColor(79, 124, 255), 2, Qt.DashLine)
            painter.setPen(pen)
            painter.drawRect(self._rect)
            
            painter.setPen(QPen(QColor(79, 124, 255), 1))
            painter.setBrush(QBrush(Qt.white))
            h = self.handle_size / 2
            for pt in [self._rect.topLeft(), self._rect.topRight(), self._rect.bottomLeft(), self._rect.bottomRight()]:
                painter.drawRect(QRectF(pt.x() - h, pt.y() - h, self.handle_size, self.handle_size))

    def _get_handle_at(self, pos):
        h = self.handle_size
        r = self._rect
        if QRectF(r.topLeft().x() - h, r.topLeft().y() - h, h*2, h*2).contains(pos): return "TL"
        if QRectF(r.topRight().x() - h, r.topRight().y() - h, h*2, h*2).contains(pos): return "TR"
        if QRectF(r.bottomLeft().x() - h, r.bottomLeft().y() - h, h*2, h*2).contains(pos): return "BL"
        if QRectF(r.bottomRight().x() - h, r.bottomRight().y() - h, h*2, h*2).contains(pos): return "BR"
        if r.contains(pos): return "MOVE"
        return None

    def hoverMoveEvent(self, event):
        handle = self._get_handle_at(event.pos())
        if handle in ("TL", "BR"):
            self.setCursor(Qt.SizeFDiagCursor)
        elif handle in ("TR", "BL"):
            self.setCursor(Qt.SizeBDiagCursor)
        elif handle == "MOVE":
            self.setCursor(Qt.OpenHandCursor)
        else:
            self.setCursor(Qt.ArrowCursor)
        super().hoverMoveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.active_handle = self._get_handle_at(event.pos())
            if self.active_handle:
                self.setSelected(True)
                self.drag_start_pos = event.scenePos()
                self.orig_rect = QRectF(self._rect)
                self.orig_pos = self.pos()
                if self.active_handle == "MOVE":
                    self.setCursor(Qt.ClosedHandCursor)
                event.accept()
                return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.active_handle:
            delta = event.scenePos() - self.drag_start_pos
            
            if self.active_handle == "MOVE":
                self.setPos(self.orig_pos + delta)
            else:
                orig_ratio = self.orig_rect.width() / self.orig_rect.height()
                
                if self.active_handle == "BR":
                    delta_scale = (delta.x() + delta.y()) / 2
                elif self.active_handle == "TL":
                    delta_scale = -(delta.x() + delta.y()) / 2
                elif self.active_handle == "TR":
                    delta_scale = (delta.x() - delta.y()) / 2
                else: # BL
                    delta_scale = (-delta.x() + delta.y()) / 2

                new_w = max(self.min_size, self.orig_rect.width() + delta_scale)
                new_h = new_w / orig_ratio
                
                self.prepareGeometryChange()
                
                if self.active_handle == "BR":
                    self._rect.setSize(QSizeF(new_w, new_h))
                elif self.active_handle == "TL":
                    self._rect.setTopLeft(self.orig_rect.bottomRight() - QPointF(new_w, new_h))
                    self._rect.setSize(QSizeF(new_w, new_h))
                elif self.active_handle == "TR":
                    self._rect.setTopRight(self.orig_rect.bottomLeft() + QPointF(new_w, -new_h))
                    self._rect.setSize(QSizeF(new_w, new_h))
                elif self.active_handle == "BL":
                    self._rect.setBottomLeft(self.orig_rect.topRight() + QPointF(-new_w, new_h))
                    self._rect.setSize(QSizeF(new_w, new_h))
            event.accept()
            return
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.active_handle = None
            if self._get_handle_at(event.pos()) == "MOVE":
                self.setCursor(Qt.OpenHandCursor)
            else:
                self.setCursor(Qt.ArrowCursor)
            event.accept()
            return
        super().mouseReleaseEvent(event)

    def contextMenuEvent(self, event):
        self.setSelected(True)
        menu = QMenu()
        
        scene_bg = self.scene().views()[0].palette().color(self.scene().views()[0].backgroundRole())
        if scene_bg.lightness() < 128:
            menu.setStyleSheet("""
                QMenu { background-color: #1e293b; color: #f1f5f9; border: 1px solid #334155; border-radius: 8px; padding: 6px; }
                QMenu::item { padding: 6px 24px; border-radius: 4px; }
                QMenu::item:selected { background-color: #5b8cff; color: white; }
            """)
        else:
            menu.setStyleSheet("""
                QMenu { background-color: #ffffff; color: #1e293b; border: 1px solid #e2e8f0; border-radius: 8px; padding: 6px; }
                QMenu::item { padding: 6px 24px; border-radius: 4px; }
                QMenu::item:selected { background-color: #4f7cff; color: white; }
            """)
            
        delete_action = QAction("删除二维码", menu)
        delete_action.triggered.connect(self.delete_self)
        menu.addAction(delete_action)
        
        menu.exec_(event.screenPos())
        event.accept()

    def delete_self(self):
        self.deleted.emit()
        if self.scene():
            self.scene().removeItem(self)


class ImageEditorView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setRenderHint(QPainter.Antialiasing)
        self.setRenderHint(QPainter.SmoothPixmapTransform)


# ==================== 主窗口 ====================
class QRCodeWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("照片二维码编辑器 - 拖拽版")
        self.settings = QSettings("QRCodeApp", "EditorMode9")
        self.theme_name = self.settings.value("theme", "light")
        
        self.fg_color = "#000000"
        self.bg_color = "#ffffff"
        self.bg_image_path = ""
        self.logo_path = ""
        self.bg_item = None
        self.qr_item = None
        
        self.fg_colors = ["#000000", "#ffffff", "#e74c3c", "#3498db", "#2ecc71", "#34495e"]
        self.bg_colors = ["#ffffff", "#f8fafc", "#f1f2f6", "#eef3ff", "#ffeaa7", "#fab1a0"]
        
        self.has_unsaved_changes = False  # 记录是否有未保存的工作
        self.autosave_path = os.path.join(os.path.expanduser("~"), ".qrcode_autosave.json")

        self.setAcceptDrops(True)
        self._setup_window()
        self._build_ui()
        self._apply_theme()
        
        # 启动时检查是否有应急备份
        self.check_autosave()

    def _setup_window(self):
        screen = QApplication.primaryScreen().availableGeometry()
        w, h = int(screen.width() * 0.88), int(screen.height() * 0.88)
        self.setGeometry((screen.width()-w)//2, (screen.height()-h)//2, w, h)
        self.setMinimumSize(1000, 820)

    def _build_ui(self):
        root = QHBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(20)

        self.left_card = QFrame()
        self.left_card.setObjectName("card")
        self.left_card.setFixedWidth(380)
        left = QVBoxLayout(self.left_card)
        left.setContentsMargins(24, 22, 24, 22)
        left.setSpacing(10)

        header = QHBoxLayout()
        title = QLabel("照片二维码编辑器")
        title.setObjectName("title")
        header.addWidget(title)
        header.addStretch(1)
        self.theme_btn = QPushButton()
        self.theme_btn.setObjectName("themeBtn")
        self.theme_btn.setFixedSize(36, 36)
        self.theme_btn.setCursor(Qt.PointingHandCursor)
        self.theme_btn.clicked.connect(self.toggle_theme)
        header.addWidget(self.theme_btn)
        left.addLayout(header)
        
        sub = QLabel("左键拖拽移动，右键呼出菜单")
        sub.setObjectName("subtitle")
        left.addWidget(sub)

        # 1. 链接
        left.addWidget(QLabel("1. 链接地址", objectName="fieldLabel"))
        self.url_edit = QLineEdit()
        self.url_edit.setPlaceholderText("https://example.com")
        self.url_edit.setText("https://baidu.com")
        left.addWidget(self.url_edit)

        # 2. 导入照片
        left.addWidget(QLabel("2. 导入背景照片", objectName="fieldLabel"))
        self.photo_btn = QPushButton("点击选择本地照片 …")
        self.photo_btn.setObjectName("fileBtn")
        self.photo_btn.setFixedHeight(36)
        self.photo_btn.setCursor(Qt.PointingHandCursor)
        self.photo_btn.clicked.connect(self.select_photo)
        left.addWidget(self.photo_btn)

        # 3. 生成按钮
        self.gen_qr_btn = QPushButton("3. 生成二维码 并 插入画布")
        self.gen_qr_btn.setObjectName("primaryBtn")
        self.gen_qr_btn.setCursor(Qt.PointingHandCursor)
        self.gen_qr_btn.clicked.connect(self.insert_qr_to_canvas)
        left.addWidget(self.gen_qr_btn)

        left.addWidget(self._divider())

        # 颜色调色板
        left.addWidget(QLabel("4. 二维码颜色定制", objectName="fieldLabel"))
        
        left.addWidget(QLabel("前景色（二维码点）", objectName="hint"))
        fg_grid = QGridLayout()
        fg_grid.setSpacing(6)
        self.fg_btns = {}
        for i, color in enumerate(self.fg_colors):
            btn = QPushButton()
            btn.setFixedSize(36, 36)
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(lambda _, c=color: self.set_fg_color(c))
            self.fg_btns[color] = btn
            fg_grid.addWidget(btn, 0, i)
        btn_custom_fg = QPushButton("自定义...")
        btn_custom_fg.setObjectName("smallBtn")
        btn_custom_fg.setFixedHeight(36)
        btn_custom_fg.clicked.connect(self.pick_fg)
        fg_grid.addWidget(btn_custom_fg, 0, len(self.fg_colors), 1, 2)
        left.addLayout(fg_grid)

        left.addWidget(QLabel("背景色（二维码底色）", objectName="hint"))
        bg_grid = QGridLayout()
        bg_grid.setSpacing(6)
        self.bg_btns = {}
        for i, color in enumerate(self.bg_colors):
            btn = QPushButton()
            btn.setFixedSize(36, 36)
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(lambda _, c=color: self.set_bg_color(c))
            self.bg_btns[color] = btn
            bg_grid.addWidget(btn, 0, i)
        btn_custom_bg = QPushButton("自定义...")
        btn_custom_bg.setObjectName("smallBtn")
        btn_custom_bg.setFixedHeight(36)
        btn_custom_bg.clicked.connect(self.pick_bg)
        bg_grid.addWidget(btn_custom_bg, 0, len(self.bg_colors), 1, 2)
        left.addLayout(bg_grid)
        
        self.bg_transparent_cb = QCheckBox("背景透明（去掉白底）")
        self.bg_transparent_cb.setChecked(True)
        self.bg_transparent_cb.toggled.connect(self.on_bg_transparent_toggled)
        left.addWidget(self.bg_transparent_cb)

        # Logo 嵌入
        left.addWidget(QLabel("中心 Logo / 头像", objectName="hint"))
        logo_layout = QHBoxLayout()
        logo_layout.setSpacing(6)
        self.logo_btn = QPushButton("插入 Logo (可选)")
        self.logo_btn.setObjectName("logoBtn")
        self.logo_btn.setFixedHeight(34)
        self.logo_btn.setCursor(Qt.PointingHandCursor)
        self.logo_btn.clicked.connect(self.select_logo)
        logo_layout.addWidget(self.logo_btn, 3)
        
        self.clear_logo_btn = QPushButton("清除")
        self.clear_logo_btn.setObjectName("smallBtn")
        self.clear_logo_btn.setFixedHeight(34)
        self.clear_logo_btn.setCursor(Qt.PointingHandCursor)
        self.clear_logo_btn.clicked.connect(self.clear_logo)
        self.clear_logo_btn.setEnabled(False)
        logo_layout.addWidget(self.clear_logo_btn, 1)
        left.addLayout(logo_layout)

        left.addWidget(self._divider())

        # 快捷排版工具
        left.addWidget(QLabel("5. 快捷排版工具", objectName="fieldLabel"))
        tool_layout = QGridLayout()
        tool_layout.setSpacing(6)
        
        pos_center = QPushButton("居中")
        pos_center.setObjectName("smallBtn")
        pos_center.clicked.connect(lambda: self.quick_align("center"))
        
        pos_tl = QPushButton("左上")
        pos_tl.setObjectName("smallBtn")
        pos_tl.clicked.connect(lambda: self.quick_align("tl"))
        
        pos_tr = QPushButton("右上")
        pos_tr.setObjectName("smallBtn")
        pos_tr.clicked.connect(lambda: self.quick_align("tr"))
        
        pos_bl = QPushButton("左下")
        pos_bl.setObjectName("smallBtn")
        pos_bl.clicked.connect(lambda: self.quick_align("bl"))
        
        pos_br = QPushButton("右下")
        pos_br.setObjectName("smallBtn")
        pos_br.clicked.connect(lambda: self.quick_align("br"))
        
        reset_size_btn = QPushButton("重置大小")
        reset_size_btn.setObjectName("smallBtn")
        reset_size_btn.clicked.connect(self.reset_size)

        tool_layout.addWidget(QLabel("定位:"), 0, 0)
        tool_layout.addWidget(pos_tl, 0, 1)
        tool_layout.addWidget(pos_center, 0, 2)
        tool_layout.addWidget(pos_tr, 0, 3)
        tool_layout.addWidget(pos_bl, 1, 1)
        tool_layout.addWidget(reset_size_btn, 1, 2)
        tool_layout.addWidget(pos_br, 1, 3)
        
        left.addLayout(tool_layout)

        left.addWidget(self._divider())

        # 6. 辅助与安全
        left.addWidget(QLabel("6. 辅助功能与安全", objectName="fieldLabel"))
        
        # 防漏边背景填充（默认开启）
        self.bg_fill_cb = QCheckBox("添加外围白边（防止露出旧码）")
        self.bg_fill_cb.setChecked(True)
        self.bg_fill_cb.toggled.connect(self.update_qr_image)
        left.addWidget(self.bg_fill_cb)

        utility_layout = QHBoxLayout()
        utility_layout.setSpacing(6)
        
        self.scan_btn = QPushButton("🔍 识别原图二维码")
        self.scan_btn.setObjectName("smallBtn")
        self.scan_btn.setFixedHeight(32)
        self.scan_btn.setCursor(Qt.PointingHandCursor)
        self.scan_btn.setToolTip("自动识别背景图里的旧二维码，并把新生成的二维码放过去")
        self.scan_btn.clicked.connect(self.scan_qr_from_image)
        utility_layout.addWidget(self.scan_btn)
        
        self.clear_canvas_btn = QPushButton("🗑 清空画布")
        self.clear_canvas_btn.setObjectName("dangerBtn")
        self.clear_canvas_btn.setFixedHeight(32)
        self.clear_canvas_btn.setCursor(Qt.PointingHandCursor)
        self.clear_canvas_btn.clicked.connect(self.clear_canvas)
        utility_layout.addWidget(self.clear_canvas_btn)
        
        left.addLayout(utility_layout)

        # 填补下方空白的提示卡片
        tips_box = QFrame()
        tips_box.setObjectName("tipsBox")
        tips_layout = QVBoxLayout(tips_box)
        tips_layout.setContentsMargins(12, 10, 12, 10)
        tips_title = QLabel("💡 贴心提示")
        tips_title.setStyleSheet("font-weight: bold; color: #4f7cff; background: transparent;")
        tips_layout.addWidget(tips_title)
        tips_text = QLabel(
            "• 数据安全：未导出的工作退出时会自动暂存，下次打开可一键恢复。\n"
            "• 扫码保障：建议选「白底黑码」，如果遮挡了人像，可勾选透明并补充外圈白边。"
        )
        tips_text.setWordWrap(True)
        tips_text.setStyleSheet("color: #64748b; font-size: 12px; background: transparent;")
        tips_layout.addWidget(tips_text)
        left.addWidget(tips_box)

        left.addStretch(1)

        # 导出
        self.save_btn = QPushButton("导出最终照片（原画质）")
        self.save_btn.setObjectName("secondaryBtn")
        self.save_btn.setCursor(Qt.PointingHandCursor)
        self.save_btn.setEnabled(False)
        self.save_btn.clicked.connect(self.export_image)
        left.addWidget(self.save_btn)

        self.status = QLabel("提示：生成后左键按住即可拖拽")
        self.status.setObjectName("hint")
        self.status.setWordWrap(True)
        left.addWidget(self.status)

        root.addWidget(self.left_card)

        # 右侧画布
        self.right_card = QFrame()
        self.right_card.setObjectName("card")
        right = QVBoxLayout(self.right_card)
        right.setContentsMargins(10, 10, 10, 10)

        self.scene = QGraphicsScene(self)
        self.view = ImageEditorView(self.scene)
        right.addWidget(self.view)
        root.addWidget(self.right_card, 1)

    def _divider(self):
        d = QFrame()
        d.setObjectName("divider")
        d.setFixedHeight(1)
        return d

    # ==================== 颜色与 Logo 调节 ====================
    def set_fg_color(self, color):
        self.fg_color = color
        self._refresh_color_btns()
        self.update_qr_image()

    def set_bg_color(self, color):
        self.bg_color = color
        self._refresh_color_btns()
        self.bg_transparent_cb.setChecked(False)
        self.update_qr_image()

    def pick_fg(self):
        col = QColorDialog.getColor(QColor(self.fg_color), self, "选择二维码点颜色")
        if col.isValid():
            self.set_fg_color(col.name())

    def pick_bg(self):
        col = QColorDialog.getColor(QColor(self.bg_color), self, "选择二维码背景颜色")
        if col.isValid():
            self.set_bg_color(col.name())

    def on_bg_transparent_toggled(self, checked):
        self._refresh_color_btns()
        self.update_qr_image()

    def select_logo(self):
        path, _ = QFileDialog.getOpenFileName(self, "选择 Logo 图片", "", "图片 (*.png *.jpg *.jpeg)")
        if path:
            self.logo_path = path
            self.logo_btn.setText(f"已选择: {os.path.basename(path)[:10]}...")
            self.clear_logo_btn.setEnabled(True)
            self.update_qr_image()

    def clear_logo(self):
        self.logo_path = ""
        self.logo_btn.setText("插入 Logo (可选)")
        self.clear_logo_btn.setEnabled(False)
        self.update_qr_image()

    def _refresh_color_btns(self):
        for c, btn in self.fg_btns.items():
            if c == self.fg_color:
                btn.setStyleSheet(f"QPushButton {{ background-color: {c}; border: 3px solid #4f7cff; border-radius: 8px; }}")
            else:
                btn.setStyleSheet(f"QPushButton {{ background-color: {c}; border: 1px solid #ccc; border-radius: 8px; }}")

        is_transparent = self.bg_transparent_cb.isChecked()
        for c, btn in self.bg_btns.items():
            btn.setEnabled(not is_transparent)
            if is_transparent:
                btn.setStyleSheet(f"QPushButton {{ background-color: {c}; border: 1px solid #eee; border-radius: 8px; opacity: 0.5; }}")
            elif c == self.bg_color:
                btn.setStyleSheet(f"QPushButton {{ background-color: {c}; border: 3px solid #4f7cff; border-radius: 8px; }}")
            else:
                btn.setStyleSheet(f"QPushButton {{ background-color: {c}; border: 1px solid #ccc; border-radius: 8px; }}")

    def update_qr_image(self):
        if not self.qr_item or not self.qr_item.scene():
            return
            
        url = self.url_edit.text().strip()
        if not url:
            return

        current_rect = self.qr_item._rect
        current_pos = self.qr_item.pos()

        qr = qrcode.QRCode(error_correction=ERROR_CORRECT_H, border=1, box_size=10)
        qr.add_data(url)
        qr.make(fit=True)
        pil_img = qr.make_image(fill_color=self.fg_color, back_color=self.bg_color).convert("RGBA")
        
        if self.bg_transparent_cb.isChecked():
            px = pil_img.getdata()
            bg_rgb = tuple(int(self.bg_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
            pil_img.putdata([
                (r, g, b, 0) if (r, g, b) == bg_rgb else (r, g, b, a)
                for (r, g, b, a) in px
            ])

        # 强制外圈白边（防漏底）
        if self.bg_fill_cb.isChecked():
            new_w = pil_img.width + 30
            new_h = pil_img.height + 30
            bg_img = Image.new("RGBA", (new_w, new_h), (255, 255, 255, 255))
            bg_img.paste(pil_img, (15, 15), pil_img)
            pil_img = bg_img

        if self.logo_path and os.path.exists(self.logo_path):
            try:
                logo = Image.open(self.logo_path).convert("RGBA")
                logo_size = int(pil_img.width * 0.22)
                logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
                center_x = pil_img.width // 2
                center_y = pil_img.height // 2
                
                pad = 6
                bg_pad = Image.new("RGBA", (logo_size + pad*2, logo_size + pad*2), (255, 255, 255, 255))
                if self.bg_transparent_cb.isChecked() and not self.bg_fill_cb.isChecked():
                    bg_pad.putalpha(0)
                    draw = ImageDraw.Draw(bg_pad)
                    draw.rectangle([0, 0, bg_pad.width, bg_pad.height], outline=(255,255,255,255), width=pad)
                
                pil_img.paste(bg_pad, (center_x - bg_pad.width//2, center_y - bg_pad.height//2), bg_pad)
                pil_img.paste(logo, (center_x - logo_size//2, center_y - logo_size//2), logo)
            except Exception as e:
                print("Logo 生成失败:", e)

        data = pil_img.tobytes("raw", "RGBA")
        qimg = QImage(data, pil_img.width, pil_img.height, QImage.Format_RGBA8888)
        qr_pixmap = QPixmap.fromImage(qimg)

        self.qr_item._pixmap = qr_pixmap
        self.qr_item.orig_w = qr_pixmap.width()
        self.qr_item.orig_h = qr_pixmap.height()
        
        self.qr_item.prepareGeometryChange()
        self.qr_item._rect = current_rect
        self.qr_item.setPos(current_pos)
        self.qr_item.update()
        self.has_unsaved_changes = True

    # ==================== 辅助功能 ====================
    def scan_qr_from_image(self):
        if not self.bg_image_path:
            QMessageBox.warning(self, "提示", "请先导入一张包含旧二维码的背景照片！")
            return
            
        try:
            img = cv2.imdecode(np.fromfile(self.bg_image_path, dtype=np.uint8), cv2.IMREAD_COLOR)
            if img is None:
                QMessageBox.warning(self, "读取失败", "背景图无法解码，请重新导入。")
                return

            detector = cv2.QRCodeDetector()
            data, bbox, _ = detector.detectAndDecode(img)
            
            if data:
                self.url_edit.setText(data)
                
                if bbox is not None and len(bbox) > 0:
                    pts = bbox[0]
                    min_x = int(min(pt[0] for pt in pts))
                    max_x = int(max(pt[0] for pt in pts))
                    min_y = int(min(pt[1] for pt in pts))
                    max_y = int(max(pt[1] for pt in pts))
                    
                    w = max_x - min_x
                    h = max_y - min_y
                    
                    # 放大 1.2 倍，确保完全覆盖旧码白边
                    w_padded = int(w * 1.2)
                    h_padded = int(h * 1.2)
                    
                    cx = (min_x + max_x) / 2
                    cy = (min_y + max_y) / 2
                    
                    new_x = cx - w_padded / 2
                    new_y = cy - h_padded / 2
                    
                    if not self.qr_item:
                        self.insert_qr_to_canvas()
                        
                    if self.qr_item:
                        self.qr_item.prepareGeometryChange()
                        self.qr_item._rect.setSize(QSizeF(w_padded, h_padded))
                        self.qr_item.setPos(new_x, new_y)
                        self.qr_item.setSelected(True)
                        
                    self.status.setText("✓ 识别成功，并已覆盖旧二维码！")
                    self.has_unsaved_changes = True
                else:
                    self.status.setText("✓ 识别到了链接，但未找到坐标区域。")
            else:
                QMessageBox.warning(self, "识别失败", "未能从背景图中识别出二维码，请确认是否清晰。")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"图像识别出错了：\n{e}")

    def clear_canvas(self):
        self.scene.clear()
        self.bg_item = None
        self.qr_item = None
        self.bg_image_path = ""
        self.photo_btn.setText("点击选择本地照片 …")
        self.save_btn.setEnabled(False)
        self.status.setText("画布已清空，请重新导入照片。")
        self.has_unsaved_changes = False
        
        # 清空时同步删除暂存
        if os.path.exists(self.autosave_path):
            try:
                os.remove(self.autosave_path)
            except:
                pass

    # ==================== 快捷排版 ====================
    def quick_align(self, pos_type):
        if not self.qr_item or not self.bg_item:
            return
            
        bg_rect = self.bg_item.boundingRect()
        qr_w = self.qr_item._rect.width()
        qr_h = self.qr_item._rect.height()
        margin = 30

        if pos_type == "center":
            x = bg_rect.center().x() - qr_w / 2
            y = bg_rect.center().y() - qr_h / 2
        elif pos_type == "tl":
            x = bg_rect.left() + margin
            y = bg_rect.top() + margin
        elif pos_type == "tr":
            x = bg_rect.right() - qr_w - margin
            y = bg_rect.top() + margin
        elif pos_type == "bl":
            x = bg_rect.left() + margin
            y = bg_rect.bottom() - qr_h - margin
        elif pos_type == "br":
            x = bg_rect.right() - qr_w - margin
            y = bg_rect.bottom() - qr_h - margin
        
        self.qr_item.setPos(x, y)
        self.qr_item.setSelected(True)
        self.has_unsaved_changes = True

    def reset_size(self):
        if not self.qr_item:
            return
        self.qr_item.prepareGeometryChange()
        initial_scale = 0.25
        self.qr_item._rect.setSize(QSizeF(self.qr_item.orig_w * initial_scale, self.qr_item.orig_h * initial_scale))
        self.qr_item.setSelected(True)
        self.quick_align("center")

    # ==================== 核心：加载与插入 ====================
    def select_photo(self):
        path, _ = QFileDialog.getOpenFileName(self, "选择照片", "", "图片 (*.png *.jpg *.jpeg *.bmp)")
        if path:
            self.load_photo(path)

    def load_photo(self, path):
        self.bg_image_path = path
        pixmap = QPixmap(path)
        if pixmap.isNull():
            QMessageBox.warning(self, "错误", "无法加载该图片")
            return
            
        self.scene.clear()
        self.qr_item = None
        
        self.bg_item = self.scene.addPixmap(pixmap)
        self.bg_item.setFlag(QGraphicsPixmapItem.ItemIsMovable, False)
        self.bg_item.setFlag(QGraphicsPixmapItem.ItemIsSelectable, False)
        
        self.view.fitInView(self.bg_item, Qt.KeepAspectRatio)
        self.save_btn.setEnabled(True)
        self.photo_btn.setText(f"已加载: {os.path.basename(path)[:15]}...")
        self.has_unsaved_changes = True

    def insert_qr_to_canvas(self):
        if not self.bg_item:
            QMessageBox.warning(self, "提示", "请先导入一张背景照片")
            return
        url = self.url_edit.text().strip()
        if not url:
            QMessageBox.warning(self, "提示", "请输入链接")
            return

        qr = qrcode.QRCode(error_correction=ERROR_CORRECT_H, border=1, box_size=10)
        qr.add_data(url)
        qr.make(fit=True)
        
        pil_img = qr.make_image(fill_color=self.fg_color, back_color=self.bg_color).convert("RGBA")
        
        if self.bg_transparent_cb.isChecked():
            px = pil_img.getdata()
            bg_rgb = tuple(int(self.bg_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
            pil_img.putdata([
                (r, g, b, 0) if (r, g, b) == bg_rgb else (r, g, b, a)
                for (r, g, b, a) in px
            ])

        if self.bg_fill_cb.isChecked():
            new_w = pil_img.width + 30
            new_h = pil_img.height + 30
            bg_img = Image.new("RGBA", (new_w, new_h), (255, 255, 255, 255))
            bg_img.paste(pil_img, (15, 15), pil_img)
            pil_img = bg_img

        if self.logo_path and os.path.exists(self.logo_path):
            try:
                logo = Image.open(self.logo_path).convert("RGBA")
                logo_size = int(pil_img.width * 0.22)
                logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
                center_x = pil_img.width // 2
                center_y = pil_img.height // 2
                
                pad = 6
                bg_pad = Image.new("RGBA", (logo_size + pad*2, logo_size + pad*2), (255, 255, 255, 255))
                if self.bg_transparent_cb.isChecked() and not self.bg_fill_cb.isChecked():
                    bg_pad.putalpha(0)
                    draw = ImageDraw.Draw(bg_pad)
                    draw.rectangle([0, 0, bg_pad.width, bg_pad.height], outline=(255,255,255,255), width=pad)
                
                pil_img.paste(bg_pad, (center_x - bg_pad.width//2, center_y - bg_pad.height//2), bg_pad)
                pil_img.paste(logo, (center_x - logo_size//2, center_y - logo_size//2), logo)
            except Exception as e:
                print("Logo 生成失败:", e)
        
        data = pil_img.tobytes("raw", "RGBA")
        qimg = QImage(data, pil_img.width, pil_img.height, QImage.Format_RGBA8888)
        qr_pixmap = QPixmap.fromImage(qimg)

        if self.qr_item:
            self.scene.removeItem(self.qr_item)

        self.qr_item = ResizablePixmapItem(qr_pixmap)
        self.qr_item.deleted.connect(self.on_qr_deleted)
        
        bg_rect = self.bg_item.boundingRect()
        initial_scale = 0.25
        self.qr_item._rect.setSize(QSizeF(self.qr_item.orig_w * initial_scale, self.qr_item.orig_h * initial_scale))
        
        self.qr_item.setPos(
            bg_rect.center().x() - self.qr_item._rect.width()/2,
            bg_rect.center().y() - self.qr_item._rect.height()/2
        )
        
        self.scene.addItem(self.qr_item)
        self.qr_item.setSelected(True)
        self.status.setText("✓ 二维码已插入！")
        self.has_unsaved_changes = True

    def on_qr_deleted(self):
        self.qr_item = None
        self.status.setText("二维码已删除")
        self.has_unsaved_changes = True

    # ==================== 导出与备份 ====================
    def export_image(self):
        if not self.bg_item:
            return
        
        rect = self.bg_item.boundingRect()
        image = QImage(int(rect.width()), int(rect.height()), QImage.Format_ARGB32)
        image.fill(Qt.transparent)
        
        painter = QPainter(image)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        
        self.scene.clearSelection()
        self.scene.render(painter, target=QRectF(image.rect()), source=rect)
        painter.end()

        default_name = f"edited_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        path, _ = QFileDialog.getSaveFileName(
            self, "保存最终照片", default_name, "PNG 图片 (*.png);;JPEG 图片 (*.jpg)"
        )
        if path:
            if path.lower().endswith((".jpg", ".jpeg")):
                image = image.convertToFormat(QImage.Format_RGB32)
            image.save(path)
            QMessageBox.information(self, "成功", f"已成功导出：\n{os.path.basename(path)}")
            self.has_unsaved_changes = False
            
            # 导出成功后顺手清理暂存
            if os.path.exists(self.autosave_path):
                try:
                    os.remove(self.autosave_path)
                except:
                    pass

    def save_autosave(self):
        if not self.bg_item:
            return
            
        data = {
            "bg_path": self.bg_image_path,
            "url": self.url_edit.text(),
            "fg_color": self.fg_color,
            "bg_color": self.bg_color,
            "transparent": self.bg_transparent_cb.isChecked(),
            "logo_path": self.logo_path,
            "qr_x": self.qr_item.pos().x() if self.qr_item else 0,
            "qr_y": self.qr_item.pos().y() if self.qr_item else 0,
            "qr_w": self.qr_item._rect.width() if self.qr_item else 0,
            "qr_h": self.qr_item._rect.height() if self.qr_item else 0,
            "has_qr": self.qr_item is not None
        }
        try:
            with open(self.autosave_path, "w", encoding="utf-8") as f:
                json.dump(data, f)
        except Exception as e:
            print("应急保存失败:", e)

    def check_autosave(self):
        if not os.path.exists(self.autosave_path):
            return
            
        reply = QMessageBox.question(self, "恢复工作",
                                     "检测到上次有未完成的编辑，是否恢复？",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            try:
                with open(self.autosave_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                
                if os.path.exists(data["bg_path"]):
                    self.load_photo(data["bg_path"])
                    self.url_edit.setText(data["url"])
                    self.fg_color = data["fg_color"]
                    self.bg_color = data["bg_color"]
                    self.logo_path = data["logo_path"]
                    self.bg_transparent_cb.setChecked(data["transparent"])
                    self._refresh_color_btns()
                    
                    if data["has_qr"]:
                        self.insert_qr_to_canvas()
                        if self.qr_item:
                            self.qr_item.prepareGeometryChange()
                            self.qr_item._rect.setSize(QSizeF(data["qr_w"], data["qr_h"]))
                            self.qr_item.setPos(data["qr_x"], data["qr_y"])
                    
                    self.status.setText("✓ 上次的工作已成功恢复！")
                    self.has_unsaved_changes = True
            except Exception as e:
                print("恢复失败:", e)
        else:
            try:
                os.remove(self.autosave_path)
            except:
                pass

    def closeEvent(self, event):
        if self.has_unsaved_changes and self.bg_item:
            reply = QMessageBox.question(
                self, "确认退出",
                "当前编辑尚未导出，直接退出会丢失进度。\n是否退出？\n（退出后会自动暂存，下次打开可恢复）",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                self.save_autosave()
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

    # ==================== 拖拽与主题 ====================
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            if path.lower().endswith((".png", ".jpg", ".jpeg", ".bmp")):
                self.load_photo(path)
                break

    def _apply_theme(self):
        if self.theme_name == "light":
            self.setStyleSheet(LIGHT_QSS)
            self.theme_btn.setText("☾")
            shadow_color = QColor(15, 23, 42, 38)
        else:
            self.setStyleSheet(DARK_QSS)
            self.theme_btn.setText("☀")
            shadow_color = QColor(0, 0, 0, 120)
        
        for card in (self.left_card, self.right_card):
            sh = QGraphicsDropShadowEffect(card)
            sh.setBlurRadius(30)
            sh.setColor(shadow_color)
            sh.setOffset(0, 6)
            card.setGraphicsEffect(sh)
            
        self._refresh_color_btns()

    def toggle_theme(self):
        self.theme_name = "dark" if self.theme_name == "light" else "light"
        self.settings.setValue("theme", self.theme_name)
        self._apply_theme()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = QRCodeWindow()
    w.show()
    sys.exit(app.exec_())