# lt-autosnap <!-- omit in toc -->

- [1. DISCLAIMER](#1-disclaimer)
- [2. Changelog](#2-changelog)
- [3. Introduction](#3-introduction)
- [4. Requirements](#4-requirements)
  - [4.1 Python Dependencies](#41-python-dependencies)
- [5. Installation](#5-installation)
  - [5.1 Isolated install (RECOMMENDED)](#51-isolated-install-recommended)
  - [5.2 Root user install](#52-root-user-install)
  - [5.3 System pip](#53-system-pip)
- [6. Configuration](#6-configuration)
  - [6.1 Parameters](#61-parameters)
    - [6.1.2 Volume](#612-volume)
    - [6.1.3 Snap set](#613-snap-set)
- [6.2 `/etc/ltautosnap.conf`](#62-etcltautosnapconf)
- [7. Usage](#7-usage)

## 1. DISCLAIMER

Due to the following factors:

- This software is intended to be run with root privileges
- This software manages logical volumes on your machine, including creationg and deletion of snapshots
- There may be bugs in this software

...be advised that this software has the ability to at the least cause you **DATA LOSS** and at the worst
**SEVERELY DAMAGE OR IMPAIR** your operating system. **THIS IS NOT BACKUP SOFTWARE**.

See [LICENSE.txt](LICENSE.txt) for further disclaimers.

## 2. Changelog

[See CHANGELOG.md](CHANGELOG.md)

## 3. Introduction

The purpose of this tool is to automate management of LVM thin pool snapshots. It is intended to be used with
cron or systemd timers for scheduling.

[There is a guide on the Samba
website](https://wiki.samba.org/index.php/Rotating_LVM_snapshots_for_shadow_copy) for setting up rotating LVM
snapshots for use with Samba's implementation of Volume Shadow Copy. This script is based on the Bash script
in that guide. It can mount snapshots to a specified path with dirnames compatible with Volume Shadow Copy,
e.g. `@GMT-2022.04.28-22.35.17`. For more on setting up Samba for shadow copies, see
[https://www.samba.org/samba/docs/current/man-html/vfs_shadow_copy2.8.html](https://www.samba.org/samba/docs/current/man-html/vfs_shadow_copy2.8.html)

## 4. Requirements

This tool requires Python 3.6 or later. For recent Linux distributions the system Python interpreter should
suffice. `pip` or `pip3` is required for installation, so you may need to install `python3-pip` or similar
package.

### 4.1 Python Dependencies

Since I expect this to be a system package, I tried to minimize the dependencies it would install.

- If you are using Python 3.6, pip will install the `dataclasses` backport for 3.6.
- pip will install `single-version` for package version management.

## 5. Installation

### 5.1 Isolated install (RECOMMENDED)

This installs lt-autosnap to an isolated environment. You have to add the bin path to your `PATH` or call
the executable directly.

Requires `python3-venv` to be installed on Ubuntu-like OSes.

The below sets up a virtual environment in `/opt/venv/lt-autosnap`. Adjust as you prefer.
```bash
# ## All as root
mkdir -p /opt/venv
# Create virtual environment. Substitute virtualenv if you prefer.
python3 -m venv /opt/venv/lt-autosnap
# install lt-autosnap
/opt/venv/lt-autosnap/bin/pip install lt-autosnap
# To add to PATH for bash
echo 'export PATH="$PATH:/opt/venv/lt-autosnap/bin"' > /etc/profile.d/lt-autosnap.sh
# --AND/OR-- To add to PATH for csh
echo 'setenv PATH "$PATH:/opt/venv/lt-autosnap/bin"' > /etc/profile.d/lt-autosnap.sh
# --OR-- just use the full path when you need to run lt-autosnap
/opt/venv/lt-autosnap/bin/ltautosnap
```

### 5.2 Root user install

This install to `root`'s `~/.local` dir, which may or may be in `PATH` (see root's `~/.bashrc` file.)

```bash
sudo pip install --user lt-autosnap
```

### 5.3 System pip

It is generally not recommended to install stuff with `pip` as root, however this package has minimal
dependencies (just `single-version` and `python3-dataclasses` for Python 3.6). This has the benefit of the
`ltautosnap` command being in your PATH without any extra work. Just run:

```bash
# as root
# generally installs to /usr/local. Specify --prefix to install somewhere else.
pip3 install lt-autosnap
```

## 6. Configuration

### 6.1 Parameters

Each configuration file typically contains one or more **volume** and **snap set** definitions. These are
defined as follows:

#### 6.1.2 Volume

An LVM thin volume that `ltautosnap` will act upon. Configurable options include:

- Where to mount snapshots of the volume
- Options to pass the mount command when mounting snapshots
- Which snapset definitions to use
- A maximum percent-full value after which the `ltautosnap check` command will start emitting warnings that
  the pool is running out of space.

#### 6.1.3 Snap set

A scheme for making snapshots. Configuration options include:

- The period of time between snapshots (`ltautosnap autosnap` uses this to determine whether to create new
  snapshots)
- The maximum number of snapshots to keep (oldest are deleted with `ltautosnap clean`)

Each volume may have multiple snapsets and nultiple volumes may use the same snapset definition.

## 6.2 `/etc/ltautosnap.conf`

1. Create a config file with `ltautosnap genconf > ltautosnap.conf`. Internal comments provide guidance on
   how to configure volumes and snap sets.
2. Modify the config file with the details about your volumes and desired snap sets and, as root, copy it to
   `/etc/ltautosnap.conf`.

## 7. Usage

Most commands require root privileges, even `list`, since it runs `lvs` which usually requires root.

- Output of `ltautosnap --help`:
  ```text
  usage: ltautosnap [-h] [--autoclean] [--config CONFIG] [-v] [-d] [-V]
                    command [volume] [snap_set]

  Automated LVM thin volume snapshot management

  positional arguments:
    command          Command to execute. Valid commands are mount, umount, snap,
                     clean, autosnap, check, list, remove, and genconf. See below
                     for more details.
    volume           Number of the volume, or "all" for all volumes
    snap_set         Number of the snaphot-set. Optional for all commands except
                     snap, autosnap, and clean.

  optional arguments:
    -h, --help       show this help message and exit
    --autoclean      If command is autosnap, run clean after creating the new
                     snapshots.
    --config CONFIG  Alternate configuration file. Default is /etc/ltautosnap.conf
    -v               Increment the logging verbosity level.
                     None for WARNING, -v for INFO, -vv for DEBUG
    -d, --daemon     Make logging appropriate for file output.
    -V, --version    show program's version number and exit

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
  ```
- As root, create a crontab file at `/etc/cron.d/ltautosnap` to generate snaps.

   Examples:

   ```bash
   # If desired, set an email address to send error messages
   #   Cron will usually email stdout and stderr if you have mail set up with
   #   Postfix or similar MTA.
   MAILTO=example@example.org
   LTAUTOSNAP=/opt/venv/lt-autosnap/bin/ltautosnap  # or whatever you get from `which ltautosnap`

   # Generate a snapshot for vol0, set0 every day at midnight, no matter what
   0 0 * * *  root $LTAUTOSNAP snap 0 0

   # Every hour at 3 minutes after the hour, for vol0, set1, if a period has
   #   elapsed since the last snap of the set, create another one.
   3 * * * *  root $LTAUTOSNAP autosnap 0 1

   # Every day at 3 AM remove all extra snaps (beyond each snapset's count)
   #   starting with the oldest
   0 3 * * *  root $LTAUTOSNAP clean all

   # Every hour at 5 after, for volume 1, automatically create new snaps as needed
   #   and clean old ones for all snap sets.
   5 0 * * *  root $LTAUTOSNAP autosnap 1 --autoclean

   # Every day at noon, check if each volume's pool has exceeded the warning level
   #   This will log a warning to stderr if the warning level has been exceeded.
   #   If MAILTO is set and your MTA is configured, you'll be emailed only if the
   #   warning percent is exceeded.
   0 12 * * *  root $LTAUTOSNAP check all

   # On the first day of the month, do the same but print the % used space to
   #   stderr no matter what. If MAILTO is set and your MTA is configued, you'll
   #   be emailed the volume usage every month.
   0 0 1 * *  root $LTAUTOSNAP check all -v
   ```
