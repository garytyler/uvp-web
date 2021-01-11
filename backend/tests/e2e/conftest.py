import tarfile
from pathlib import Path

import pytest


@pytest.fixture
def retrieve_from_workdir(pytestconfig, tmp_path):
    def _retrieve_from_workdir(container, rel_path):
        archive_src = Path(container.attrs["Config"]["WorkingDir"]) / rel_path
        archive_dest = tmp_path / rel_path
        extract_dest = Path(pytestconfig.rootdir) / rel_path
        stream, _ = container.get_archive(archive_src)
        with open(archive_dest, "wb") as f:
            for chunk in stream:
                f.write(chunk)
        with tarfile.open(archive_dest, "r") as f:
            f.extractall(pytestconfig.rootdir)
        return extract_dest

    yield _retrieve_from_workdir
