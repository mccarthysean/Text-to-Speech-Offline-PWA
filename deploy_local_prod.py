# /!/usr/bin/env python3

import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

env_file = Path(__file__).parent / ".env"
print(f"Loading environment variables from: {env_file}")
load_dotenv(dotenv_path=env_file, verbose=True, override=True)

# Gitlab repo
# ci_registry = "registry.gitlab.com"
ci_registry = "https://index.docker.io/v1/"
ci_project_namespace = "mccarthysean"
ci_project_name = "text_to_speech"
docker_service_name = "text_to_speech"
git_repo_name = "rcom"

custom_version = "0.1.2"
# For Gitlab
# image = f"{ci_registry}/{ci_project_namespace}/{ci_project_name}"

# IMAGE_PROD_FINAL = f"{image}:text_to_speech-{custom_version}"
IMAGE_PROD_FINAL="mccarthysean/text_to_speech:latest"

# Set the environment variables the Docker Compose files will use
os.environ["IMAGE_PROD_FINAL"] = IMAGE_PROD_FINAL
# This is used in the Dockerfile.prod files to ensure the cache is busted and certain
# RUN commands are re-run every time the image is built.
os.environ["CACHEBUST"] = datetime.now().strftime("%Y%m%d%H%M%S")

# To ensure we use BuildKit for faster, more efficient builds
os.environ["DOCKER_BUILDKIT"] = "1"
os.environ["BUILDKIT_INLINE_CACHE"] = "1"
os.environ["COMPOSE_DOCKER_CLI_BUILD"] = "1"


def check_var(var, var_name):
    """Check if the environment variable is NULL"""
    if not var:
        print(f"{var_name} is NULL! Exiting...")
        sys.exit(1)

    print(f"{var_name} is good")


def run_command(command: str, raise_error: bool = True, shell: bool = True) -> None:
    """Run a shell command. If the command fails, raise an exception"""

    rc = None
    stdout = None
    stderr = None
    try:
        print(f"Running command: {command}")
        # process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        # for c in iter(lambda: process.stdout.read(1), b""):
        #     sys.stdout.buffer.write(c)
        #     print(c)
        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=shell
        )

        # Read stdout line by line
        for line in iter(process.stdout.readline, b""):
            print(line.strip().decode("utf-8"))

        # get the return code, stdout and stderr
        rc = process.poll()
        stdout, stderr = process.communicate()
        print(f"rc: {rc}")
        print(f"stdout: {stdout.decode('utf-8') if stdout else None}")
        print(f"stderr: {stderr.decode('utf-8') if stderr else None}")
    except subprocess.CalledProcessError:
        if raise_error:
            raise

    if rc != 0:
        print(
            f"Command had a non-zero exit status: {rc}. Command: {command}. Stdout: {stdout}. Stderr: {stderr}"
        )
        if raise_error:
            raise subprocess.CalledProcessError(rc, command)
        # sys.exit(rc)

    return None


def setup(branch: str = "main") -> None:
    """Setup function"""

    print("Setting up the environment...")
    print("Checking the current branch...")
    run_command("git rev-parse --abbrev-ref HEAD", raise_error=False, shell=True)

    print(f"Checking out the '{branch}' branch...")
    run_command(f"git checkout {branch} || true", raise_error=False, shell=True)

    print("Fetching the latest changes...")
    run_command("git fetch", raise_error=True, shell=True)

    print("Pulling the latest changes...")
    run_command("git pull", raise_error=True, shell=True)

    # Set the current working directory to the directory in which the script is located, for CI/CD
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print(f"Current working directory: {os.getcwd()}")

    print("\nChecking the environment variable...")
    DOCKER_HUB_PASSWORD = os.getenv("DOCKER_HUB_PASSWORD")
    print(f"DOCKER_HUB_PASSWORD = {DOCKER_HUB_PASSWORD}")

    check_var(DOCKER_HUB_PASSWORD, "DOCKER_HUB_PASSWORD")

    # Login to the Gitlab container registry (with a project-specific token) and download the images
    print("\nLogging into Docker container repo so we can pull and push images...")
    run_command(
        # f"docker login -u gitlab+deploy-token-598621 -p {GITLAB_DEPLOY_TOKEN} {ci_registry}",
        f"docker login {ci_registry} -u {ci_project_namespace} -p {os.getenv('DOCKER_HUB_PASSWORD')}",
        raise_error=False,
        shell=True,
    )


def build_and_push():
    """Build and push the Docker images"""

    # Pull images
    run_command(
        f"docker pull {IMAGE_PROD_FINAL}", raise_error=False, shell=True
    )

    # Build and push images
    print("\nBuilding the production image...")
    run_command("docker compose -f docker-compose.build.prod.yml build")

    print("\nPushing the production image...")
    run_command(f"docker push {IMAGE_PROD_FINAL}")

    print(f"\nFinished building and pushing the Docker image to {IMAGE_PROD_FINAL}")


def run_docker_swarm():
    """Run the Docker Swarm"""

    print("\nDeploying to the Docker swarm...")
    run_command(
        f"docker stack deploy --with-registry-auth -c docker-compose.ci.prod.yml {docker_service_name}"
    )

    run_command(f"docker pull {IMAGE_PROD_FINAL}")
    run_command(
        f"docker service update --image {IMAGE_PROD_FINAL} --with-registry-auth {docker_service_name}"
    )

    run_command(f"docker stack ps {docker_service_name}")
    run_command("docker service ls")

    return None


def run_kubernetes():
    """Deploy Kubernetes resources"""

    print("\nDeploying Kubernetes resources...")
    # run_command("microk8s kubectl apply -f /home/ubuntu/git/{git_repo_name}/kubernetes")
    run_command(f"bash /home/ubuntu/git/{git_repo_name}/kubernetes/deploy.k8s.sh")

    return None


def main() -> None:
    """Main function"""

    staging_or_main: str = (
        input(
            "Are you deploying to 'staging' or 'main' branch? [staging/main] (default main): "
        )
        or "main"
    )
    pull_image = (
        input("Do you want to pull the Docker image? [y/N] (default y): ") or "y"
    )
    build_push = (
        input("Do you want to build and push the Docker images? [y/N] (default y): ")
        or "y"
    )
    deploy_swarm = (
        input("Do you want to deploy to the Docker Swarm? [y/N] (default n): ") or "n"
    )
    deploy_k8s = (
        input("Do you want to deploy to Kubernetes? [y/N] (default n): ") or "n"
    )

    branch: str = staging_or_main.lower()
    if branch == "staging":
        print("You are deploying to the staging branch.")
    elif branch == "main":
        print("You are deploying to the main branch.")
    else:
        print("Invalid input. Exiting...")
        sys.exit(1)
    setup(branch=branch)

    if pull_image.lower() == "y":
        run_command(
            f"docker pull {IMAGE_PROD_FINAL}", raise_error=False, shell=True
        )

    if build_push.lower() == "y":
        build_and_push()

    if deploy_swarm.lower() == "y":
        run_docker_swarm()

    if deploy_k8s.lower() == "y":
        run_kubernetes()

    return None


if __name__ == "__main__":
    main()
