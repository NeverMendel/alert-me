import logging
import os

from alert_me.plugin import Plugin
from alert_me.plugins.telegram import TelegramPlugin
from alert_me.plugins.url import UrlPlugin

from configparser import ConfigParser


CONFIG_FILE = "~/.alert-me.ini"

_plugins: dict[str, Plugin] = {
    TelegramPlugin.name: TelegramPlugin,
    UrlPlugin.name: UrlPlugin,
}


def register_plugin(self, plugin: Plugin) -> None:
    if plugin.name in _plugins:
        raise Exception(f"Plugin with name '{plugin.name}' is already registered")
    _plugins[plugin.name] = plugin


def get_config(*args: list[str]) -> list[Plugin]:
    logging.debug(f"Reading config from '{CONFIG_FILE}'. Installed plugins: {_plugins}")

    config: list[Plugin] = []

    parser = ConfigParser()
    parser.read(os.path.expanduser(CONFIG_FILE))

    logging.debug(f"ConfigParser sections: {parser.sections()}")

    for config_name in args:
        if config_name not in parser:
            raise Exception(f"Config {config_name} not found")
        section = parser[config_name]
        plugin_name = section["plugin"]
        if plugin_name not in _plugins:
            raise Exception(f"Plugin {plugin_name} not found")
        plugin_params = {}
        for param in section:
            if param == "plugin" or param == "default":
                continue
            plugin_params[param] = section[param]
        plugin_class = _plugins[plugin_name]
        plugin = plugin_class(plugin_params)
        config.append(plugin)

    return config


def get_plugin(plugin_name: str) -> Plugin:
    if plugin_name not in _plugins:
        raise Exception(f"Plugin {plugin_name} not found")
    return _plugins[plugin_name]
