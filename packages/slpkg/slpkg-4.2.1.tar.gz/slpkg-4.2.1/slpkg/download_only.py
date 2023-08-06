#!/usr/bin/python3
# -*- coding: utf-8 -*-


from dataclasses import dataclass

from slpkg.downloader import Wget
from slpkg.configs import Configs
from slpkg.queries import SBoQueries
from slpkg.views.views import ViewMessage
from slpkg.models.models import session as Session


@dataclass
class Download:
    flags: list
    session: str = Session
    download_only = Configs.download_only
    sbo_repo_url: str = Configs.sbo_repo_url
    sbo_tar_suffix: str = Configs.sbo_tar_suffix

    def packages(self, slackbuilds: list):

        view = ViewMessage(self.flags)
        view.download_packages(slackbuilds)
        view.question()
        wget = Wget()

        for sbo in slackbuilds:
            file = f'{sbo}{self.sbo_tar_suffix}'
            location = SBoQueries(sbo).location()
            url = f'{self.sbo_repo_url}/{location}/{file}'

            wget.download(self.download_only, url)

            sources = SBoQueries(sbo).sources()
            for source in sources.split():
                wget.download(self.download_only, source)
