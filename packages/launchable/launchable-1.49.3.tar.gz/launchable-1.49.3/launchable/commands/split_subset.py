import os

import click

from ..utils.click import FRACTION, FractionType
from ..utils.env_keys import REPORT_ERROR_KEY
from ..utils.http_client import LaunchableClient
from .test_path_writer import TestPathWriter


@click.group(help="Split subsetting tests")
@click.option(
    '--subset-id',
    'subset_id',
    help='subset id',
    type=str,
    required=True,
)
@click.option(
    '--bin',
    'bin_target',
    help='bin',
    type=FRACTION,
    required=True
)
@click.option(
    '--rest',
    'rest',
    help='output the rest of subset',
    type=str,
)
@click.option(
    '--base',
    'base_path',
    help='(Advanced) base directory to make test names portable',
    type=click.Path(exists=True, file_okay=False),
    metavar="DIR",
)
@click.pass_context
def split_subset(context: click.core.Context, subset_id: str, bin_target: FractionType, rest: str, base_path: str):

    TestPathWriter.base_path = base_path

    class SplitSubset(TestPathWriter):
        def __init__(self, dry_run: bool = False):
            super(SplitSubset, self).__init__(dry_run=dry_run)

        def run(self):
            index = bin_target[0]
            count = bin_target[1]

            if (index == 0 or count == 0):
                click.echo(
                    click.style(
                        'Error: invalid bin value. Make sure to set over 0 like `--bin 1/2` but set `--bin {}`'.format(
                            bin_target),
                        'yellow'),
                    err=True,
                )
                return

            if count < index:
                click.echo(
                    click.style(
                        'Error: invalid bin value. Make sure to set below 1 like `--bin 1/2`, `--bin 2/2` but set `--bin {}`'.format(
                            bin_target),
                        'yellow'),
                    err=True,
                )
                return

            output = []
            rests = []
            is_observation = False

            try:
                client = LaunchableClient(
                    test_runner=context.invoked_subcommand,
                    dry_run=context.obj.dry_run)

                payload = {
                    "sliceCount": count,
                    "sliceIndex": index,
                }

                res = client.request(
                    "POST", "{}/slice".format(subset_id), payload=payload)
                res.raise_for_status()

                output = res.json()["testPaths"]
                rests = res.json()["rest"]
                is_observation = res.json().get("isObservation", False)

            except Exception as e:
                if os.getenv(REPORT_ERROR_KEY):
                    raise e
                else:
                    click.echo(e, err=True)
                    click.echo(click.style(
                        "Warning: the service failed to split subset. Falling back to running all tests", fg='yellow'),
                        err=True)
                    return

            if len(output) == 0:
                click.echo(click.style(
                    "Error: no tests found in this subset id.", 'yellow'), err=True)
                return

            if is_observation:
                output = output + rests
            if rest:
                if len(rests) == 0:
                    rests.append(output[0])

                self.write_file(rest, rests)

            self.print(output)

    context.obj = SplitSubset(dry_run=context.obj.dry_run)
