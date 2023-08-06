import difflib
import logging
import subprocess
from io import StringIO
from typing import Callable

from godkjenn.artifact import Artifact

log = logging.getLogger(__name__)


class DiffSelector:
    """Select differ based on MIME types."""

    def __init__(self, mime_type_map, default_command=None):
        self._mime_type_map = mime_type_map
        self._default_command = default_command

    def __getitem__(self, mime_type: str) -> Callable[[Artifact, Artifact], None]:
        try:
            command_template = self._mime_type_map[mime_type]
            log.info("MIME type-specific differ found for %s", mime_type)
        except KeyError:
            command_template = self._default_command
            if command_template is not None:
                log.info("Default diff command used for MIME type %s", mime_type)

        if command_template is not None:
            return _external_command_runner(command_template)

        elif mime_type.startswith("text/"):
            log.info("Fallback text diff command used for MIME type %s", mime_type)
            return _fallback_text_diff

        log.info("Fallback binary diff command used for MIME type %s", mime_type)
        return _fallback_binary_diff


def _external_command_runner(command_template: str):
    def run(received, accepted):
        command = command_template.format(received=received, accepted=accepted)
        log.info("Running diff command => %s", command)
        subprocess.run(command.split())

    return run


def _fallback_text_diff(received: Artifact, accepted: Artifact):
    print(default_text_diff(received.data, accepted.data))


def default_text_diff(received: str, accepted: str) -> str:
    """A default diff report for two strings.

    Args:
        received (str): The received artifact
        accepted (str): The accepted artifact

    Returns:
        str: The diff report.
    """
    diff = difflib.unified_diff(list(StringIO(accepted)), list(StringIO(received)), lineterm="")
    return "\n".join(diff)


def _fallback_binary_diff(received: Artifact, accepted: Artifact):
    diff = default_binary_diff(received.data, accepted.data)
    print(diff)


def default_binary_diff(received: bytes, accepted: bytes) -> str:
    diff = difflib.diff_bytes(
        difflib.unified_diff, [accepted], [received], lineterm=b""
    )
    diff = "\n".join(map(lambda b: b.decode("ascii"), diff))
    return diff
