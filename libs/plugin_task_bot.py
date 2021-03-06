# -*- encoding: utf-8 -*-
# author: binux<17175297.hk@gmail.com>

import logging
import requests
from flexget.plugin import register_plugin, PluginError
from flexget import validator

log = logging.getLogger("task_bot")

class PluginTaskBot(object):
    def __init__(self):
        pass

    def validator(self):
        root = validator.factory()
        advanced = root.accept("dict")
        advanced.accept("text", key="host")
        advanced.accept("text", key="tags")
        return root

    def prepare_config(self, config):
        if "host" not in config:
            config['host'] = "localhost:8880"
        if "tags" not in config:
            config['tags'] = ""
        return config

    def on_feed_download(self, feed, config):
        for entry in feed.accepted:
            if feed.manager.options.test:
                log.info("Would add %s to %s" % (entry['url'], config['host']))
                continue
            data = dict(
                    url = entry['url'],
                    title = entry['title'],
                    tags = config['tags']
                    )
            try:
                r = requests.post("http://"+config['host']+"/add_task", data=data)
                assert "task_id" in r.content
            except Exception:
                feed.fail(entry, "Add task error")
            log.info('"%s" added to %s' % (entry['title'], config['host']))

register_plugin(PluginTaskBot, "task_bot", api_ver=2)
