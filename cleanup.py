from datetime import datetime
from pathlib import Path

import dotenv
from dotenv import load_dotenv
import shutil



TERMINATIONS = {
    'images': ('.jpg', '.jpeg', '.png', '.gif'),
    'docs': ('.pdf', '.docx'),
    'videos': ('.mp4', '.avi', '.mov'),
}

env_path = Path(__file__).parent / '.env'

if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else: raise FileNotFoundError(f'Environment file {env_path} not found')


desktop = Path(dotenv.get_key(env_path, 'SOURCE_DIR')).expanduser()
cleanup_path = Path(dotenv.get_key(env_path, 'CLEANUP_DIR')).expanduser()

### Creates Paths for target directories
cleanup_directories = [cleanup_path / termination for termination in TERMINATIONS.keys()]

#### Ensures Target directories are created
for directory in cleanup_directories:
    directory.mkdir(parents=True, exist_ok=True)

### Moves files to clean-up location, filtered by type
logs = []
for item in desktop.iterdir():
    moved = False
    if item.is_file():
        for key in TERMINATIONS.keys():
            for termination in TERMINATIONS.get(key):
                if item.suffix.lower() == termination.lower():
                    shutil.move(str(item), str(cleanup_path / key / item.name))
                    moved = True
                    logs.append(
                        f"{datetime.now()}: {item.name} moved to {cleanup_path / key}"
                    )
                    break

            if moved:
                break

path_to_logs = Path(__file__).parent / 'logs.log'
with open(path_to_logs, 'a') as f:
    for log in logs:
        f.write(log + '\n')