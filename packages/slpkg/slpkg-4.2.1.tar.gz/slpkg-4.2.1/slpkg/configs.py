#!/usr/bin/python3
# -*- coding: utf-8 -*-


import os
import yaml

from dataclasses import dataclass


@dataclass
class Configs:

    # Programme name
    prog_name: str = 'slpkg'

    ''' Default configurations. '''
    # OS architecture by default
    os_arch: str = 'x86_64'

    # All necessary paths
    tmp_path: str = '/tmp'
    tmp_slpkg: str = f'{tmp_path}/{prog_name}'
    build_path: str = f'/tmp/{prog_name}/build'
    download_only: str = f'{tmp_slpkg}/'
    lib_path: str = f'/var/lib/{prog_name}'
    etc_path: str = f'/etc/{prog_name}'
    db_path: str = f'/var/lib/{prog_name}/database'
    sbo_repo_path: str = f'/var/lib/{prog_name}/repository'
    log_packages: str = '/var/log/packages'

    # Database name
    database: str = f'database.{prog_name}'

    # SBo repository configs
    sbo_repo_url: str = 'http://slackbuilds.org/slackbuilds/15.0'
    sbo_txt: str = 'SLACKBUILDS.TXT'
    sbo_tar_suffix: str = '.tar.gz'
    sbo_repo_tag: str = '_SBo'

    # Slackware commands
    installpkg: str = 'upgradepkg --install-new'
    reinstall: str = 'upgradepkg --reinstall'
    removepkg: str = 'removepkg'

    # Cli menu colors configs
    colors: str = 'on'

    # Wget options
    wget_options = '-c -N'

    # Creating the build path
    if not os.path.isdir(build_path):
        os.makedirs(build_path)

    ''' Overwrite with user configuration. '''
    config_file: str = f'{etc_path}/{prog_name}.yml'
    if os.path.isfile(config_file):
        with open(config_file, 'r') as conf:
            configs = yaml.safe_load(conf)

        try:

            config = configs['configs']

            # OS architecture by default
            os_arch: str = config['os_arch']

            # All necessary paths
            tmp_path: str = config['tmp_path']
            tmp_slpkg: str = config['tmp_slpkg']
            build_path: str = config['build_path']
            download_only: str = config['download_only']
            lib_path: str = config['lib_path']
            etc_path: str = config['etc_path']
            db_path: str = config['db_path']
            sbo_repo_path: str = config['sbo_repo_path']
            log_packages: str = config['log_packages']

            # Database name
            database: str = config['database']

            # SBo repository details
            sbo_repo_url: str = config['sbo_repo_url']
            sbo_txt: str = config['sbo_txt']
            sbo_tar_suffix: str = config['sbo_tar_suffix']
            sbo_repo_tag: str = config['sbo_repo_tag']

            # Slackware commands
            installpkg: str = config['installpkg']
            reinstall: str = config['reinstall']
            removepkg: str = config['removepkg']

            # Cli menu colors configs
            colors: str = config['colors']

            # Wget options
            wget_options: str = config['wget_options']

        except KeyError:
            pass

    @classmethod
    def colour(cls):
        color = {
            'BOLD': '',
            'RED': '',
            'GREEN': '',
            'YELLOW': '',
            'CYAN': '',
            'BLUE': '',
            'GREY': '',
            'ENDC': ''
        }

        if cls.colors:
            color = {
                'BOLD': '\033[1m',
                'RED': '\x1b[91m',
                'GREEN': '\x1b[32m',
                'YELLOW': '\x1b[93m',
                'CYAN': '\x1b[96m',
                'BLUE': '\x1b[94m',
                'GREY': '\x1b[38;5;247m',
                'ENDC': '\x1b[0m'
            }

        return color
