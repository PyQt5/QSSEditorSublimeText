import functools
import sublime
import sublime_plugin
from time import sleep
from threading import Thread

PLUGIN_NAME = 'QSSEditor'
SETTINGS_FILENAME = '{0}.sublime-settings'.format(PLUGIN_NAME)


def get_setting(view, key, default_value=None):
    settings = view.settings().get(PLUGIN_NAME) if view else None
    if settings is None or settings.get(key) is None:
        settings = sublime.load_settings(SETTINGS_FILENAME)
    return settings.get(key, default_value)


class QSSEditorClient(Thread):

    def __init__(self, *args, **kwargs):
        super(QSSEditorClient, self).__init__(*args, **kwargs)
        print('QSSEditorClient::__init__')
        self.m_valid = True

    def setValid(self, valid):
        self.m_valid = valid

    def _applyStyle(self, style=[]):
        print('QSSEditorClient::applyStyle: ', style)

    def applyStyle(self, view=None):
        if view is None:
            view = sublime.active_window().active_view()

        # 获取选中的内容
        styleSheets = [
            view.substr(sublime.Region(region.a, region.b))
            for region in view.sel()
            if not region.empty()
        ]
        styleSheets = [
            text for text in styleSheets if text.strip().strip('\r').strip('\n')
        ]

        if len(styleSheets) == 0:
            # 获取全部内容
            styleSheets.append(view.substr(sublime.Region(0, view.size())))

        if len(styleSheets) == 0:
            return

        self._applyStyle(styleSheets)

    def run(self):
        while self.m_valid:
            sleep(3)


g_client = QSSEditorClient()
g_client.start()


class QSSEditorWatcher(sublime_plugin.EventListener):

    def __init__(self, *args, **kwargs):
        super(QSSEditorWatcher, self).__init__(*args, **kwargs)
        print('QSSEditorWatcher::__init__')

    def on_modified(self, view):
        print('QSSEditorWatcher::on_modified')

    def on_load(self, view):
        print('QSSEditorWatcher::on_load')

    def on_post_save(self, view):
        print('QSSEditorWatcher::on_post_save')

    def on_query_completions(self, view, prefix, locations):
        print('QSSEditorWatcher::on_post_save: prefix={}, locations={}'.format(
            prefix, locations))
        if not prefix.startswith('#'):
            return None


class QssApplyStyleCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        g_client.applyStyle(self.view)
