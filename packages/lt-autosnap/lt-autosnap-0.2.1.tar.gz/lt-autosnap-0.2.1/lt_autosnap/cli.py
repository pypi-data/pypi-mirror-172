"""Command line interface and data structure"""
import logging
import textwrap
from argparse import ArgumentParser, RawTextHelpFormatter
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Union

from .autosnap import run_cmd
from .exit import errexit
from .logger import set_daemon_formatter, set_loglevel
from .version import __version__

logger = logging.getLogger(__name__)


@dataclass
class CLIArgs:
    """The command-line arguments for ltautosnap"""

    command: str
    vol_id: Union[str, int]
    snap_set_id: Optional[int]
    autoclean: bool
    config_path: Path
    log_level: int
    daemon: bool

    def __init__(self):
        """Parse args from the CLI into the dataclass fields"""
        args = self.gen_parser().parse_args()
        command: str = args.command
        volume: str = args.volume
        if command not in (
            "mount",
            "umount",
            "snap",
            "clean",
            "autosnap",
            "check",
            "list",
            "remove",
            "genconf",
        ):
            errexit("Invalid command")
        if command not in ["genconf"] and args.volume != "all" and not args.volume.isdecimal():
            errexit("Volume must be 'all' or a volume number.")
        self.command = command
        self.vol_id = int(volume) if volume.isdecimal() else volume
        self.snap_set_id = args.snap_set
        self.autoclean = args.autoclean
        self.config_path = Path(args.config)
        log_levels = {
            0: logging.WARNING,
            1: logging.INFO,
            2: logging.DEBUG,
        }
        self.log_level = log_levels.get(args.verbosity, logging.DEBUG)
        self.daemon = args.daemon

    def gen_parser(self):
        """Generate the ArgumentParser for the CLI"""
        parser = ArgumentParser(
            description="Automated LVM thin volume snapshot management",
            formatter_class=lambda prog: RawTextHelpFormatter(prog, width=80),
            epilog=textwrap.dedent("""\
                Detailed Command description:

                Note, in most of the below commands, "all" (without quotes) can be used to
                repeat the operation on all volumes, and the snap set number may be omitted to
                operate on all snap sets.

                ltautosnap mount <vol_n>|all [<snap_set_n>]
                    Mounts snapshots of the specified volume and snap set(s) to new directories
                    under the 'snap_mount_base' location configured for the volume. The mount
                    point will have a name like '@GMT-<snapshot datetime>'. If NOMOUNT is
                    specified for 'snap_mount_base', an error will be raised.

                ltautosnap umount <vol_n>|all [<snap_set_n>]
                    Unmount any mounted snapshots for the specified volume and snap set(s).

                ltautosnap snap <vol_n>|all [<snap_set_n]
                    Create a snapshot for the specified volume and snap set(s). This will always
                    create a snapshot, regardless of the snap set definition.

                ltautosnap clean <vol_n>|all [<snap_set_n]
                    For the specified volume and snap set[s], determine if there are more
                    snapshots than defined in the snap set's 'count' parameter. If so, unmount
                    and delete the oldest snapshot[s] as necessary to meet the 'count'. Also run
                    the `fstrim` command on the filesystem of the volume so `lvs` returns the
                    correct total used capacity of the pool.

                ltautosnap autosnap <vol_n>|all [<snap_set_n] [--autoclean]
                    For the specified volume and snap set[s], create a snapshot only if the time
                    since the most recent snapshot of the snap set is greater than the period of
                    the snap set. Perform the 'mount' command for the volume and snap set[s]. If
                    --autoclean is specified, run the 'clean' command afterwards.

                ltautosnap check <vol_n>|all
                    Check that the data usage of the pool for the specified volume has not
                    exceeded its 'warning_pct' configuration parameter.

                ltautosnap list <vol_n>|all [<snap_set_n]
                    List all snapshots of the given volume and snap set[s].

                ltautosnap remove <vol_n>|all [<snap_set_n]
                    Removes all snapshots in the specified snap set[s] of the volume.
                    `ltautosnap umount` must be run first.

                ltautosnap genconf
                    Print an example configuration file to stdout.

                For more help, see README at https://gitlab.com/randallpittman/lt-autosnap
                """),
        )
        parser.add_argument(
            "command",
            help=textwrap.dedent(
                """\
                Command to execute. Valid commands are mount, umount, snap,
                clean, autosnap, check, list, remove, and genconf. See below
                for more details.
                """
            ),
        )
        parser.add_argument(
            "--autoclean",
            action="store_true",
            help="If command is autosnap, run clean after creating the new\nsnapshots.",
        )
        parser.add_argument(
            "--config",
            default="/etc/ltautosnap.conf",
            help="Alternate configuration file. Default is /etc/ltautosnap.conf",
        )
        parser.add_argument(
            "-v",
            dest="verbosity",
            action="count",
            default=0,
            help="Increment the logging verbosity level.\nNone for WARNING, -v for INFO, -vv for DEBUG",
        )
        parser.add_argument(
            "-d", "--daemon", action="store_true", help="Make logging appropriate for file output."
        )
        parser.add_argument("-V", "--version", action="version", version=__version__)
        parser.add_argument(
            "volume", help='Number of the volume, or "all" for all volumes', default="", nargs="?"
        )
        parser.add_argument(
            "snap_set",
            nargs="?",
            type=int,
            default=None,
            help="Number of the snaphot-set. Optional for all commands except\nsnap, autosnap, and clean.",
        )
        return parser


def cli():
    """Main entry point for the ltautosnap application. Process cli args and run the desired command."""
    try:
        args = CLIArgs()
        set_loglevel(args.log_level)
        if args.daemon:
            set_daemon_formatter()
        run_cmd(args)
    except Exception as ex:
        errexit("Exception", 255, ex)
