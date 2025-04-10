from flask import Flask, request, jsonify, send_file
# import importlib.util
# import os
import sys
sys.path.insert(0, '/home/ubuntu/code/music_source_separation')

from bytesep.__main__ import main

app = Flask(__name__)
#
# def load_main_function():
#     """
#     动态加载 __main__.py 并获取 main() 方法
#     """
#     MAIN_MODULE_PATH = os.path.join(os.path.dirname(__file__), "__main__.py")
#
#     spec = importlib.util.spec_from_file_location("__main__", MAIN_MODULE_PATH)
#     module = importlib.util.module_from_spec(spec)
#     spec.loader.exec_module(module)
#
#     return module.main  # 确保 __main__.py 里有 main(mode)
@app.route('/')
def index():
    return 'Hello from Flask on AWS Lambda!'

@app.route("/separate_from_audio_file", methods=["POST"])
def separate_from_audio_file():
    """
    处理 POST 请求，调用 main(mode) 并返回结果
    """
    # print(request.files)
    # scale_volume, source_type, audio_path, output_path, cpu
    mode = request.form.get("mode", None)
    scale_volume = request.form.get("scale_volume", False)
    source_type = request.form.get("source_type", None)
    audio_path = request.files["audio_path"]
    output_path = request.form.get("output_path", None)
    cpu = request.form.get("cpu", False)

    audio_buffer_res = main(mode, scale_volume, source_type, audio_path, output_path, cpu)  # 传入参数 mode
    return send_file(audio_buffer_res, mimetype='audio/mpeg', as_attachment=True, download_name='audiofile.mp3')
    # return jsonify({"result": result})  # 返回 JSON 结果

if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", port=5000, debug=True)
    except Exception as e:
        print(f"发生异常：{e}")