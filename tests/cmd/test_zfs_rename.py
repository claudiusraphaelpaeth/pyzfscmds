import pytest
import datetime

import pyzfsutils.cmd
import pyzfsutils.utility

"""zfs commands tests"""

require_zpool = pytest.mark.require_zpool
require_test_dataset = pytest.mark.require_test_dataset


@require_zpool
@require_test_dataset
def test_zfs_rename_successful(zpool, test_dataset):
    dataset_name = "/".join([zpool, test_dataset,
                             f"pyzfsutils-{datetime.datetime.now().isoformat()}"])
    dataset_renamed = "/".join([zpool,
                               test_dataset,
                               f"pyzfsutils-{datetime.datetime.now().isoformat()}"])

    pyzfsutils.cmd.zfs_create_dataset(dataset_name)
    pyzfsutils.cmd.zfs_rename(dataset_name, dataset_renamed)

    assert pyzfsutils.utility.dataset_exists(dataset_renamed)
