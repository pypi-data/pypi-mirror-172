# Copyright (c) 2022  Peter Pentchev <roam@ringlet.net>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.
"""Test the UTF-8 locale detection class."""

from __future__ import annotations

from typing import Iterable

import ddt  # type: ignore

import utf8_locale

from . import test_detect


def test_utf8_env() -> None:
    """Test get_utf8_env() and, indirectly, detect_utf8_locale()."""
    env = utf8_locale.UTF8Detect().detect().env
    test_detect.check_env(env)

    mod_env = test_detect.get_mod_env()
    env2 = utf8_locale.UTF8Detect(env=mod_env).detect().env
    test_detect.check_mod_env(env, mod_env, env2)


@ddt.ddt
class TestLanguages(test_detect.TestLanguages):
    """Run the same tests using the UTF8Detect object."""

    @staticmethod
    def detect_locale(languages: Iterable[str]) -> str:
        with test_detect.mock_locale():  # type: ignore
            return utf8_locale.UTF8Detect(languages=languages).detect().locale

    @staticmethod
    def get_vars(languages: Iterable[str]) -> dict[str, str]:
        with test_detect.mock_locale():  # type: ignore
            return utf8_locale.UTF8Detect(languages=languages).detect().env_vars

    @staticmethod
    def get_langs(env: dict[str, str]) -> list[str]:
        return utf8_locale.LanguagesDetect(env=env).detect()
