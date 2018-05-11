"""ZFS library"""

import pyzfsutils.cmd

"""
ZFS helper functions
"""


def is_snapshot(snapname: str) -> bool:
    if "@" in snapname:
        return dataset_exists(snapname, zfs_type="snapshot")

    return False


"""
Check if clone, raise if not valid dataset
"""


def is_clone(dataset: str) -> bool:
    try:
        origin = pyzfsutils.cmd.zfs_get(dataset,
                                        properties=["origin"],
                                        columns=["value"])
        print(origin)
    except RuntimeError:
        raise

    if origin.split()[0] == "-":
        return False

    return True


def dataset_parent(dataset: str) -> str:
    # TODO: Should I check ds valid?
    return dataset.rsplit('/', 1)[0]


def dataset_child_name(dataset: str) -> str:
    return dataset.rsplit('/', 1)[-1]


def snapshot_parent_dataset(dataset: str) -> str:
    return dataset.rsplit('@', 1)[-2]


def dataset_exists(target: str, zfs_type: str = "filesystem") -> bool:

    try:
        pyzfsutils.cmd.zfs_list(target, zfs_types=[zfs_type])
    except RuntimeError:
        return False

    return True
