import os
import shutil
import sys


def main() -> int:
	import cv2
	import numpy
	import onnx
	import onnxruntime
	import scipy

	print('Python:', sys.version)
	print('numpy:', numpy.__version__)
	print('cv2:', cv2.__version__)
	print('onnx:', onnx.__version__)
	print('onnxruntime:', onnxruntime.__version__)
	print('scipy:', scipy.__version__)
	print('providers:', onnxruntime.get_available_providers())
	print('curl:', resolve_binary('curl', 'FACEFUSION_CURL_BIN'))
	print('ffmpeg:', resolve_binary('ffmpeg', 'FACEFUSION_FFMPEG_BIN'))

	if os.environ.get('FACEFUSION_REQUIRE_CUDA') == '1' and 'CUDAExecutionProvider' not in onnxruntime.get_available_providers():
		raise RuntimeError('CUDAExecutionProvider is not available')

	return 0


def resolve_binary(binary_name : str, env_name : str) -> str:
	return os.environ.get(env_name) or shutil.which(binary_name) or ''


if __name__ == '__main__':
	raise SystemExit(main())
