# -*- coding: utf-8 -*-
import argparse

from tools.lambda_python_pkg import bundle_files, MIN_EPOCH


def main(args):
    bundle_files(**args.__dict__)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="create a zip file", fromfile_prefix_chars="@"
    )

    parser.add_argument(
        "-o", "--output_file", type=str, help="The output zip file path."
    )
    parser.add_argument(
        "-e", "--entrypoint", type=str, help="The entrypoint for the function",
    )
    parser.add_argument(
        "-t",
        "--timestamp",
        type=int,
        default=MIN_EPOCH,
        help=(
            "The unix time to use for files added into the zip. Values prior "
            "to 1980-01-01 00:00:00 UTC are ignored."
        ),
    )
    parser.add_argument(
        "-s",
        "--strip_prefix",
        type=str,
        help="A directory prefix to strip from the extracted files",
    )
    parser.add_argument(
        "-P",
        "--path_vars",
        type=str,
        help="Comma delimited list of paths to add to system PATH",
    )
    parser.add_argument(
        "files", type=str, nargs="*", help="Files to be added to the zip",
    )

    args = parser.parse_args()
    main(args)
