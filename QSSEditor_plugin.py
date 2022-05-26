from __future__ import absolute_import, print_function

import logging
import os
import sys

import sublime
import sublime_plugin

sys.path.append(os.path.join(os.path.dirname(__file__), 'site-packages'))

from qsseditor import Client
from qsseditor.Utils import PLUGIN_NAME, get_setting, init_log


class QSSEditorWatcher(sublime_plugin.EventListener):
    """事件监听"""

    def __init__(self, *args, **kwargs):
        super(QSSEditorWatcher, self).__init__(*args, **kwargs)
        logging.getLogger(PLUGIN_NAME).debug('QSSEditorWatcher::__init__')

    def on_modified(self, view):
        """
        文档被修改
        :param view: sublime.View
        """
        logging.getLogger(PLUGIN_NAME).debug('QSSEditorWatcher::on_modified')

    def on_load(self, view):
        """
        文档被加载
        :param view: sublime.View
        """
        logging.getLogger(PLUGIN_NAME).debug('QSSEditorWatcher::on_load')

    def on_post_save(self, view):
        """
        文档被保存
        :param view: sublime.View
        """
        logging.getLogger(PLUGIN_NAME).debug('QSSEditorWatcher::on_post_save')

    def on_query_completions(self, view, prefix, locations):
        """
        自动补全查询
        :param view: sublime.View
        :param prefix: 前缀
        :param locations: 位置
        """
        logging.getLogger(PLUGIN_NAME).debug(
            'QSSEditorWatcher::on_post_save: prefix={}, locations={}'.format(
                prefix, locations))
        if not prefix.startswith('#'):
            return None


class QssApplyStyleCommand(sublime_plugin.TextCommand):
    """应用样式命令"""

    def __init__(self, *args, **kwargs):
        super(QssApplyStyleCommand, self).__init__(*args, **kwargs)
        logging.getLogger(PLUGIN_NAME).debug('QSSEditorWatcher::__init__')

    def run(self, edit):
        if Client.Client:
            Client.Client.applyStyle(self.view)


def plugin_loaded():
    """插件被加载"""
    init_log(os.path.join(os.path.dirname(__file__), PLUGIN_NAME + '.log'),
             level=getattr(logging, get_setting(None, 'debug_level', 'INFO'),
                           logging.INFO))
    print(dir(Client))
    print(dir(Client.QSSEditorClient))
    if Client.Client is None:
        Client.Client = Client.QSSEditorClient()
        Client.Client.start()
    logging.getLogger(PLUGIN_NAME).debug('plugin_loaded')


def plugin_unloaded():
    """插件被卸载"""
    print(dir(Client))
    if Client.Client:
        if Client.Client:
            Client.Client.stop()
    logging.getLogger(PLUGIN_NAME).debug('plugin_unloaded')
