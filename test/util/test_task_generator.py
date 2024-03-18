import RobotRaconteur as RR
from RobotRaconteurCompanion.Util.TaskGenerator import AsyncTaskGenerator, SyncTaskGenerator
from RobotRaconteurCompanion.Util.TestFixtures import IntraTaskFixture

import time
import pytest

robdef_text = """
service experimental.testing.companion.test_task_generator_py

stdver 0.10

import com.robotraconteur.action

using com.robotraconteur.action.ActionStatusCode

struct TestGenStatus
    field ActionStatusCode action_status
    field string message
    field varvalue{string} data
end

object TestGenObject
    function TestGenStatus{generator} test_task_generator(double done_time, double fail_time, double status_update_time, double next_timeout, double watchdog_timeout)
    function TestGenStatus{generator} test_sync_task_generator(double done_time, double fail_time, double next_timeout, double watchdog_timeout)
end
"""


class _TestTaskGenImpl(AsyncTaskGenerator):

    def __init__(self, node, status_type, done_time, fail_time, status_update_time, next_timeout, watchdog_timeout):
        super().__init__(node, status_type, next_timeout, watchdog_timeout)
        self.done_time = done_time
        self.fail_time = fail_time
        self.status_update_time = status_update_time

    def StartTask(self):
        self.task_complete_timer = self._node.CreateTimer(self.done_time, self.task_complete_timeout, True)
        self.task_failed_timer = self._node.CreateTimer(self.fail_time, self.task_failed_timeout, True)
        self.status_update_timer = self._node.CreateTimer(self.status_update_time, self.status_update_timeout, True)

        self.task_complete_timer.Start()
        self.task_failed_timer.Start()
        self.status_update_timer.Start()

    def task_complete_timeout(self, ev):
        if ev.stopped:
            return
        status = self._status_type()
        status.action_status = self._action_const["ActionStatusCode"]["complete"]
        status.message = "Task completed"
        status.data = {}
        status.data["test"] = RR.VarValue([5], "int32[]")
        self.SetResult(status)

        self.task_complete_timer = None
        self.task_failed_timer = None

    def task_failed_timeout(self, ev):
        if ev.stopped:
            return
        err = RR.OperationFailedException("Task failed")
        self.SetResultException(err)

        self.task_complete_timer = None
        self.task_failed_timer = None

    def status_update_timeout(self, ev):
        if ev.stopped:
            return
        self.SendUpdate()


class SyncTestTaskGenImpl(SyncTaskGenerator):
    def __init__(self, node, status_type, done_time, fail_time, next_timeout, watchdog_timeout):
        super().__init__(node, status_type, next_timeout, watchdog_timeout)
        self.done_time = done_time
        self.fail_time = fail_time

    def RunTask(self):
        if self.done_time <= self.fail_time:
            time.sleep(self.done_time)
            status = self._status_type()
            status.message = "Task completed"
            status.data = {}
            status.data["test"] = RR.VarValue([5], "int32[]")
            return status
        else:
            time.sleep(self.fail_time)
            raise RR.OperationFailedException("Task failed")


class _TestGenObjectImpl:

    def __init__(self, node):
        self.node = node
        self.status_type = self.node.GetStructureType(
            "experimental.testing.companion.test_task_generator_py.TestGenStatus")

    def test_task_generator(self, done_time, fail_time, status_update_time, next_timeout, watchdog_timeout):
        return _TestTaskGenImpl(self.node, self.status_type, done_time, fail_time, status_update_time, next_timeout, watchdog_timeout)

    def test_sync_task_generator(self, done_time, fail_time, next_timeout, watchdog_timeout):
        return SyncTestTaskGenImpl(self.node, self.status_type, done_time, fail_time, next_timeout, watchdog_timeout)


class TaskGenTestFixture:

    def __init__(self):
        self.fixture = IntraTaskFixture()
        self.fixture.register_standard_service_types()
        self.fixture.register_service_types_text([robdef_text])

        self.test_gen_obj = _TestGenObjectImpl(self.fixture.server_node)

        self.fixture.register_service(
            "test_gen", "experimental.testing.companion.test_task_generator_py.TestGenObject", self.test_gen_obj)

        self.test_gen_obj_client = self.fixture.connect_service("rr+intra:///?nodename=server_node&service=test_gen")

        self.action_const = self.fixture.client_node.GetConstants("com.robotraconteur.action", self.test_gen_obj_client)

    def test_task_generator(self, done_time, fail_time, status_update_time, next_timeout, watchdog_timeout):
        return self.test_gen_obj_client.test_task_generator(done_time, fail_time, status_update_time, next_timeout, watchdog_timeout)

    def test_sync_task_generator(self, done_time, fail_time, next_timeout, watchdog_timeout):
        return self.test_gen_obj_client.test_sync_task_generator(done_time, fail_time, next_timeout, watchdog_timeout)


