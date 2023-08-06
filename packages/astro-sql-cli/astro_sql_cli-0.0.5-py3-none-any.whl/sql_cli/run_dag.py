from __future__ import annotations

import logging
import sys
import warnings
from datetime import datetime
from typing import Any, List

from airflow.configuration import secrets_backend_list
from airflow.models.connection import Connection
from airflow.models.dag import DAG
from airflow.models.dagrun import DagRun
from airflow.models.taskinstance import TaskInstance
from airflow.secrets.local_filesystem import LocalFilesystemBackend
from airflow.utils import timezone
from airflow.utils.session import NEW_SESSION, provide_session
from airflow.utils.state import DagRunState, State
from airflow.utils.types import DagRunType
from rich import print as pprint
from sqlalchemy.orm.session import Session

from astro.sql.operators.cleanup import AstroCleanupException

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class AstroFilesystemBackend(LocalFilesystemBackend):
    def __init__(
        self,
        connections: dict[str, Connection] = None,
        variables_file_path: str | None = None,
        connections_file_path: str | None = None,
    ):
        self._local_conns: dict[str, Connection] = connections or {}
        super().__init__(variables_file_path=variables_file_path, connections_file_path=connections_file_path)

    @property
    def _local_connections(self) -> dict[str, Connection]:
        conns = self._local_conns
        conns.update(super()._local_connections)
        return conns


@provide_session
def run_dag(
    dag: DAG,
    execution_date: datetime | None = None,
    run_conf: dict[str, Any] | None = None,
    conn_file_path: str | None = None,
    variable_file_path: str | None = None,
    connections: dict[str, Connection] | None = None,
    session: Session = NEW_SESSION,
) -> None:
    """
    Execute one single DagRun for a given DAG and execution date.

    :param dag: The Airflow DAG we will run
    :param execution_date: execution date for the DAG run
    :param run_conf: configuration to pass to newly created dagrun
    :param conn_file_path: file path to a connection file in either yaml or json
    :param variable_file_path: file path to a variable file in either yaml or json
    :param session: database connection (optional)
    """

    execution_date = execution_date or timezone.utcnow()
    dag.log.debug("Clearing existing task instances for execution date %s", execution_date)
    dag.clear(
        start_date=execution_date,
        end_date=execution_date,
        dag_run_state=False,  # type: ignore
        session=session,
    )
    dag.log.debug("Getting dagrun for dag %s", dag.dag_id)
    dr: DagRun = _get_or_create_dagrun(
        dag=dag,
        start_date=execution_date,
        execution_date=execution_date,
        run_id=DagRun.generate_run_id(DagRunType.MANUAL, execution_date),
        session=session,
        conf=run_conf,
    )

    if conn_file_path or variable_file_path or connections:
        local_secrets = AstroFilesystemBackend(
            variables_file_path=variable_file_path,
            connections_file_path=conn_file_path,
            connections=connections,
        )
        secrets_backend_list.insert(0, local_secrets)

    tasks = dag.task_dict
    dag.log.debug("starting dagrun")
    # Instead of starting a scheduler, we run the minimal loop possible to check
    # for task readiness and dependency management. This is notably faster
    # than creating a BackfillJob and allows us to surface logs to the user
    while dr.state == State.RUNNING:
        schedulable_tis, _ = dr.update_state(session=session)
        for ti in schedulable_tis:
            add_logger_if_needed(dag, ti)
            ti.task = tasks[ti.task_id]
            _run_task(ti, session=session)
    pprint(f"Dagrun {dr.dag_id} final state: {dr.state}")
    if conn_file_path or variable_file_path:
        # Remove the local variables we have added to the secrets_backend_list
        secrets_backend_list.pop(0)


def add_logger_if_needed(dag: DAG, ti: TaskInstance) -> None:
    """
    Add a formatted logger to the taskinstance so all logs are surfaced to the command line instead
    of into a task file. Since this is a local test run, it is much better for the user to see logs
    in the command line, rather than needing to search for a log file.
    :param ti: The taskinstance that will receive a logger

    """
    logging_format = logging.Formatter("[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s")
    handler = logging.StreamHandler(sys.stdout)
    handler.level = logging.INFO
    handler.setFormatter(logging_format)
    # only add log handler once
    if not any(isinstance(h, logging.StreamHandler) for h in ti.log.handlers):
        dag.log.debug("Adding Streamhandler to taskinstance %s", ti.task_id)
        ti.log.addHandler(handler)


def _run_task(ti: TaskInstance, session: Session) -> None:
    """
    Run a single task instance, and push result to Xcom for downstream tasks. Bypasses a lot of
    extra steps used in `task.run` to keep our local running as fast as possible
    This function is only meant for the `dag.test` function as a helper function.

    :param ti: TaskInstance to run
    """
    pprint("[bold green]*****************************************************[/bold green]")
    if hasattr(ti, "map_index") and ti.map_index > 0:
        pprint("Running task %s index %d", ti.task_id, ti.map_index)
    else:
        pprint(f"Running task [bold red]{ti.task_id}[/bold red]")
    try:
        warnings.filterwarnings(action="ignore")
        ti._run_raw_task(session=session)  # skipcq: PYL-W0212
        session.flush()
        session.commit()
        pprint(f"[bold red]{ti.task_id}[/bold red] ran successfully!")
    except AstroCleanupException:
        pprint("aql.cleanup async, continuing")
    pprint("[bold green]*****************************************************[/bold green]")


def _get_or_create_dagrun(
    dag: DAG,
    conf: dict[Any, Any] | None,
    start_date: datetime,
    execution_date: datetime,
    run_id: str,
    session: Session,
) -> DagRun:
    """
    Create a DAGRun, but only after clearing the previous instance of said dagrun to prevent collisions.
    This function is only meant for the `dag.test` function as a helper function.
    :param dag: Dag to be used to find dagrun
    :param conf: configuration to pass to newly created dagrun
    :param start_date: start date of new dagrun, defaults to execution_date
    :param execution_date: execution_date for finding the dagrun
    :param run_id: run_id to pass to new dagrun
    :param session: sqlalchemy session
    :return: the Dagrun object needed to run tasks.
    """
    log.info("dagrun id: %s", dag.dag_id)
    dr: DagRun = (
        session.query(DagRun)
        .filter(DagRun.dag_id == dag.dag_id, DagRun.execution_date == execution_date)
        .first()
    )
    if dr:
        session.delete(dr)
        session.commit()
    dr = dag.create_dagrun(
        state=DagRunState.RUNNING,
        execution_date=execution_date,
        run_id=run_id,
        start_date=start_date or execution_date,
        session=session,
        conf=conf,  # type: ignore
    )
    pprint(f"Created dagrun [bold blue]{str(dr)}[/bold blue]", str(dr))
    return dr
