import subprocess
from pathlib import Path

import jdk
import jpype.imports
import logging


def load_config(config_path: str) -> 'Properties':
  from java.io import FileInputStream
  from java.util import Properties

  config_path = Path(config_path).expanduser()
  if not config_path.exists():
    raise IOError(f'{config_path} not found')
  config = Properties()
  with FileInputStream(config_path) as input_stream:
    config.load(input_stream)
  return config


def _install_jre() -> str:
  logging.info('Installing JRE')
  try:
    # https://github.com/jpype-project/jpype/issues/1097: support for java 17+
    jre_install_dir = jdk.install('13', jre=True)
  except PermissionError as e:
    jre_install_dir = Path(e.filename.split('/Contents/')[0])
  jvm_path = Path(jre_install_dir) / 'Contents/Home/lib/libjli.dylib'
  assert jvm_path.exists()
  return str(jvm_path)


class _Maven:
  def __init__(self):
    self._project_dir = Path(__file__).parent
    self._mvn_path = self._project_dir / 'mvnw'
    assert self._mvn_path.exists()

  def install_dependencies(self):
    logging.info('Installing Maven dependencies')
    self._run_command('install')

  def get_class_path(self):
    return self._run_command('-q', 'exec:exec', '-Dexec.executable=echo', '-Dexec.args="%classpath"')

  def _run_command(self, *commands: str):
    process = subprocess.run([str(self._mvn_path), *commands, '-f', str(self._project_dir)], capture_output=True)
    if process.returncode != 0:
      raise EnvironmentError(f'Return code {process.returncode} {process.stderr}')
    logging.debug(process)
    return process.stdout.decode()


if not jpype.isJVMStarted():
  jvm_path = _install_jre()
  maven = _Maven()
  maven.install_dependencies()
  class_path = maven.get_class_path()
  logging.info('Starting JVM')
  jpype.startJVM(jvmpath=jvm_path, classpath=[class_path])

jpype.imports.registerDomain("jio", alias="io")