def run_task_gen_test(done_time, fail_time, status_update_time, next_timeout, watchdog_timeout, next_delay):
    fixture = TaskGenTestFixture()
    gen = fixture.test_gen_obj_client.test_task_generator(
        done_time, fail_time, status_update_time, next_timeout, watchdog_timeout)

    res = False
    while True:
        res, status = gen.TryNext()
        if res:
            print("Status: " + status.message)
        if res and next_delay > 0:
            time.sleep(next_delay)
        if not res:
            break


def run_task_gen_test_status_update():
    fixture = TaskGenTestFixture()
    gen = fixture.test_gen_obj_client.test_task_generator(.200, 2.000, .050, 2.000, 2.100)

    res, status = gen.TryNext()
    assert res
    res, status = gen.TryNext()
    assert res
    assert status.action_status == fixture.action_const["ActionStatusCode"]["running"]
    res, status = gen.TryNext()
    assert res
    assert status.action_status == fixture.action_const["ActionStatusCode"]["complete"]
    res, status = gen.TryNext()
    assert not res


def run_task_gen_test_status_update2():
    fixture = TaskGenTestFixture()
    gen = fixture.test_gen_obj_client.test_task_generator(.200, 2.000, .050, 2.000, 2.100)

    res, status = gen.TryNext()
    assert res
    time.sleep(0.1)
    res, status = gen.TryNext()
    assert res
    assert status.action_status == fixture.action_const["ActionStatusCode"]["running"]
    res, status = gen.TryNext()
    assert res
    assert status.action_status == fixture.action_const["ActionStatusCode"]["complete"]
    res, status = gen.TryNext()
    assert not res


def run_sync_task_gen_test(done_time, fail_time, next_timeout, watchdog_timeout, next_delay):
    fixture = TaskGenTestFixture()
    gen = fixture.test_gen_obj_client.test_sync_task_generator(done_time, fail_time, next_timeout, watchdog_timeout)

    res = False
    while True:
        res, status = gen.TryNext()
        if res:
            print("Status: " + status.message)
        if not res:
            break
        if res and next_delay > 0:
            time.sleep(next_delay)


def test_async_task_generator():

    with pytest.raises(RR.OperationAbortedException):
        run_task_gen_test(1.000, 2.000, 5.000, .010, 0.150, 0.200)
    with pytest.raises(RR.OperationFailedException):
        run_task_gen_test(1.000, .300, 5.000, .500, 2.000, 0)
    with pytest.raises(RR.OperationFailedException):
        run_task_gen_test(1.000, .100, 5.000, .010, 2.000, .200)
    run_task_gen_test(.100, 1.000, 5.000, 1.000, -1, 0)
    run_task_gen_test(.200, 1.000, 5.000, 0.010, -1, 1.200)
    run_task_gen_test(1.000, 2.000, 5.000, .010, -1, 1)
    run_task_gen_test(2.000, 5.000, 5.000, .050, .200, .025)
    run_task_gen_test_status_update()
    run_task_gen_test_status_update2()


def test_sync_task_generator():
    with pytest.raises(RR.OperationAbortedException):
        run_sync_task_gen_test(1.000, 2.000, .010, .150, .200)
    with pytest.raises(RR.OperationFailedException):
        run_sync_task_gen_test(1.000, .300, .500, 2.000, 0)
    with pytest.raises(RR.OperationFailedException):
        run_sync_task_gen_test(1.000, .100, .010, 2.000, .200)
    run_sync_task_gen_test(.100, 1.000, 1.000, -1, 0)
    run_sync_task_gen_test(.200, 1.000, .010, -1, 1.200)
    run_sync_task_gen_test(1.000, 2.000, .010, -1, 1)
    run_sync_task_gen_test(2.000, 5.000, .050, .200, .025)
