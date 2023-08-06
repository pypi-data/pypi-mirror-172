__version__ = '0.0.10'

import os
from datetime import datetime

from flask import Flask, render_template, request
from flask_cors import CORS
from werkzeug.security import safe_join

app = Flask(__name__, static_url_path='/')
CORS(app, supports_credentials=True)


def index(e):
    path = safe_join(app.static_folder, request.path.strip('/'))
    if not os.path.exists(path):
        return render_template('404.html'), 400
    body = []
    f: os.DirEntry
    for f in os.scandir(path):
        if f.name.startswith('.'):
            continue
        f_stat = f.stat()
        body.append({
            'path': f.name + ('/' if f.is_dir() else ''),
            'time': datetime.strftime(datetime.fromtimestamp(f_stat.st_mtime), '%Y-%m-%d %H:%M:%S'),
            'size': f_stat.st_size if f.is_file() else '-'
        })
    body.sort(key=lambda x: x['path'])
    body.sort(key=lambda x: not x['path'].endswith('/'))
    return render_template('index.html', title=request.path, body=body)


app.register_error_handler(404, index)


def start_server(host, port, dir_):
    app._static_folder = os.path.abspath(dir_)
    app.run(host=host, port=port)


def main():
    import argparse
    parser = argparse.ArgumentParser(
        description='simple http server for share files.',
        epilog=f'pyhttp({__version__}) by foyou(https://github.com/foyoux)'
    )
    parser.add_argument('dir', nargs='?', default='.', help='HTTP Server 共享目录')
    parser.add_argument('--host', dest='host', default='0.0.0.0', help='HTTP Server 监听地址')
    parser.add_argument('--port', dest='port', default='5512', help='HTTP Server 监听端口')
    parser.add_argument('--version', dest='version', help='打印版本信息', action='store_true')
    args = parser.parse_args()

    if args.version:
        print('pyhttp version', __version__)
        return

    start_server(args.host, args.port, args.dir)


if __name__ == '__main__':
    start_server('0.0.0.0', '1234', '/')
