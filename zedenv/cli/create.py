"""List boot environments cli"""

import datetime

import click
import zedenv.lib.zfs.commands
import zedenv.lib.zfs.linux

@click.command(name="create",
               help="Create a boot environment.")
@click.option('--verbose', '-v',
              is_flag=True,
              help="Print verbose output.")
@click.option('--existing', '-e',
              is_flag=True,
              help="Use existing boot environment as source.")
@click.argument('boot_environment')
def cli(boot_environment, verbose, existing):

    if verbose:
        click.echo("Listing Boot Environments verbosely.")

    zfs = zedenv.lib.zfs.commands.ZFS()

    root_dataset = zedenv.lib.zfs.linux.mount_dataset("/")

    zfs.get(root_dataset,
            columns=["name", "property", "value"],
            source=["local", "received"],
            properties=["all"])

    click.echo("Cloning...")
    if existing:
        source_snap = existing
    else:
        snap_suffix = "zedenv-{}".format(datetime.datetime.now().isoformat())
        try:
            zfs.snapshot(root_dataset, snap_suffix)
        except RuntimeError as e:
            click.echo(f"Failed to create snapshot: '{root_dataset}@{snap_suffix}'")

        source_snap = f"{root_dataset}@{snap_suffix}"

        click.echo(f"Using {source_snap} as source")

    # Remove the final part of the data set after the last / and add new name
    boot_environment_dataset = f"{root_dataset.rsplit('/', 1)[0]}/{boot_environment}"

    click.echo(f"Creating BE: {boot_environment_dataset}")

    try:
        zfs.clone(source_snap, boot_environment_dataset)
    except RuntimeError as e:
        click.echo(f"Failed to create {boot_environment} from {source_snap}")
