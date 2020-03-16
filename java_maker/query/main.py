# -*- coding: utf-8 -*-
"""
@create: 2020-03-15 11:28:34.

@author: ppolxda

@desc: query_maker.py
"""
import os
import re
import glob
import json
import codecs
import argparse
import pkg_resources
from mako.template import Template


class TmplConfig(object):

    def __init__(self, output, prefix, tmpl, encoding):
        self.prefix = prefix
        self.xoutput = output
        self.tmpl = tmpl.replace('{tmpl}', self.env_tmpl)
        self.tmpl_name = os.path.basename(self.tmpl)
        # TODO - check format
        if not (self.tmpl_name.count('.') == 2 and
                self.tmpl_name.endswith('.mako')):
            raise TypeError('tmpl_name invaild {}'.format(self.tmpl_name))
        self.suffix = '.' + self.tmpl_name.split('.')[1]
        self.encoding = encoding
        self.tmpl.replace('{tmpl}', self.env_tmpl)
        with codecs.open(self.tmpl, encoding=self.encoding) as fs:
            self.tmpl = fs.read()

    def table_name(self, table):
        return self.prefix.capitalize() + table

    def output(self, table):
        o = os.path.join(
            self.xoutput, self.prefix,
            self.table_name(table) + self.suffix
        )
        return o

    @property
    def env_tmpl(self):
        DB_TMLP = os.environ.get('DB_TMLP', None)
        if DB_TMLP:
            return DB_TMLP

        return pkg_resources.resource_filename(
            'java_maker.query', os.path.join('', 'mako')
        )


class TmplConfigs(object):

    def __init__(self, output, tmpls, encoding):
        self.tmpls_str = tmpls
        self.encoding = encoding
        self.tmpls = [
            # TODO - check fmt
            TmplConfig(
                output,
                i.split(':')[0],
                i.split(':')[1],
                encoding
            )
            for i in tmpls.split(',')
        ]

    def loop_tmpls(self):
        for i in self.tmpls:
            yield i


class Cmdoptions(object):
    PKG_RE = re.compile(r'^[a-zA-Z\.]{1,}$')

    def __init__(self):
        self.cmds = self.parse_args()
        self.encoding = self.cmds.encoding
        self.project = self.cmds.project
        self.tmpls = self.cmds.tmpls
        self.output = self.cmds.output
        self.input = self.cmds.input

        if not self.input:
            raise TypeError('--input not set')

        # if not self.output:
        #     raise TypeError('--output not set')

        if not self.project:
            raise TypeError('--project not set')

        if not self.PKG_RE.match(self.project):
            raise TypeError('--project format invaild {}'.format(self.project))

        if not self.tmpls:
            raise TypeError('--tmpl not set')

        # self.input = os.path.join(
        #     os.path.abspath(self.input),
        #     self.project.replace('.', '/')
        # )

        self.input = os.path.abspath(self.input)

        if self.output:
            self.output = os.path.abspath(self.output)
        else:
            self.output = self.input

        if not os.path.isdir(self.input):
            raise TypeError('--input invaild, input must is directory')

        if not os.path.isdir(self.output):
            raise TypeError('--output invaild, input must is directory')

        self.input = self.input.replace('\\', '/')
        self.input_glob = self.input + '/**/*[!_history]*.json'
        self.output = self.output.replace('\\', '/')
        self.tmpls = TmplConfigs(self.output, self.tmpls, self.encoding)

    @property
    def package_path(self):
        return 'query_maker'

    def parse_args(self):
        parser = argparse.ArgumentParser(description=self.package_path)

        parser.add_argument('-i', '--input',
                            default=None,
                            help='query json config')  # noqa

        parser.add_argument('-o', '--output',
                            default=None,
                            help='query json output config')  # noqa

        parser.add_argument(
            '-t', '--tmpls',
            default='query:{tmpl}/query.java.mako,dto:{tmpl}/dto.java.mako',
            help='tmpls path'
        )

        parser.add_argument('-p', '--project',
                            default=None,
                            help='project name')  # noqa

        # parser.add_argument('-c', '--config',
        #                     default=self.default_config_path,
        #                     help='templates json path ({tmpl} default pydbgen/swagger/)')  # noqa

        parser.add_argument('-e', '--encoding',
                            default='utf8',
                            help='output encoding(default: utf8)')

        return parser.parse_args()

    def loop_json(self):
        if self.input:
            pass

        config_lists = glob.glob(self.input_glob, recursive=True)
        for file_path in config_lists:
            file_path = file_path.replace('\\', '/')
            table_name = os.path.basename(file_path).replace('.json', '')
            with codecs.open(file_path, encoding=self.encoding) as fs:
                query_json = json.loads(fs.read())

            yield file_path, table_name, query_json


def generate_file(tmpl, **kwargs):
    """generate_file."""
    # template_loader = template.Loader(options.fs_tmpl)
    return Template(tmpl).render(**kwargs)


def fmt_print(output, table_name, config):
    return '\n'.join([
        'in:' + str(input),
        'out:' + str(output),
        'table:' + str(table_name),
        'config:' + str(config),
    ])


def main():
    cmds = Cmdoptions()
    cmds.parse_args()

    for file_path, table_name, query_json in cmds.loop_json():
        for tmpl in cmds.tmpls.loop_tmpls():
            out_path = tmpl.output(table_name)
            print(fmt_print(out_path, table_name, query_json))

            context = generate_file(
                tmpl.tmpl,
                table=tmpl.table_name(table_name),
                project=cmds.project,
                config=query_json
            )

            try:
                os.makedirs(os.path.dirname(out_path))
            except FileExistsError:
                pass

            with codecs.open(out_path, 'w', encoding=tmpl.encoding) as fs:
                fs.write(context)


if __name__ == '__main__':
    main()
