from pydantic import BaseModel
from ..plugins.file import FilePlugin
from ..load_config import load_config
import os
import pytest


class Schema(BaseModel):
  name: str


def test_env_plugin(fs):
  os.environ['PYTHON_ENV'] = 'test'
  default_config_file = '''
  name: ${file:/name.txt}
  '''
  fs.create_file('/name.txt', contents='Bob')
  fs.create_file('/config/default.yml', contents=default_config_file)
  config = load_config(Schema, config_dir='/config', plugins=[FilePlugin()])
  assert config.name == 'Bob'


def test_env_plugin_not_defined(fs):
  os.environ['PYTHON_ENV'] = 'test'
  default_config_file = '''
  name: ${file:/name.txt}
  '''
  fs.create_file('/config/default.yml', contents=default_config_file)
  with pytest.raises(Exception) as e:
    load_config(Schema, config_dir='/config', plugins=[FilePlugin()])
    assert str(e) == 'File /name.txt does not exist'