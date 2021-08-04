# Copyright 2020 - 2021 MONAI Consortium
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser, Namespace, _SubParsersAction
from typing import List

from monai.deploy.runner import runner
from monai.deploy.utils import argparse_types

logger = logging.getLogger(__name__)

def create_run_parser(subparser: _SubParsersAction, command: str, parents: List[ArgumentParser]) -> ArgumentParser:
    parser = subparser.add_parser(command, formatter_class=ArgumentDefaultsHelpFormatter,
                                  parents=parents, add_help=False)

    parser.add_argument("map", metavar="<map-image[:tag]>", help="MAP image name")

    parser.add_argument("input", metavar="<input>", type=argparse_types.valid_existing_path,
                        help="input data path")

    parser.add_argument("output", metavar="<output>", type=argparse_types.valid_path,
                        help="output data path")

    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true',
                        default=False, help='verbose mode')

    parser.add_argument('-q', '--quiet', dest='quiet', action='store_true', default=False,
                        help='execute MAP quietly without printing container logs onto console')

    return parser


def execute_run_command(args: Namespace):
    runner.main(args)
