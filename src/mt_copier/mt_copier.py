import json
import time
import shutil

SIGNAL_PATH = '../../sample_data/sample_signal.json'
COPIED_PATH = '../../sample_data/copied_signal.json'


def copy_signal():
    """Simulate copying a signal from MT4/MT5."""
    shutil.copyfile(SIGNAL_PATH, COPIED_PATH)
    print(f"Signal copied to {COPIED_PATH}")

if __name__ == "__main__":
    while True:
        copy_signal()
        time.sleep(2)
