import sys
from pathlib import Path

# backendディレクトリのパスを取得
backend_dir = Path(__file__).parent

# PYTHONPATHにbackendディレクトリを追加
sys.path.insert(0, str(backend_dir))
