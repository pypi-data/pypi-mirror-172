#!/usr/bin/env python3

import os
import argparse
from auterioncli.commands import available_commands

from auterioncli.meta_util import PersistentState, check_for_updates, get_version, eprint

def main():

    persistent_state = PersistentState()

    config = {
        "device_address": os.getenv('AUTERION_DEVICE_ADDRESS', "10.41.1.1")
    }
    commands = available_commands(config)

    main_parser = argparse.ArgumentParser()
    main_parser.add_argument('--version', help='Print version of this tool', action='store_true')
    command_subparsers = main_parser.add_subparsers(title="command", metavar='<command>', dest="root_command")

    for name, command in commands.items():
        parser = command_subparsers.add_parser(name, help=command.help())
        command.setup_parser(parser)

    args = main_parser.parse_args()

    if args.version:
        print(get_version())
        exit(0)

    if args.root_command is None:
        main_parser.print_help()
        exit(1)

    check_for_updates(persistent_state)

    try:
        # Run command
        commands[args.root_command].run(args)
    except Exception as e:
        # Give command modules as chance to handle their exceptions
        commands[args.root_command].handle_exception(e)
    except KeyboardInterrupt:
        eprint("Aborting..")
        exit(1)

    persistent_state.persist()


if __name__ == "__main__":
    main()
