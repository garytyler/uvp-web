import uuid

import docker


class EndToEndTestError(Exception):
    pass


def test_e2e_from_frontend(docker_client, frontend_container, request):
    try:
        pw_container = docker_client.containers.run(
            image="mcr.microsoft.com/playwright:focal",
            name=f"test-playwright-{uuid.uuid4()}",
            command=["npm", "run", "coverage:e2e"],
            working_dir=frontend_container.attrs["Config"]["WorkingDir"],
            network_mode=f"container:{frontend_container.id}",
            volumes_from=frontend_container.id,
            auto_remove=True,
            detach=True,
            stream=True,
            tty=False,
        )
        out = ""
        for line in pw_container.logs(stream=True, stdout=True, stderr=True):
            out += line.decode()
        if 0 != pw_container.wait()["StatusCode"]:
            raise EndToEndTestError(out)
    finally:
        try:
            pw_container.remove(force=True)
        except Exception:
            pass
