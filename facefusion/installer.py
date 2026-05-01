import os
import shutil
import signal
import subprocess
import sys
from argparse import ArgumentParser, HelpFormatter
from functools import partial
from types import FrameType

from facefusion import metadata
from facefusion.common_helper import is_linux, is_windows

LOCALES =\
{
	'install_dependency': 'install the {dependency} package',
	'force_reinstall': 'force reinstall of packages',
	'requirements_file_not_found': 'requirements file not found',
	'skip_conda': 'skip the conda environment check',
	'conda_not_activated': 'conda is not activated',
	'requirements_file': 'install packages from the requirements file',
	'skip_onnxruntime_rewrite': 'skip rewriting the onnxruntime package'
}
ONNXRUNTIME_SET =\
{
	'default': ('onnxruntime', '1.24.1')
}
if is_windows() or is_linux():
	ONNXRUNTIME_SET['cuda'] = ('onnxruntime-gpu', '1.24.3')
	ONNXRUNTIME_SET['openvino'] = ('onnxruntime-openvino', '1.24.1')
if is_windows():
	ONNXRUNTIME_SET['directml'] = ('onnxruntime-directml', '1.24.3')
	ONNXRUNTIME_SET['qnn'] = ('onnxruntime-qnn', '1.24.3')
if is_linux():
	ONNXRUNTIME_SET['migraphx'] = ('onnxruntime-migraphx', '1.24.2')
	ONNXRUNTIME_SET['rocm'] = ('onnxruntime-rocm', '1.22.2.post1')


def cli() -> None:
	signal.signal(signal.SIGINT, signal_exit)
	program = ArgumentParser(formatter_class = partial(HelpFormatter, max_help_position = 50))
	program.add_argument('--onnxruntime', help = LOCALES.get('install_dependency').format(dependency = 'onnxruntime'), choices = ONNXRUNTIME_SET.keys(), required = False, default = 'default')
	program.add_argument('--requirements-file', help = LOCALES.get('requirements_file'), default = 'requirements.txt')
	program.add_argument('--skip-onnxruntime-rewrite', help = LOCALES.get('skip_onnxruntime_rewrite'), action = 'store_true')
	program.add_argument('--force-reinstall', help = LOCALES.get('force_reinstall'), action = 'store_true')
	program.add_argument('--skip-conda', help = LOCALES.get('skip_conda'), action = 'store_true')
	program.add_argument('-v', '--version', version = metadata.get('name') + ' ' + metadata.get('version'), action = 'version')
	run(program)


def signal_exit(signum : int, frame : FrameType) -> None:
	sys.exit(0)


def run(program : ArgumentParser) -> None:
	args = program.parse_args()
	has_conda = 'CONDA_PREFIX' in os.environ

	if not args.skip_conda and not has_conda:
		sys.stdout.write(LOCALES.get('conda_not_activated') + os.linesep)
		sys.exit(1)

	commands = [ shutil.which('pip'), 'install' ]

	if args.force_reinstall:
		commands.append('--force-reinstall')

	if not os.path.isfile(args.requirements_file):
		sys.stdout.write(LOCALES.get('requirements_file_not_found') + ': ' + args.requirements_file + os.linesep)
		sys.exit(1)

	with open(args.requirements_file) as file:
		for line in file.readlines():
			__line__ = line.strip()
			if __line__ and not __line__.startswith('#') and (not __line__.startswith('onnxruntime') or args.skip_onnxruntime_rewrite):
				commands.append(__line__)

	if not args.skip_onnxruntime_rewrite:
		onnxruntime_name, onnxruntime_version = ONNXRUNTIME_SET.get(args.onnxruntime)
		commands.append(onnxruntime_name + '==' + onnxruntime_version)

		subprocess.call([ shutil.which('pip'), 'uninstall', 'onnxruntime', onnxruntime_name, '-y', '-q' ])

	subprocess.call(commands)
