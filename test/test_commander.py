"""
Tests brewblox_devcon_spark.commander
"""

import asyncio
from datetime import timedelta
from unittest.mock import PropertyMock

import pytest
from asynctest import CoroutineMock
from brewblox_service import scheduler

from brewblox_devcon_spark import commander, commands, exceptions

TESTED = commander.__name__


@pytest.fixture
def reset_msgid():
    commands.Command._msgid = 0


@pytest.fixture
def conduit_mock(mocker):
    m = mocker.patch(TESTED + '.communication.get_conduit')
    m.return_value.bind = CoroutineMock()
    m.return_value.write = CoroutineMock()
    return m.return_value


@pytest.fixture
def app(app, conduit_mock, mocker):
    mocker.patch(TESTED + '.REQUEST_TIMEOUT', timedelta(seconds=1))
    scheduler.setup(app)
    commander.setup(app)
    return app


@pytest.fixture
async def sparky(app, client):
    return commander.get_commander(app)


async def test_init(conduit_mock, app, client):
    spock = commander.SparkCommander(app)

    await spock.shutdown()
    await spock.startup(app)
    await spock.shutdown()
    await spock.shutdown()

    assert str(spock)


async def test_on_data(conduit_mock, sparky):
    assert len(sparky._requests) == 0

    await sparky._on_data(conduit_mock, '05 00 |00 00 00 00')
    await asyncio.sleep(0.0001)
    assert len(sparky._requests) == 1
    assert sparky._requests['0500'].queue.qsize() == 1


async def test_on_data_error(mocker, conduit_mock, sparky):
    logger_mock = mocker.spy(commander, 'LOGGER')

    # No response pipe
    await sparky._on_data(conduit_mock, '1234')
    assert len(sparky._requests) == 0
    assert logger_mock.error.call_count == 1

    # Valid hex, not an opcode
    # process_response does not validate - it will be cleaned up later
    await sparky._on_data(conduit_mock, 'BB|AA')
    assert len(sparky._requests) == 1
    assert logger_mock.error.call_count == 1


async def test_on_event(mocker, conduit_mock, sparky):
    logger_mock = mocker.spy(commander, 'LOGGER')
    await sparky._on_event(conduit_mock, 'hello')
    assert logger_mock.info.call_count == 1


async def test_command(conduit_mock, sparky, reset_msgid):
    await sparky._on_data(conduit_mock, '01 00 07 28 | 00 00 00')

    command = commands.ListStoredObjectsCommand.from_args()
    v = command.encoded_request
    print(v)
    resp = await sparky.execute(command)
    assert resp['objects'] == []

    conduit_mock.write.assert_called_once_with('01000728')


async def test_error_command(conduit_mock, sparky, reset_msgid):
    command = commands.ListStoredObjectsCommand.from_args()
    await sparky._on_data(conduit_mock, '01 00 07 28 | FF 00 ')

    with pytest.raises(exceptions.CommandException):
        await sparky.execute(command)


async def test_timeout_command(conduit_mock, sparky, mocker):
    mocker.patch(TESTED + '.REQUEST_TIMEOUT', timedelta(microseconds=1))
    with pytest.raises(exceptions.CommandTimeout):
        await sparky.execute(commands.ListStoredObjectsCommand.from_args())


async def test_stale_reply(conduit_mock, sparky, reset_msgid):
    # error code
    stale = commander.TimestampedResponse('ff0000')
    stale._timestamp -= timedelta(minutes=1)
    fresh = commander.TimestampedResponse('000000')

    q = sparky._requests['01000728'].queue
    await q.put(stale)
    await q.put(fresh)

    command = commands.ListStoredObjectsCommand.from_args()
    assert await sparky.execute(command)


async def test_timestamped_queue():
    q = commander.TimestampedQueue()
    assert q.fresh

    q._timestamp -= 2*commander.QUEUE_VALID_DURATION
    assert not q.fresh

    # retrieving the queue should reset timestamp
    assert q.queue.empty()
    assert q.fresh


async def test_timestamped_response():
    res = commander.TimestampedResponse('data')
    assert res.fresh

    res._timestamp -= 2*commander.RESPONSE_VALID_DURATION
    assert not res.fresh

    # retrieving data does not reset timestamp
    assert res.content == 'data'
    assert not res.fresh


async def test_queue_cleanup(mocker, conduit_mock, sparky, app):
    mocker.patch(TESTED + '.CLEANUP_INTERVAL', timedelta(milliseconds=10))
    fresh_mock = PropertyMock(return_value=True)
    type(commander.TimestampedQueue()).fresh = fresh_mock

    await sparky.startup(app)
    await sparky._on_data(conduit_mock, '05 00 |00 00 00')

    # Still fresh
    await asyncio.sleep(0.1)
    assert len(sparky._requests) == 1

    # Assert stale was removed
    fresh_mock.return_value = False
    await asyncio.sleep(0.1)
    assert len(sparky._requests) == 0


async def test_queue_cleanup_error(mocker, sparky, app):
    mocker.patch(TESTED + '.CLEANUP_INTERVAL', timedelta(milliseconds=10))
    warning_spy = mocker.spy(commander, 'warnings')

    # Trigger an error
    sparky._requests = None

    await sparky.startup(app)
    await asyncio.sleep(0.1)
    assert warning_spy.warn.call_count > 0
    assert not sparky._cleanup_task.done()
