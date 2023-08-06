import os
import shutil
import subprocess
import tarfile
import urllib.request
from pathlib import Path

PWD = Path(os.path.dirname(os.path.abspath(__file__)))
USER = "EBI-Metagenomics"
PROJECT = "deciphon-sched"
VERSION = "0.5.0"
CMAKE_OPTS = [
    "-DCMAKE_BUILD_TYPE=Release",
    "-DENABLE_ALL_WARNINGS=ON",
    "-DCMAKE_POSITION_INDEPENDENT_CODE=ON",
    "-DSCHED_BUILD_TESTS=OFF",
]


def rm(folder: Path, pattern: str):
    for filename in folder.glob(pattern):
        filename.unlink()


def get_cmake_bin():
    from cmake import CMAKE_BIN_DIR

    bins = [str(v) for v in Path(CMAKE_BIN_DIR).glob("cmake*")]
    return str(sorted(bins, key=lambda v: len(v))[0])


def cleanup_intree_artifacts():
    rm(PWD / "deciphon_sched", "cffi.c")
    rm(PWD / "deciphon_sched", "*.o")
    rm(PWD / "deciphon_sched", "*.so")
    rm(PWD / "deciphon_sched", "*.dylib")


def build_deps():
    ext_dir = PWD / ".ext_deps"
    shutil.rmtree(ext_dir, ignore_errors=True)

    prj_dir = ext_dir / f"{PROJECT}-{VERSION}"
    build_dir = prj_dir / "build"
    os.makedirs(build_dir, exist_ok=True)

    url = f"https://github.com/{USER}/{PROJECT}/archive/refs/tags/v{VERSION}.tar.gz"

    with urllib.request.urlopen(url) as rf:
        data = rf.read()

    tar_filename = f"{PROJECT}-{VERSION}.tar.gz"

    with open(ext_dir / tar_filename, "wb") as lf:
        lf.write(data)

    with tarfile.open(ext_dir / tar_filename) as tf:
        tf.extractall(ext_dir)

    cmake_bin = get_cmake_bin()
    subprocess.check_call(
        [cmake_bin, "-S", str(prj_dir), "-B", str(build_dir)] + CMAKE_OPTS
    )
    subprocess.check_call([cmake_bin, "--build", str(build_dir), "--config", "Release"])
    subprocess.check_call(
        [cmake_bin, "--install", str(build_dir), "--prefix", str(ext_dir)]
    )
    rm(ext_dir / "lib", "*.dylib")
    rm(ext_dir / "lib", "*.so*")
    rm(ext_dir / "lib64", "*.dylib")
    rm(ext_dir / "lib64", "*.so*")


if __name__ == "__main__":
    from cffi import FFI

    ffibuilder = FFI()

    cleanup_intree_artifacts()
    build_deps()
    library_dirs = [PWD / ".ext_deps" / "lib", PWD / ".ext_deps" / "lib64"]
    include_dirs = [PWD / ".ext_deps" / "include"]

    with open(PWD / "deciphon_sched" / "interface.h", "r") as f:
        interface_h = f.read()

    ffibuilder.cdef(interface_h)
    ffibuilder.set_source(
        "deciphon_sched.cffi",
        """
        #include "sched/sched.h"
        """,
        language="c",
        libraries=["sched"],
        library_dirs=[str(d) for d in library_dirs if d.exists()],
        include_dirs=[str(d) for d in include_dirs if d.exists()],
    )
    ffibuilder.compile(verbose=True)
