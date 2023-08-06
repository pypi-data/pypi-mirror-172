import tarfile
import tempfile

import click
import click_log
from convisoappsec.common.box import ContainerWrapper
from convisoappsec.flowcli import help_option
from convisoappsec.flowcli.common import on_http_error, project_code_option
from convisoappsec.flowcli.context import pass_flow_context
from convisoappsec.logger import LOGGER

click_log.basic_config(LOGGER)


@click.command()
@click_log.simple_verbosity_option(LOGGER)
@project_code_option(
    help="Not required when --no-send-to-flow option is set",
    required=False
)
@click.option(
    '-r',
    '--repository-dir',
    default=".",
    show_default=True,
    type=click.Path(
        exists=True,
        resolve_path=True,
    ),
    required=False,
    help="The source code repository directory.",
)
@click.option(
    "--send-to-flow/--no-send-to-flow",
    default=True,
    show_default=True,
    required=False,
    help="""Enable or disable the ability of send analysis result
    reports to flow. When --send-to-flow option is set the --project-code
    option is required""",
    hidden=True
)
@click.option(
    "--scanner-timeout",
    hidden=True,
    required=False,
    default=7200,
    type=int,
    help="Set timeout for each scanner"
)
@click.option(
    "--parallel-workers",
    hidden=True,
    required=False,
    default=2,
    type=int,
    help="Set max parallel workers"
)
@click.option(
    "--deploy-id",
    default=None,
    required=False,
    hidden=True,
    envvar="FLOW_DEPLOY_ID"
)
@help_option
@pass_flow_context
def run(
    flow_context,
    project_code,
    repository_dir,
    send_to_flow,
    scanner_timeout,
    parallel_workers,
    deploy_id
):
    '''
      This command will perform IAC analysis at the source code. The analysis
      results can be reported or not to flow application.

    '''

    if send_to_flow and not project_code:
        raise click.MissingParameter(
            'It is required when sending reports to Conviso API .',
            param_type='option',
            param_hint='--project-code',
        )

    perform_command(
        flow_context,
        project_code,
        repository_dir,
        send_to_flow,
        scanner_timeout,
        parallel_workers,
        deploy_id
    )


def perform_command(
    flow_context, project_code, repository_dir, send_to_flow, scanner_timeout, parallel_workers, deploy_id
):
    try:
        REQUIRED_CODEBASE_PATH = '/code'
        IAC_IMAGE_NAME = 'sastbox-iac-scanner-checkov'
        IAC_SCAN_FILENAME = '/{}.sarif'.format(IAC_IMAGE_NAME)
        containers_map = {
            IAC_IMAGE_NAME: {
                'repository_dir': repository_dir,
                'repository_name': IAC_IMAGE_NAME,
                'tag': 'latest',
                'command': [
                    '-v',
                    '--codebase', REQUIRED_CODEBASE_PATH,
                    '--output', IAC_SCAN_FILENAME
                ],
            },
        }

        LOGGER.info('\U0001F4AC Preparing Environment')
        flow = flow_context.create_flow_api_client()
        token = flow.docker_registry.get_sast_token()
        scanners_wrapper = ContainerWrapper(
            token=token,
            containers_map=containers_map,
            logger=LOGGER,
            timeout=scanner_timeout
        )

        LOGGER.info('\U0001F4AC Starting IaC')
        scanners_wrapper.run()

        LOGGER.info('\U0001F4AC Processing Results')
        if send_to_flow:
            for scanner in scanners_wrapper.scanners:

                report_filepath = scanner.results
                if report_filepath:
                    compatible_report_filepath = convert_sarif_to_sastbox1(
                        report_filepath, repository_dir, token, scanner_timeout
                    )
                    with open(compatible_report_filepath) as report_file:
                        LOGGER.info(
                            "   Sending {} data to Conviso Platform...".format(
                                scanner.name)
                        )
                        response = flow.findings.create(
                            project_code=project_code,
                            commit_refs=None,
                            finding_report_file=report_file,
                            default_report_type="sast",
                            deploy_id=deploy_id,
                        )

                        if response < 210:
                            LOGGER.info('   {} data has been sent successfully'.format(
                                scanner.name
                            ))
                        else:
                            LOGGER.info('   {} was not sent, Conviso will be notified about this error.'.format(
                                scanner.name
                            ))
                else:
                    LOGGER.info('   {} has no issues to report'.format(
                        scanner.name
                    ))

        LOGGER.info('\U00002705 IaC Scan Finished')

    except Exception as e:
        on_http_error(e)
        raise click.ClickException(str(e)) from e


def convert_sarif_to_sastbox1(report_filepath, repository_dir, token, scanner_timeout):
    """

    Args:
        report_filepath (string): filepath to the report to be converted
        repository_dir (string): filepath to the repository being tested
        token (string): conviso platform token
        scanner_timeout (string): container timeout

    Returns:
        string: filepath to the converted report
    """
    CONTAINER_IMAGE_NAME = 'sastbox-converter-tool'

    CONTAINER_INPUT_FILEPATH = '/code{}'.format(
        report_filepath.replace(repository_dir, '')
    )
    CONTAINER_OUTPUT_FILENAME = CONTAINER_INPUT_FILEPATH.replace(
        'sarif', 'json'
    )

    CONTAINERS_MAP = {
        CONTAINER_IMAGE_NAME: {
            'repository_dir': repository_dir,
            'repository_name': CONTAINER_IMAGE_NAME,
            'tag': 'latest',
            'command': [
                '-v',
                '--format', 'sastbox1',
                '--input', CONTAINER_INPUT_FILEPATH,
                '--output', CONTAINER_OUTPUT_FILENAME
            ],
        },
    }
    converter_wrapped = ContainerWrapper(
        token=token,
        containers_map=CONTAINERS_MAP,
        logger=LOGGER,
        timeout=scanner_timeout
    )

    converter_wrapped.logger.setLevel('WARN')
    converter_wrapped.run()
    converter_wrapped.logger.setLevel('INFO')

    scanner = converter_wrapped.scanners[0].scanner
    last_scan_name = scanner.name
    last_container = scanner.docker.containers.get(
        last_scan_name
    )

    chunks, _ = last_container.get_archive(CONTAINER_OUTPUT_FILENAME)
    output_filepath = extract_tarball_chunks(
        chunks, report_filepath.replace('sarif', 'json')
    )
    return output_filepath


def extract_tarball_chunks(tarball_chunks, report_absolute_filepath):
    """

    Args:
        tarball_chunks (int): The number of bytes returned by each iteration of the generator
        report_filename (string): The name of the extracted report

    Returns:
        string: Report absolute filepath in local filesystem
    """
    output_dirpath = report_absolute_filepath[:report_absolute_filepath.rfind(
        '/')]

    with tempfile.TemporaryFile() as tmp_wrapper_file:
        for chunk in tarball_chunks:
            tmp_wrapper_file.write(chunk)
        tmp_wrapper_file.seek(0)

        with tarfile.open(mode="r|", fileobj=tmp_wrapper_file) as talball_file:
            talball_file.extractall(path=output_dirpath)

    return report_absolute_filepath


EPILOG = '''
Examples:

  \b
  1 - Reporting the results to Conviso Platform API:
    1.1 - Running an analysis at all commit range:
      $ export FLOW_API_KEY='your-api-key'
      $ export FLOW_PROJECT_CODE='your-project-code'
      $ {command}

'''  # noqa: E501

SHORT_HELP = "Perform Infrastructure Code analysis"

command = 'flow iac run'
run.short_help = SHORT_HELP
run.epilog = EPILOG.format(
    command=command,
)
