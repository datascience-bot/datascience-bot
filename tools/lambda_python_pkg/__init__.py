# -*- coding: utf-8 -*-
from datetime import datetime, timezone
import os
import re
from typing import List, Tuple
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo


MIN_EPOCH = datetime(1980, 1, 1, tzinfo=timezone.utc).timestamp()


def gen_path_loader(path_vars: List[str], strip_prefix):
    """Generate boilerplate Python to add runfiles to system PATH

    AWS Lambda won't recognize these paths by default, so we have to add them
    to the PATH ourselves

    Args:
        path_vars (List[str]): filepaths to add to system PATH
        strip_prefix ([type]): [description]

    Returns:
        [type]: [description]
    """
    bazel_generated = re.compile(r"bazel-ou.*bin")
    all_path_vars = []
    for path_var in path_vars.split(","):
        if bazel_generated.findall(path_var) and strip_prefix in path_var:
            all_path_vars += bazel_generated.findall(path_var)
        else:
            all_path_vars.append(path_var)

    with open("tools/lambda_python_pkg/data/preamble_template.py", "r") as ifile:
        preamble = ifile.read().format(repr(set(all_path_vars)))

    return preamble


def convert_epoch_to_datetime_parts(timestamp: int) -> Tuple[int]:
    dt = datetime.utcfromtimestamp(timestamp)

    return dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second


def define_zip_info(path: str, timestamp: int = MIN_EPOCH, strip_prefix: str = None):
    if strip_prefix is not None:
        path = os.path.relpath(path, strip_prefix)

    if timestamp < MIN_EPOCH:  # prevent errors with zip dated before 1980
        dt = MIN_EPOCH
    else:
        dt = convert_epoch_to_datetime_parts(timestamp)

    info = ZipInfo(filename=path, date_time=dt)
    info.external_attr = 0o777 << 16  # give full access to included file
    info.compress_type = ZIP_DEFLATED

    return info


def bundle_files(
    files: List[str],
    output_file: str,
    entrypoint: str,
    strip_prefix: str,
    path_vars: str,
    timestamp: str = MIN_EPOCH,
):
    f"""Bundle files into a zip file.

    Args:
        files (List[str]): Files to bundle into a zip file.
        output_file (str): Output zip filepath.
        entrypoint (str): The entrypoint for the zip file.
        strip_prefix (str): The root of the executable.
        path_vars (str): Comma delimited list of extra paths.
        timestamp (str): The unix time to use for files added into the zip.
            Values prior to Jan 1, 1980 are ignored. Defaults to {MIN_EPOCH}.
    """
    # TODO: Assert entrypoint in listed files
    preamble = gen_path_loader(path_vars, strip_prefix)

    with ZipFile(output_file, "w") as ofile:
        for f in files:
            with open(f, "rb") as ifile:
                script = ifile.read()
            if f == entrypoint:
                script = preamble.encode("utf-8") + b"\n" + script
                info = define_zip_info(f, timestamp, strip_prefix)
            else:
                info = define_zip_info(f, timestamp)

            ofile.writestr(info, script)
