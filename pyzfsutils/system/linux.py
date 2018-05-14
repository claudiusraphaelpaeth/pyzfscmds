import re


def mountpoint_dataset(mountpoint: str):
    """
    Check if dataset is a 'zfs' mount.
    return dataset, or None if not found
    """

    with open("/proc/mounts") as f:
        mount = next((ds for ds in f.read().splitlines() if f"{mountpoint} zfs" in ds), None)

    return None if mount is None else mount.split(" ")[0]


def dataset_mountpoint(dataset: str):
    """
    Get dataset mountpoint, or None if not found
    """

    target = re.compile(r'\b' + dataset + r'\b')

    with open("/proc/mounts") as f:
        mount = next(
            (ds for ds in f.read().splitlines() if all(
                x in ds for x in [dataset, "zfs"]) and target.search(ds)), None)

    return None if mount is None else mount.split(" ")[1]


def zfs_module_loaded():
    with open("/proc/modules") as f:
        if "zfs" not in f.read():
            return False

    return True
