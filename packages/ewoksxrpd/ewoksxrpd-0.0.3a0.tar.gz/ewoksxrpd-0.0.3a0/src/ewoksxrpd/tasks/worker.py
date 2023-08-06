import logging
from contextlib import contextmanager
from collections import OrderedDict
from typing import Iterable, Dict, Mapping
from ewokscore.hashing import uhash

import pyFAI
import pyFAI.worker

_WORKER_POOL = None


logger = logging.getLogger(__name__)


class WorkerPool:
    """Pool with one worker per configuration up to a maximum number of workers."""

    def __init__(self, nworkers: int = 1) -> None:
        self.nworkers = nworkers
        self._workers: Dict[int, pyFAI.worker.Worker] = OrderedDict()

    @staticmethod
    def _worker_id(*args):
        # What to do with the mask?
        # return hash(tuple(sorted(integration_options.items())))
        return uhash(args)

    @contextmanager
    def worker(
        self, worker_options: Mapping, integration_options: Mapping
    ) -> Iterable[pyFAI.worker.Worker]:
        # TODO: deal with threads and subprocesses
        worker_id = self._worker_id(worker_options, integration_options)
        worker = self._workers.pop(worker_id, None)
        if worker is None:
            worker = self._create_worker(worker_options, integration_options)
        self._workers[worker_id] = worker
        while len(self._workers) > self.nworkers:
            self._workers.popitem(last=False)
        yield worker

    @staticmethod
    def _create_worker(
        worker_options: Mapping, integration_options: Mapping
    ) -> pyFAI.worker.Worker:
        # Worker class has the following issues:
        # - cannot provide a "mask" in memory through the configuration
        # - the "error_model" parameter is not used
        worker = pyFAI.worker.Worker(**worker_options)
        worker.output = "raw"
        integration_options = dict(integration_options)
        mask = integration_options.pop("mask", None)
        provided = set(integration_options)
        worker.set_config(integration_options, consume_keys=True)
        unused = {k: v for k, v in integration_options.items() if k in provided}
        if unused:
            logger.warning("Unused pyfai integration options: %s", unused)
        if mask is not None:
            worker.ai.set_mask(mask)
        return worker


def _get_global_pool() -> WorkerPool:
    global _WORKER_POOL
    if _WORKER_POOL is None:
        _WORKER_POOL = WorkerPool()
    return _WORKER_POOL


def maximum_persistent_workers(nworkers: int) -> None:
    pool = _get_global_pool()
    pool.nworkers = nworkers


@contextmanager
def persistent_worker(
    worker_options: Mapping,
    integration_options: Mapping,
) -> Iterable[pyFAI.worker.Worker]:
    """Get a worker for a particular configuration that stays in memory."""
    pool = _get_global_pool()
    with pool.worker(worker_options, integration_options) as worker:
        yield worker
