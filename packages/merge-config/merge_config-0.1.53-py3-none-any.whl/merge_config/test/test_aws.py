# from pydantic import BaseModel
# from load_config import load_config
# import os
# from moto import mock_ssm, mock_secretsmanager
# from plugins.aws import AWSPlugin, SSMPlugin

# class Schema(BaseModel):
#   name: str

# @mock_ssm
# def test_ssm_plugin(fs):
#   os.environ['PYTHON_ENV'] = 'test'
#   default_config_file = '''
#   name: ${ssm:NAME}
#   '''
#   fs.create_file('/config/default.yml', contents=default_config_file)
#   config = load_config(Schema, config_dir='/config', plugins=[SSMPlugin()])
#   assert config.name == 'Bob'

# @mock_secretsmanager
# def test_aws_plugin(fs):
#   os.environ['PYTHON_ENV'] = 'test'
#   default_config_file = '''
#   name: ${aws:bastion/host}
#   '''
#   fs.create_file('/config/default.yml', contents=default_config_file)

#   config = load_config(Schema, config_dir='/config', plugins=[AWSPlugin()])
#   assert config.name == 'bastion-lb-e9369ce9c6fe48aa.elb.eu-west-2.amazonaws.com'


def test_nothing():
  assert True == True