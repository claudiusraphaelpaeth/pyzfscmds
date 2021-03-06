import datetime
import os

import pytest

import pyzfscmds.cmd

module_env = os.path.basename(__file__).upper().rsplit('.', 1)[0]
if module_env in os.environ:
    pytestmark = pytest.mark.skipif(
        "false" in os.environ[module_env],
        reason=f"Environment variable {module_env} specified test should be skipped.")

"""zfs commands tests"""

require_zpool = pytest.mark.require_zpool
require_test_dataset = pytest.mark.require_test_dataset


# @pytest.mark.parametrize("", [None, [""]])
@require_zpool
@require_test_dataset
def test_zfs_rollback_successful(zpool, test_dataset):
    dataset_name = "/".join([zpool,
                             test_dataset,
                             f"pyzfscmds-{datetime.datetime.now().isoformat()}"])
    snapname = f"pyzfscmds-{datetime.datetime.now().isoformat()}"

    pyzfscmds.cmd.zfs_create_dataset(dataset_name)
    pyzfscmds.cmd.zfs_snapshot(dataset_name, snapname)
    pyzfscmds.cmd.zfs_rollback("@".join([dataset_name, snapname]))
