import shutil
import json


def write_path(src, dest, sha256=None):
    if sha256:
        raise ValueError("Sha256 unhandled")

    shutil.move(src, dest)


def write_drv(path, contents):
    with open(path, "w") as f:
        f.write(json.dumps(contents, indent=2))
