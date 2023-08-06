"""
This module is part of the 'web-compressor' package,
which is released under GPL-3.0-only license.
"""

import functools
import operator
from pathlib import Path
from typing import Any, Dict, Union

import xdg

from ..utils import dump_toml, load_toml


class Config:
    """
    Handles configuration
    """

    def __init__(self, config_file: Union[Path, str, None] = None) -> None:
        """
        Constructor

        :param config_file: pathlib.Path | str | None Path to config file
        :return: None
        """

        # Define fallback for config directory
        config_path = Path(xdg.xdg_config_home(), "webcompr")

        # If not specified ..
        if config_file is None:
            # .. set fallback for config file
            config_file = config_path / "config.toml"

        # .. otherwise ..
        else:
            # .. use provided directory
            config_file = Path(config_file)
            config_path = config_file.parent

        # If it does not exist ..
        if not config_file.exists():
            # .. create config file ..
            config_path.mkdir(parents=True, exist_ok=True)
            dump_toml(self.defaults(), config_file)

        # Load its contents
        self.config = load_toml(config_file)

    def defaults(self) -> Dict[str, Any]:
        """
        Provides default settings

        :return: dict
        """

        return {
            # (1) Minifier
            "minify": {
                "options": {
                    "css-precision": 0,
                    "html-keep-comments": False,
                    "html-keep-conditional-comments": False,
                    "html-keep-default-attr-vals": False,
                    "html-keep-document-tags": False,
                    "html-keep-end-tags": False,
                    "html-keep-whitespace": False,
                    "html-keep-quotes": False,
                    "js-precision": 0,
                    "js-keep-var-names": False,
                    "js-no-nullish-operator": False,
                    "json-precision": 0,
                    "json-keep-numbers": False,
                    "svg-keep-comments": False,
                    "svg-precision": 0,
                    "xml-keep-whitespace": False,
                    # For more information,
                    # see https://github.com/tdewolff/minify/tree/master/bindings/py
                },
            },
            # (2) Optimizer
            "images": {
                "optimize": {
                    "quality": 75,
                    "strip_meta": True,
                },
                "convert": {
                    "avif": {"quality": 90},
                    "webp": {"method": 6},
                },
            },
            # (3) Hasher
            "hashing": {
                "hash_length": 10,
                "use_mtime": False,
                "sri": {
                    "digest": "sha512",
                },
                "csp": {
                    "digest": "sha512",
                },
            },
        }

    def get(self, option: str, fallback: Union[Any, None] = None) -> Any:
        """
        Retrieves data from config object

        :param option: str Option name
        :param fallback: Any Fallback value
        :return: Any
        """

        # If you see the hole ..
        if "." in option:
            # .. follow the white rabbit
            try:
                return functools.reduce(
                    operator.getitem, option.split("."), self.config
                )

            # If you cannot make it on your own ..
            except KeyError:
                # .. wait for reinforcements
                return fallback

        return self.config.get(option, fallback)
