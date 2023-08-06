import os
import shutil
import subprocess
import sys
import tempfile
from typing import Optional

import click
import coiled
from rich import print

from .utils import CONTEXT_SETTINGS


def open_ssh(address: str, key: str, jump_to_address: Optional[str] = None):
    """Open an SSH session, relies on `ssh` and `ssh-add` (agent)."""

    if not shutil.which("ssh"):
        print(
            "Unable to find `ssh`, you may need to install OpenSSH or add it to your paths."
        )
        return

    if not shutil.which("ssh-add"):
        print(
            "Unable to find `ssh-add`, you may need to install OpenSSH or add it to your paths."
        )
        return

    with tempfile.TemporaryDirectory() as keydir:
        key_path = os.path.join(keydir, f"scheduler-key-{address}.pem")

        with open(key_path, "w") as f:
            f.write(key)

        # ssh needs file permissions to be set
        os.chmod(key_path, mode=0o600)

        # briefly add key to agent, this allows us to jump to worker with agent forwarding
        p = subprocess.run(["ssh-add", key_path, "-t", "5"], capture_output=True)

        if p.returncode and p.stderr:
            print(
                "An error occurred calling `ssh-add`. You may need to enable the ssh agent."
            )
            print(p.stderr)
            return

    if jump_to_address:
        ssh_target = f"-J ubuntu@{address} ubuntu@{jump_to_address}"
        ssh_target_label = f"worker at {jump_to_address}"
    else:
        ssh_target = f"ubuntu@{address}"
        ssh_target_label = f"scheduler at {address}"

    ssh_command = f"ssh {ssh_target} -o StrictHostKeyChecking=no -o ForwardAgent=yes"

    # print(ssh_command)
    print(f"===Starting SSH session to {ssh_target_label}===")
    subprocess.run(ssh_command, shell=True)
    print("===SSH session closed===")


@click.group(context_settings=CONTEXT_SETTINGS)
def cluster():
    """Commands for managing Coiled clusters"""
    pass


# @click.command(context_settings=CONTEXT_SETTINGS)
# def list():
#     print(f"...pretend this is a list of clusters...")


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument("cluster")
@click.option(
    "--private",
    default=False,
    is_flag=True,
    help="Use private IP address of scheduler (default is public IP address)",
)
@click.option(
    "--worker",
    default=None,
    help="Connect to worker with specified name or private IP address (default is to connect to scheduler)",
)
def ssh(cluster: str, private: bool, worker: Optional[str]):
    with coiled.Cloud() as cloud:

        if cluster.isnumeric():
            cluster_id = int(cluster)
        else:
            try:
                cluster_id = cloud.get_cluster_by_name(name=cluster)
            except coiled.errors.DoesNotExist:
                cluster_id = None

        if not cluster_id:
            print(f"Unable to find cluster `{cluster}`")
            return

        ssh_info = cloud.get_ssh_key(cluster_id=cluster_id, worker=worker)

        # print(ssh_info)

        if ssh_info["scheduler_state"] != "started":
            print(
                f"Scheduler state is {ssh_info['scheduler_state']}. "
                "You can only connect when scheduler is 'started'."
            )
            return

        scheduler_address = (
            ssh_info["scheduler_private_address"]
            if private
            else ssh_info["scheduler_public_address"]
        )

        if not scheduler_address:
            print("Unable to retrieve scheduler address")
            return

        if not ssh_info["private_key"]:
            print("Unable to retrieve SSH key")
            return

        open_ssh(
            address=scheduler_address,
            key=ssh_info["private_key"],
            jump_to_address=ssh_info["worker_address"],
        )


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument("cluster")
@click.option(
    "--scheduler",
    default=False,
    is_flag=True,
    help="Get scheduler logs",
)
@click.option(
    "--workers",
    help="Get worker logs ('any', 'all', or comma-delimited list of names, states, or internal IP addresses)",
)
@click.option(
    "--follow",
    default=False,
    is_flag=True,
    help="Passed directly to `aws logs tail`, see aws cli docs for details.",
)
@click.option(
    "--filter",
    default=None,
    help="Passed directly to `aws logs tail`, see aws cli docs for details.",
)
@click.option(
    "--since",
    default=None,
    help="Passed directly to `aws logs tail`, see aws cli docs for details.",
)
@click.option(
    "--profile",
    default=None,
    help="Passed directly to `aws logs tail`, see aws cli docs for details.",
)
def logs(
    cluster: str,
    scheduler: bool,
    workers: Optional[str],
    follow: bool,
    filter: Optional[str],
    since: Optional[str],
    profile: Optional[str],
):

    do_logs(cluster, scheduler, workers, follow, filter, since, profile)


