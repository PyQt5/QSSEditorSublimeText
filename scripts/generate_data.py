#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2022/05/26
@author: Irony
@site: https://pyqt.site https://github.com/PyQt5
@email: 892768447@qq.com
@file: generate_data.py
@description:
"""

from collections import OrderedDict
import json
import os
import sys

Widgets = [
    'QAbstractButton', 'QAbstractItemView', 'QAbstractScrollArea',
    'QAbstractSlider', 'QAbstractSpinBox', 'QCalendarWidget', 'QCheckBox',
    'QColorDialog', 'QColumnView', 'QComboBox', 'QCommandLinkButton',
    'QDateEdit', 'QDateTimeEdit', 'QDial', 'QDialog', 'QDialogButtonBox',
    'QDockWidget', 'QDoubleSpinBox', 'QErrorMessage', 'QFileDialog',
    'QFocusFrame', 'QFontComboBox', 'QFontDialog', 'QFrame', 'QGraphicsView',
    'QGroupBox', 'QHeaderView', 'QInputDialog', 'QKeySequenceEdit',
    'QLCDNumber', 'QLabel', 'QLineEdit', 'QListView', 'QListWidget',
    'QMainWindow', 'QMdiArea', 'QMdiSubWindow', 'QMenu', 'QMenuBar',
    'QMessageBox', 'QOpenGLWidget', 'QPlainTextEdit', 'QProgressBar',
    'QProgressDialog', 'QPushButton', 'QRadioButton', 'QRubberBand',
    'QScrollArea', 'QScrollBar', 'QSizeGrip', 'QSlider', 'QSpinBox',
    'QSplashScreen', 'QSplitter', 'QSplitterHandle', 'QStackedWidget',
    'QStatusBar', 'QTabBar', 'QTabWidget', 'QTableView', 'QTableWidget',
    'QTextBrowser', 'QTextEdit', 'QTimeEdit', 'QToolBar', 'QToolBox',
    'QToolButton', 'QTreeView', 'QTreeWidget', 'QUndoView', 'QWidget',
    'QWizard', 'QWizardPage'
]


def generate_completions():
    result = OrderedDict()
    result['scope'] = [
        'source.css', 'meta.selector.css', 'entity.name.tag.html.css',
        'source.qss'
    ]

    completions = []
    for widget in Widgets:
        tmp = OrderedDict()
        tmp['trigger'] = widget
        tmp['contents'] = widget
        tmp['kind'] = 'markup'
        completions.append(tmp)

    result['completions'] = completions

    open(
        os.path.join(os.path.dirname(os.path.dirname(sys.argv[0])),
                     'QSSEditor.sublime-completions'),
        'wb').write(json.dumps(result, indent=4).encode())


if __name__ == '__main__':
    generate_completions()
