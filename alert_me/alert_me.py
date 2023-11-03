import logging

from alert_me.plugin import Plugin


class AlertMe:
    def __init__(self, plugins: list[Plugin]):
        self._plugins = plugins

    def notify(self, notify_params: dict[str, any]) -> None:
        for plugin in self._plugins:
            plugin.notify(**notify_params)

    def notify(self, *args: list[str]) -> None:
        for plugin in self._plugins:
            plugin.notify_args(*args)
