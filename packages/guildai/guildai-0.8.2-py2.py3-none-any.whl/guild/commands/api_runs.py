# Copyright 2017-2022 RStudio, PBC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import click

from guild import click_util

from . import api_support
from . import runs_support


@click.command("runs")
@api_support.output_options
@runs_support.runs_arg
@runs_support.all_filters
@click_util.use_args
@click.option("--include-batch", is_flag=True, help="Include batch runs.")
@click_util.render_doc
def main(args):
    """Show runs as JSON."""
    api_support.out(_runs_data(args), args)


def _runs_data(args):
    from .view_impl import ViewDataImpl

    return ViewDataImpl(args).runs_data()
