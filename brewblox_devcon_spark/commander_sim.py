"""
Monkey patches commander.SparkCommander to not require an actual connection.
"""

from copy import deepcopy

from aiohttp import web
from brewblox_service import features

from brewblox_devcon_spark import commander, commands
from brewblox_devcon_spark.commands import (OBJECT_DATA_KEY, OBJECT_ID_KEY,
                                            OBJECT_LIST_KEY, OBJECT_TYPE_KEY,
                                            PROFILE_LIST_KEY, SYSTEM_ID_KEY)


def setup(app: web.Application):
    # Register as a SparkCommander, so features.get(app, SparkCommander) still works
    features.add(app, SimulationCommander(app), key=commander.SparkCommander)


class SimulationResponder():

    def __init__(self):
        self._generators = {
            commands.ReadObjectCommand: self._read_object,
            commands.WriteObjectCommand: self._write_object,
            commands.CreateObjectCommand: self._create_object,
            commands.DeleteObjectCommand: self._delete_object,
            commands.ReadSystemObjectCommand: self._read_system_object,
            commands.WriteSystemObjectCommand: self._write_system_object,
            commands.ReadActiveProfilesCommand: self._read_active_profiles,
            commands.WriteActiveProfilesCommand: self._write_active_profiles,
            commands.ListActiveObjectsCommand: self._list_active_objects,
            commands.ListSavedObjectsCommand: self._list_saved_objects,
            commands.ListSystemObjectsCommand: self._list_system_objects,
            commands.ClearProfileCommand: self._clear_profile,
            commands.FactoryResetCommand: self._factory_reset,
            commands.RestartCommand: self._restart,
        }

        self._current_id = 1
        self._active_profiles = []

        self._system_objects = {
            2: {
                SYSTEM_ID_KEY: 2,
                OBJECT_TYPE_KEY: 256,
                # data: {'command':{}, 'address':['aa','bb']}
                OBJECT_DATA_KEY: b'\x08\n\x00\x12\x01\xaa\x12\x01\xbb'
            }
        }

        self._objects = {}

    def respond(self, command):
        func = self._generators[type(command)]
        retv = func(command.decoded_request)
        return retv if retv is not None else dict()

    def _next_controller_id(self):
        self._current_id += 1
        return self._current_id

    def _read_object(self, request):
        return deepcopy(self._objects[request[OBJECT_ID_KEY]])

    def _write_object(self, request):
        key = request[OBJECT_ID_KEY]
        if key not in self._objects:
            raise KeyError(f'{key} not found')

        self._objects[key] = deepcopy(request)
        return deepcopy(request)

    def _create_object(self, request):
        key = request.get(OBJECT_ID_KEY)
        obj = deepcopy(request)

        if not key:
            key = self._next_controller_id()
            obj[OBJECT_ID_KEY] = key
        elif key in self._objects:
            raise KeyError(f'Object {key} already exists')

        self._objects[key] = obj
        return deepcopy(obj)

    def _delete_object(self, request):
        key = request[OBJECT_ID_KEY]
        del self._objects[key]

    def _read_system_object(self, request):
        return deepcopy(self._system_objects[request[SYSTEM_ID_KEY]])

    def _write_system_object(self, request):
        key = request[SYSTEM_ID_KEY]
        if key not in self._system_objects:
            raise KeyError(f'{key} not found')

        self._system_objects[key] = deepcopy(request)
        return deepcopy(request)

    def _read_active_profiles(self, request):
        return {PROFILE_LIST_KEY: deepcopy(self._active_profiles)}

    def _write_active_profiles(self, request):
        self._active_profiles = deepcopy(request[PROFILE_LIST_KEY])
        return self._read_active_profiles(request)

    def _list_active_objects(self, request):
        return {
            OBJECT_LIST_KEY: [
                deepcopy(obj) for obj in self._objects.values()
                if set(obj[PROFILE_LIST_KEY]) & set(self._active_profiles)
            ]
        }

    def _list_saved_objects(self, request):
        return {OBJECT_LIST_KEY: [deepcopy(obj) for obj in self._objects.values()]}

    def _list_system_objects(self, request):
        return {OBJECT_LIST_KEY: [deepcopy(obj) for obj in self._system_objects.values()]}

    def _clear_profile(self, request):
        cleared_profiles = request[PROFILE_LIST_KEY]
        for obj in self._objects:
            obj_profiles = obj[PROFILE_LIST_KEY]
            obj[PROFILE_LIST_KEY] = [p for p in obj_profiles if p not in cleared_profiles]

    def _factory_reset(self, request):
        pass

    def _restart(self, request):
        pass


class SimulationCommander(commander.SparkCommander):

    def __init__(self, app: web.Application):
        super().__init__(app)
        self._responder = SimulationResponder()

    async def startup(self, _):
        pass

    async def shutdown(self, _):
        pass

    async def execute(self, command: commands.Command) -> dict:
        return self._responder.respond(command)
