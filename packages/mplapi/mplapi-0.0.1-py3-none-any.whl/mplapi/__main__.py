import argparse
import os


def create_plugin(plugin_name):
    if not (os.path.exists(PLUGIN_PATH)):
        os.mkdir(PLUGIN_PATH)
    if not (os.path.exists(f'{PLUGIN_PATH}/{init_file}')):
        with open(f'{PLUGIN_PATH}/{init_file}', 'w', encoding='utf-8') as file:
            pass
    if not (os.path.exists(f'{PLUGIN_PATH}/{plugin_name}')):
        os.mkdir(f'{PLUGIN_PATH}/{plugin_name}')
    if not (os.path.exists(f'{PLUGIN_PATH}/{plugin_name}/{init_file}')):
        file_lines = '\n'.join([
            'from mplapi.plugin import PyPlugin',
            'from mplapi.mirai import Bot',
            'from mplapi.mirai import msg',
            'from mplapi.plugin import catch_async_exception',
            '',
            '',
            f'class {plugin_name}Class(PyPlugin):',
            '\tpass',
        ])
        with open(f'{PLUGIN_PATH}/{plugin_name}/{init_file}', 'w', encoding='utf-8') as file:
            file.write(file_lines)
        print('创建完成')


if __name__ == '__main__':
    PLUGIN_PATH = 'plugins'
    init_file = '__init__.py'
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--new', help="新建插件项目")
    args = parser.parse_args()
    plugin_name = args.new
    if plugin_name is None:
        parser.print_help()
    else:
        create_plugin(plugin_name)
