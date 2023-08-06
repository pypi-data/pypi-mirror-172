import logging
import os
from configparser import ConfigParser
from typing import Optional

class ConfigHandler:
    def __init__(
        self,
        source_dir: Optional[str],
        html_output_dir: Optional[str],
        gemini_output_dir: Optional[str],
        gopher_output_dir: Optional[str],
        css_template_path: Optional[str]
    ) -> None:
        self.source_dir = source_dir
        self.html_output_dir = html_output_dir
        self.gemini_output_dir = gemini_output_dir
        self.gopher_output_dir = gopher_output_dir
        self.css_template_path = css_template_path

        if not self._all_parameters_defined():
            self._check_for_missing_args_in_env()
        if not self._all_parameters_defined():
            self._check_for_missing_args_in_config_file()
        self._final_arg_check()
    
    def _all_parameters_defined(self) -> bool:
        return (self.source_dir is not None and
            self.html_output_dir is not None and
            self.gemini_output_dir is not None and
            self.gopher_output_dir is not None and
            self.css_template_path is not None)
    
    def _check_for_missing_args_in_env(self) -> None:
        """Args passed in via command line take first precedence. Args set via env vars
        come second.

        The dockerfile sets env vars to "null" by default. "null" values are set to None
        so that we don't have to handle this special case downstream.
        """
        if self.source_dir is None:
            self.source_dir = os.getenv("OMNIHOST_SOURCE_DIR")
            if self.source_dir == "null":
                self.source_dir = None

        if self.html_output_dir is None:
            self.html_output_dir = os.getenv("OMNIHOST_HTML_OUTPUT_DIR")
            if self.html_output_dir == "null":
                self.html_output_dir = None

        if self.gemini_output_dir is None:
            self.gemini_output_dir = os.getenv("OMNIHOST_GEMINI_OUTPUT_DIR")
            if self.gemini_output_dir == "null":
                self.gemini_output_dir = None

        if self.gopher_output_dir is None:
            self.gopher_output_dir = os.getenv("OMNIHOST_GOPHER_OUTPUT_DIR")
            if self.gopher_output_dir == "null":
                self.gopher_output_dir = None

        if self.css_template_path is None:
            self.css_template_path = os.getenv("OMNIHOST_CSS_TEMPLATE_PATH")
            if self.css_template_path == "null":
                self.css_template_path = None
            
    def _get_config_file_path(self) -> str:
        appdata_path = os.getenv('APPDATA')
        if appdata_path:
            return os.path.join(appdata_path, "Local", "Omnihost", "config.txt")
        else:
            home_path = os.path.expanduser("~")
            return os.path.join(home_path, ".config", "omnihost", "config")
    
    def _check_for_missing_args_in_config_file(self) -> None:
        config_path = self._get_config_file_path()
        if os.path.exists(config_path):
            config_file_values = ConfigParser()
            config_file_values.read(config_path)
            # The Dockerfile sets the expected env vars to "null" by default.
            if self.source_dir is None:
                self.source_dir = config_file_values["DEFAULT"]["OMNIHOST_SOURCE_DIR"]
            if self.html_output_dir is None:
                self.html_output_dir = config_file_values["DEFAULT"]["OMNIHOST_HTML_OUTPUT_DIR"]
            if self.gemini_output_dir is None:
                self.gemini_output_dir = config_file_values["DEFAULT"]["OMNIHOST_GEMINI_OUTPUT_DIR"]
            if self.gopher_output_dir is None:
                self.gopher_output_dir = config_file_values["DEFAULT"]["OMNIHOST_GOPHER_OUTPUT_DIR"]
            if self.css_template_path is None:
                self.css_template_path = config_file_values["DEFAULT"]["OMNIHOST_CSS_TEMPLATE_PATH"]
        else:
            logging.info(f"No config file exists at {config_path}, cannot resolve missing parameters")
    
    def _final_arg_check(self) -> None:
        if self.source_dir is None:
            raise ConfigException("No input dir path provided")
        if self.source_dir == "":
            raise ConfigException("Empty input dir path provided")
        if not os.path.exists(self.source_dir):
            raise ConfigException(f"Gemtext input directory '{self.source_dir}' does not exist.")
        if not os.listdir(self.source_dir):
            raise ConfigException(f"Gemtext input directory '{self.source_dir}' is empty.")

        if not self.html_output_dir and not self.gemini_output_dir and not self.gopher_output_dir:
            raise ConfigException("No HTML, gemini, or gopher output directories provided")

        self._check_output_dir(self.html_output_dir, "HTML output")
        self._check_output_dir(self.gemini_output_dir, "Gemtext output")
        self._check_output_dir(self.gopher_output_dir, "Gopher output")

        if self.css_template_path is not None:
            if not os.path.exists(self.css_template_path):
                raise ConfigException(f"CSS template {self.css_template_path} does not exist.")

    def _check_output_dir(self, dir_path: Optional[str], dir_name: str) -> None:
        if dir_path is not None:
            if not os.path.exists(dir_path):
                raise ConfigException(f"{dir_name} directory '{dir_path}' does not exist.")
            if os.listdir(dir_path):
                raise ConfigException(f"{dir_name} directory '{dir_path}' is not empty.")


class ConfigException(Exception):
    """Represents an error with a config parameter."""
    pass
