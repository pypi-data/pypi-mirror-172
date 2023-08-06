import argparse
import os
import re
import zipfile
from hdf5extractor.h5handler import write_h5, find_data_ref_in_xml


UUID_REGEX = r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}\
-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"
FILE_NAME_REGEX = r"^[\w]+_" + UUID_REGEX + r"\.xml$"


def process_files(
    file_path: str, input_h5: str, output_folder: str, overwrite=False
):
    to_process_files = []
    if file_path.endswith(".xml"):
        file_name = file_path
        if "/" in file_name:
            file_name = file_name[file_name.rindex("/") + 1:]
        if "\\" in file_name:
            file_name = file_name[file_name.rindex("\\") + 1:]

        xml_content = open(file_path, "rb").read()
        to_process_files.append((xml_content, file_name))
    elif file_path.endswith(".epc"):
        with zipfile.ZipFile(file_path) as epc_as_zip:
            for f_name in epc_as_zip.namelist():
                if not f_name.startswith("_rels/") and re.match(
                    FILE_NAME_REGEX, f_name
                ):
                    # print(f_name)
                    with epc_as_zip.open(f_name) as myfile:
                        to_process_files.append((myfile.read(), f_name))

    for f_content, f_name in to_process_files:
        write_h5(
            input_h5,
            output_folder + "/" + f_name[: f_name.rindex(".")] + ".h5",
            find_data_ref_in_xml(f_content),
            overwrite,
        )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        "-i",
        required=True,
        type=str,
        help="[Required] Input file (xml of epc) from which the\
        referenced data path are taken",
    )
    parser.add_argument(
        "--h5",
        required=True,
        type=str,
        help="[Required] Input h5 file or folder that contains h5 files",
    )
    parser.add_argument(
        "--output",
        "-o",
        default="extracted",
        type=str,
        help="h5 output folder",
    )
    parser.add_argument(
        "--force",
        "-f",
        action="store_true",
        help="force the overwrite the output files if allready exists",
    )
    args = parser.parse_args()

    try:
        os.makedirs(args.output)
    except OSError:
        pass

    process_files(
        file_path=args.input,
        input_h5=args.h5,
        output_folder=args.output,
        overwrite=args.force,
    )


if __name__ == "__main__":
    main()
