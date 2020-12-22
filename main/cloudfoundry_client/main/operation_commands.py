from typing import Tuple

from cloudfoundry_client.client import CloudFoundryClient
from cloudfoundry_client.main.command_domain import Command, ParserGenerator
from cloudfoundry_client.operations.push.push import PushOperation


def generate_push_command() -> Tuple[Command, str]:
    entry = 'push_app'

    def generate_parser(parser: ParserGenerator):
        command_parser = parser(entry)
        command_parser('manifest_path', dict(metavar='manifest_paths', type=str, nargs=1,
                       help='The manifest path'))
        command_parser('-space_guid', dict(action='store', dest='space_guid', type=str,
                       help='Space guid'))

    def execute(client: CloudFoundryClient, arguments: object):
        manifest_path = arguments.manifest_path[0]
        PushOperation(client).push(arguments.space_guid, manifest_path)

    return Command(entry, generate_parser, execute), 'Push an application by its manifest'