def do_logs(
    cluster: str,
    scheduler: bool,
    workers: Optional[str],
    follow: bool,
    filter: Optional[str],
    since: Optional[str],
    profile: Optional[str],
    capture: bool = False,
):

    if not shutil.which("aws"):
        raise click.ClickException("`coiled cluster logs` relies on AWS CLI.")

    with coiled.Cloud() as cloud:

        if cluster.isnumeric():
            cluster_id = int(cluster)
        else:
            try:
                recent_cluster = cloud.get_clusters_by_name(name=cluster)[-1]

                if recent_cluster["current_state"]["state"] in ("stopped", "error"):
                    follow = False
                    print(
                        f"[red]Cluster state is {recent_cluster['current_state']['state']} so not following.[/red]",
                        file=sys.stderr,
                    )

                cluster_id = recent_cluster["id"]

            except coiled.errors.DoesNotExist:
                cluster_id = None

        if not cluster_id:
            raise click.ClickException(f"Unable to find cluster `{cluster}`")

        cluster_info = cloud.cluster_details(cluster_id)

        if workers:
            worker_attrs_to_match = workers.split(",")

            def filter_worker(idx, worker):
                if workers == "all":
                    return True
                elif workers == "any":
                    if idx == 0:
                        return True
                else:
                    if worker.get("name") and worker["name"] in worker_attrs_to_match:
                        return True
                    elif (
                        worker.get("instance", {}).get("private_ip_address")
                        and worker["instance"]["private_ip_address"]
                        in worker_attrs_to_match
                    ):
                        return True
                    elif (
                        worker.get("current_state", {}).get("state")
                        and worker["current_state"]["state"] in worker_attrs_to_match
                    ):
                        return True

                return False

            worker_names = [
                worker["name"]
                for i, worker in enumerate(cluster_info["workers"])
                if filter_worker(i, worker)
            ]
        else:
            worker_names = []

        log_info = cloud.get_cluster_log_info(cluster_id)

        if log_info["type"] == "vm_aws":

            group_name = log_info["log_group"]
            region = log_info["region"]

            stream_names = []

            if not group_name:
                raise click.ClickException(
                    "Unable to find CloudWatch Log Group for this cluster."
                )

            if scheduler:
                stream_names.append(log_info["scheduler_stream"])

            if workers:
                worker_stream_name = [
                    log_info["worker_streams"][worker_name]
                    for worker_name in worker_names
                ]
                stream_names.extend(worker_stream_name)

            if not stream_names:
                raise click.ClickException(
                    "No matching CloudWatch Log Streams to show, use `--scheduler` or `--workers`."
                )  # FIXME better error

            streams = ",".join(stream_names)

            command = f"aws logs tail {group_name} --region {region} --log-stream-names {streams}"
            if follow:
                command = f"{command} --follow"
            if filter:
                command = f"{command} --filter {filter}"
            if since:
                command = f"{command} --since {since}"
            if profile:
                command = f"{command} --profile {profile}"

            return subprocess.run(command.split(" "), capture_output=capture)

            # TODO `aws logs tail` gives ResourceNotFoundException error ("The specified log stream does not exist.")
            #   when *any* of the log streams doesn't exist. We should query to see which exist before trying to tail.

        else:
            raise click.ClickException(
                f"Cluster backend type is {log_info['type']}, only AWS is currently supported."
            )


# cluster.add_command(list)
cluster.add_command(ssh)
cluster.add_command(logs)
