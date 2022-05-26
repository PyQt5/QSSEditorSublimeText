from __future__ import absolute_import, print_function

import logging
import os
import sys

import sublime
import sublime_plugin

sys.path.append(os.path.join(os.path.dirname(__file__), 'site-packages'))

from qsseditor.Client import QSSEditorClient
from qsseditor.Utils import PLUGIN_NAME, get_setting, init_log, is_support


class QSSEditorWatcher(sublime_plugin.EventListener):
    """事件监听"""

    def on_modified(self, view):
        """
        文档被修改
        :param view: sublime.View
        """
        if not is_support(view.file_name(), view.syntax()):
            return
        logging.getLogger(PLUGIN_NAME).debug('QSSEditorWatcher::on_modified')
        if QSSEditorClient.Client:
            QSSEditorClient.Client.applyStyleAsync(view, True)

    def on_load(self, view):
        """
        文档被加载
        :param view: sublime.View
        """
        if not is_support(view.file_name(), view.syntax()):
            return
        logging.getLogger(PLUGIN_NAME).debug('QSSEditorWatcher::on_load')
        if QSSEditorClient.Client:
            QSSEditorClient.Client.applyStyleAsync(view)

    def on_post_save(self, view):
        """
        文档被保存
        :param view: sublime.View
        """
        if not is_support(view.file_name(), view.syntax()):
            return
        logging.getLogger(PLUGIN_NAME).debug('QSSEditorWatcher::on_post_save')
        if QSSEditorClient.Client:
            QSSEditorClient.Client.applyStyleAsync(view)

    def on_query_completions(self, view, prefix, locations):
        """
        自动补全查询
        :param view: sublime.View
        :param prefix: 前缀
        :param locations: 位置
        """
        if not is_support(view.file_name(), view.syntax()):
            return
        logging.getLogger(PLUGIN_NAME).debug(
            'QSSEditorWatcher::on_query_completions: prefix={}, locations={}'.
            format(prefix, locations))

        if QSSEditorClient.Client:
            return QSSEditorClient.Completions
        return None


class QssApplyStyleCommand(sublime_plugin.TextCommand):
    """应用样式命令"""

    def run(self, edit):
        if QSSEditorClient.Client:
            QSSEditorClient.Client.applyStyleAsync(self.view)

    def is_visible(self):
        return is_support(self.view.file_name(), self.view.syntax())


def plugin_loaded():
    """插件被加载"""
    if QSSEditorClient.Client is None:
        # 只初始化一次
        init_log(os.path.join(os.path.dirname(__file__), PLUGIN_NAME + '.log'),
                 level=getattr(logging, get_setting(None, 'debug_level',
                                                    'INFO'), logging.INFO))
    QSSEditorClient.Client = QSSEditorClient()
    QSSEditorClient.Client.start()
    logging.getLogger(PLUGIN_NAME).debug('plugin_loaded')


def plugin_unloaded():
    """插件被卸载"""
    if QSSEditorClient.Client:
        QSSEditorClient.Client.stop()
    logging.getLogger(PLUGIN_NAME).debug('plugin_unloaded')
