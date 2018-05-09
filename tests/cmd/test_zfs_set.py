import pytest
import datetime

import pyzfsutils.cmd

"""zfs commands tests"""

require_zpool = pytest.mark.require_zpool
require_test_dataset = pytest.mark.require_test_dataset


@require_zpool
@require_test_dataset
@pytest.fixture(scope="function")
def set_dataset(zpool, test_dataset):
    dataset_name = "/".join([zpool,
                             test_dataset,
                             f"pyzfsutils-cloneds-{datetime.datetime.now().isoformat()}"])

    pyzfsutils.cmd.zfs_create_dataset(dataset_name,
                                      create_parent=True)

    return dataset_name


@pytest.mark.parametrize("prop", [
    ["mountpoint", "none"], ["canmount", "noauto"], ["compression", "on"]
])
@require_zpool
@require_test_dataset
def test_zfs_set_successful(set_dataset, prop):

    pyzfsutils.cmd.zfs_set(set_dataset, "=".join(prop))

    assert prop[1] in pyzfsutils.cmd.zfs_get(set_dataset,
                                             columns=["value"],
                                             properties=[prop[0]])