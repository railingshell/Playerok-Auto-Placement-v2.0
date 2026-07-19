import os
import sys

# Добавляем корень проекта в путь импорта, чтобы тесты видели пакеты бота
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
