import logging
import pathlib
import sys

import astroid
import click
import libcst as cst

from .transform import LazyLogTransformer, clear_cache, get_cache, handle_call

log = logging.getLogger()


@click.command()
@click.option(
    "--check", is_flag=True, default=False, help="Only run a check and set the exit status if there would be a change"
)
@click.option("-s", "--silent", is_flag=True, default=False, help="Don't output anything to stdout")
@click.option("-v", "--verbose", is_flag=True, default=False, help="Increase verbosity")
@click.argument("files", nargs=-1, type=click.Path(exists=True))
def main(files, check, verbose, silent):
    if silent and verbose:
        log.error("Both silent and verbose options set")
        sys.exit(-1)

    if silent:
        log.setLevel(logging.ERROR)

    if verbose:
        log.setLevel(logging.INFO)

    found_files: set[pathlib.Path] = set()

    for filename in files:
        file = pathlib.Path(filename)

        if not file.exists():
            log.error("Could not find %s", file)
            sys.exit(-1)

        if file.is_dir():
            for path in file.rglob("*.py"):
                log.info("Found %s", path)
                found_files.add(path)
        else:
            log.info("Found %s", file)
            found_files.add(file)

    for file in sorted(found_files):
        log.info("Checking %s...", file)

        file_data = file.read_text()

        # TODO use a visitor not a transformer
        astroid.MANAGER.register_transform(astroid.Call, handle_call)

        # Use astroid to scan the file for logging.Logger.<function> calls
        # These calls are stored as a set of positions (line, col) in FOUND_LOG_CALLS
        astroid.parse(file_data)
        astroid.MANAGER.unregister_transform(astroid.Call, handle_call)
        astroid.MANAGER.clear_cache()

        if len(get_cache()) == 0:
            # No log function calls have been detected
            log.info("Leaving %s unchanged", file)
            continue

        # Run the libcst transformer
        # It will visit all of the call nodes with position metadata
        # If it matches the ones found in astroid, it will add them to the list of calls to modify
        # Only calls that have been matched will have the transformation applied
        source_tree = cst.metadata.MetadataWrapper(cst.parse_module(file_data))  # type: ignore
        transformer = LazyLogTransformer()
        modified_tree = source_tree.visit(transformer)

        clear_cache()

        if file_data != modified_tree.code:
            if check:
                # TODO Total up changed files
                sys.exit(-1)

            log.warning("%s has changed, writing", file)
            file.write_text(modified_tree.code)
        else:
            log.info("Leaving %s unchanged", file)
