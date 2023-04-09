import copy
import os
import re
import json
from typing import List

from amiyabot import Message, Chain
from core import bot as main_bot
from core import log
from core.customPluginInstance import AmiyaBotPluginInstance
from core.customPluginInstance.amiyaBotPluginInstance import global_config_channel_key
from core.database.plugin import PluginConfiguration

curr_dir = os.path.dirname(__file__)

global_loaded_switch = False

async def custom_verify_verify(data: Message, config_name, switch_key, old_func):

    if not global_loaded_switch:
        return await old_func(data)

    channel_id = "0"
    if hasattr(data, "channel_id"):
        channel_id = data.channel_id

    switch = bot.get_config(switch_key, channel_id)

    if not switch:
        return await old_func(data)

    switch = bot.get_config(config_name, channel_id)

    if not switch:
        return False, 0

    return await old_func(data)


async def multi_keyword_verify(data: Message, config_name, switch_key, level, old_array):

    channel_id = "0"
    if hasattr(data, "channel_id"):
        channel_id = data.channel_id

    text = ""
    if hasattr(data, "text"):
        text = data.text

    if not global_loaded_switch:
        if any(substring in text for substring in old_array):
            return True, level
        return False, 0


    switch = bot.get_config(switch_key, channel_id)

    if not switch:
        if any(substring in text for substring in old_array):
            return True, level
        return False, 0

    array = bot.get_config(config_name, channel_id)

    # log.info(f'{config_name}-{channel_id} {array}')
    if array is None or array == [] or (not isinstance(array, list)):
        return False, 0

    if any(substring in text for substring in array):
        return True, level
    return False, 0


def make_custom_verify_verify(config_key, switch_key, old_func):
    return lambda data: custom_verify_verify(data, config_key, switch_key, old_func)


def make_multi_keyword_verify(config_key, switch_key, level, old_array):
    return lambda data: multi_keyword_verify(data, config_key, switch_key, level, old_array)


class PluginConfigDemoPluginInstance(AmiyaBotPluginInstance):
    def load(self):

        log.info('正在生成配置项')

        propertys = {}
        config_schema = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "properties": propertys
        }
        config_default = {}
        for _, plugin in main_bot.plugins.items():

            if plugin.plugin_id == 'amiyabot-hsyhhssyy-functions-gui':
                continue

            plugin_overall_key = f"{plugin.plugin_id}-{plugin.version}-global"

            config_default[plugin_overall_key] = False
            propertys[plugin_overall_key] = {
                "title": f"全局开关：{plugin.name}",
                "description": f"{plugin.description}",
                "type": "boolean"
            }

            try:

                # handler 处理
                handlers = plugin.get_container('message_handlers')
                for i in range(len(handlers)):
                    handler = handlers[i]

                    if handler.keywords is not None:
                        key = f"{plugin.plugin_id}-{plugin.version}-handler-keyword-{i}"
                        config_default[key] = handler.keywords[:]
                        propertys[key] = {
                            "title": f"消息处理器{i+1}",
                            "type": "array"
                        }
                        handler.custom_verify = make_multi_keyword_verify(
                            key, plugin_overall_key, handler.level, handler.keywords)
                        handler.keywords = None
                        handler.level = None
                    elif handler.custom_verify is not None:
                        key = f"{plugin.plugin_id}-{plugin.version}-handler-custom_verify-{i}"
                        config_default[key] = True
                        propertys[key] = {
                            "title": f"消息处理器{i+1}",
                            "type": "boolean"
                        }
                        handler.custom_verify = make_custom_verify_verify(
                            key, plugin_overall_key, handler.custom_verify)
                        handler.keywords = None
                        handler.level = None

            except Exception as e:
                log.error(e, f"Error: {plugin.plugin_id}")

        self._AmiyaBotPluginInstance__channel_config_default = self._AmiyaBotPluginInstance__parse_to_json(
            config_default)
        self._AmiyaBotPluginInstance__channel_config_schema = self._AmiyaBotPluginInstance__parse_to_json(
            config_schema)
        self._AmiyaBotPluginInstance__global_config_default = self._AmiyaBotPluginInstance__parse_to_json(
            config_default)
        self._AmiyaBotPluginInstance__global_config_schema = self._AmiyaBotPluginInstance__parse_to_json(
            config_schema)

        global global_loaded_switch
        global_loaded_switch = True

        try:

            # 我来检查所有配置项并进行强制比对
            configs: List[PluginConfiguration] = PluginConfiguration.select().where(
                PluginConfiguration.plugin_id == self.plugin_id
            )


            for channel_conf in configs:
                channel_conf_json = json.loads(channel_conf.json_config)
                # 补充新的配置项
                diff_dict = {key: copy.deepcopy(
                    value) for key, value in config_default.items() if key not in channel_conf_json}
                channel_conf_json.update(diff_dict)
                
                log.info(f'{channel_conf_json}')

                if channel_conf.channel_id == global_config_channel_key:
                    self._AmiyaBotPluginInstance__set_global_config(channel_conf_json)
                else:
                    self._AmiyaBotPluginInstance__set_channel_config(channel_conf.channel_id,channel_conf_json)
                
        
        except Exception as e:
                log.error(e, f"Error: {plugin.plugin_id}")

        log.info('配置项生成完毕')

bot = PluginConfigDemoPluginInstance(
    name='超级功能开关',
    version='1.1',
    plugin_id='amiyabot-hsyhhssyy-functions-gui',
    plugin_type='',
    description='一个可以通过图形界面开关插件子功能的插件',
    document=f'{curr_dir}/README.md'
)


@bot.on_message(keywords=['重置超级功能开关'], check_prefix=False, direct_only=True)
async def _(data: Message):

    PluginConfiguration.delete().where(PluginConfiguration.plugin_id ==
                                       'amiyabot-hsyhhssyy-functions-gui').execute()

    return Chain(data).text(f'配置项删除完毕')
