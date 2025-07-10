import os

# Root directory of your project
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))

for dirpath, dirnames, filenames in os.walk(ROOT):
    # Remove __pycache__ directories
    if '__pycache__' in dirnames:
        pycache_path = os.path.join(dirpath, '__pycache__')
        print(f'Removing {pycache_path}')
        try:
            import shutil
            shutil.rmtree(pycache_path)
        except Exception as e:
            print(f'Error removing {pycache_path}: {e}')
    # Remove .pyc files
    for filename in filenames:
        if filename.endswith('.pyc'):
            pyc_path = os.path.join(dirpath, filename)
            print(f'Removing {pyc_path}')
            try:
                os.remove(pyc_path)
            except Exception as e:
                print(f'Error removing {pyc_path}: {e}')

print('Cleanup complete.')
