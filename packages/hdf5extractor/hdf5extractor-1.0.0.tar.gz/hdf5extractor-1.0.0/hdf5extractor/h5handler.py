from lxml import etree
import os
import h5py


def write_h5(
    input_h5: str, output_h5: str, h5_datasets: list, overwrite=False
):
    if len(h5_datasets) > 0:

        if not overwrite and os.path.exists(output_h5):
            print(f"The output file '{output_h5}'allready exists")
            return

        print(f"writing: {output_h5}: Found datasets: {h5_datasets}")

        with h5py.File(output_h5, "w") as f_dest:
            with h5py.File(input_h5, "r") as f_src:
                for dataset in h5_datasets:
                    f_dest.create_dataset(dataset, data=f_src[dataset])


def find_data_ref_in_xml(xml_content: bytes):
    tree = etree.ElementTree(etree.fromstring(xml_content))
    root = tree.getroot()
    return [
        x.text for x in root.xpath("//*[local-name() = 'PathInHdfFile']")
    ] + [
        x.text for x in root.xpath("//*[local-name() = 'PathInExternalFile']")
    ]
