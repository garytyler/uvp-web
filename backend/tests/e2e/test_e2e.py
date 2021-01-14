import os
import sys
import uuid


class EndToEndTestError(Exception):
    pass


def test_e2e_from_frontend(docker_client, pytestconfig, capsys):
    fe_container = docker_client.containers.get("frontend")
    fe_uid = fe_container.exec_run("id -u").output.decode().strip()
    output = ""
    try:
        pw_container = docker_client.containers.run(
            image="mcr.microsoft.com/playwright:focal",
            name=f"test-playwright-{uuid.uuid4()}",
            command=["npm", "run", "coverage:e2e"],
            user=os.geteuid() if os.geteuid() == fe_uid else 0,
            working_dir=fe_container.attrs["Config"]["WorkingDir"],
            network_mode=f"container:{fe_container.id}",
            volumes_from=fe_container.id,
            ipc_mode="host",
            auto_remove=True,
            detach=True,
            stream=True,
            tty=False,
        )
        for line in pw_container.logs(stream=True, stdout=True, stderr=True):
            output += line.decode()
        if 0 != pw_container.wait()["StatusCode"]:
            raise EndToEndTestError(output)
    finally:
        try:
            pw_container.remove(force=True)
        except Exception:
            pass
    if output and pytestconfig.getoption("verbose") > 0:
        with capsys.disabled():
            sys.stdout.write(output)
