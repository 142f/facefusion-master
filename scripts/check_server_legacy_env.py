import os
import shutil
import sys
import tempfile


def main() -> int:
    import cv2
    import insightface
    import numpy
    import onnx
    import onnxruntime
    import scipy

    print('Python:', sys.version)
    print('numpy:', numpy.__version__)
    print('cv2:', cv2.__version__)
    print('insightface:', insightface.__version__)
    print('onnx:', onnx.__version__)
    print('onnxruntime:', onnxruntime.__version__)
    print('scipy:', scipy.__version__)
    print('providers:', onnxruntime.get_available_providers())
    print('curl:', resolve_binary('curl', 'FACEFUSION_CURL_BIN'))
    print('ffmpeg:', resolve_binary('ffmpeg', 'FACEFUSION_FFMPEG_BIN'))

    if os.environ.get('FACEFUSION_REQUIRE_CUDA') == '1' and 'CUDAExecutionProvider' not in onnxruntime.get_available_providers():
        raise RuntimeError('CUDAExecutionProvider is not available')
    if os.environ.get('FACEFUSION_REQUIRE_CUDA') == '1':
        assert_cuda_session()

    return 0


def resolve_binary(binary_name : str, env_name : str) -> str:
    return os.environ.get(env_name) or shutil.which(binary_name) or ''


def assert_cuda_session() -> None:
    import numpy
    import onnx
    import onnxruntime
    from onnx import TensorProto, helper

    model_path = os.path.join(tempfile.gettempdir(), 'facefusion_cuda_smoke.onnx')
    input_info = helper.make_tensor_value_info('x', TensorProto.FLOAT, [1, 3])
    output_info = helper.make_tensor_value_info('y', TensorProto.FLOAT, [1, 3])
    node = helper.make_node('Identity', ['x'], ['y'])
    graph = helper.make_graph([node], 'facefusion_cuda_smoke', [input_info], [output_info])
    model = helper.make_model(graph)
    onnx.save(model, model_path)

    session = onnxruntime.InferenceSession(model_path, providers=['CUDAExecutionProvider'])
    if 'CUDAExecutionProvider' not in session.get_providers():
        raise RuntimeError('CUDAExecutionProvider was requested but session fell back to: ' + ', '.join(session.get_providers()))
    session.run(None, {
        'x': numpy.array([[1, 2, 3]], dtype=numpy.float32)
    })


if __name__ == '__main__':
    raise SystemExit(main())
