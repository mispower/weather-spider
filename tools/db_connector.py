# -*- coding: utf-8 -*-
from pymongo import MongoClient, IndexModel, HASHED, ASCENDING, GEOSPHERE
from pymongo.database import Database
from pymongo.collection import Collection
from abc import abstractmethod

HISTORY_COLLECTION_NAME = "weather_history"
BASIC_COLLECTION_NAME = "weather_basic"


class AutoBasicCollection:
    def __init__(self):
        self.__conn = MongoClient("10.10.11.75", 27017)
        self.__authorized_database = self.__conn.get_database("basicdata")
        self.__authorized_database.authenticate("basicdata_write", "basicdata_write")
        self.__coll = self._get_create_collection(self.__authorized_database)

    @abstractmethod
    def _get_create_collection(self, authorized_database: Database)->Collection: pass

    @property
    def collection(self) -> Collection:
        return self.__coll

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__conn.close()


class WeatherBasicCollection(AutoBasicCollection):
    def __init__(self):
        super().__init__()

    def _get_create_collection(self, authorized_database: Database):
        if BASIC_COLLECTION_NAME not in authorized_database.list_collection_names():
            coll_create = authorized_database.get_collection(BASIC_COLLECTION_NAME)
            coll_create.create_indexes([
                IndexModel([("weather_code", ASCENDING)], unique=True),
                IndexModel([("gps_info", GEOSPHERE)])
            ])
        return authorized_database.get_collection(BASIC_COLLECTION_NAME)


class WeatherHistoryCollection(AutoBasicCollection):
    def __init__(self):
        super().__init__()

    def _get_create_collection(self, authorized_database: Database):
        if HISTORY_COLLECTION_NAME not in authorized_database.list_collection_names():
            coll_create = authorized_database.get_collection(HISTORY_COLLECTION_NAME)
            coll_create.create_indexes([
                IndexModel([("weather_code", HASHED)]),
                IndexModel([
                    ("datetime", ASCENDING),
                    ("weather_code", ASCENDING)
                ], unique=True),
            ])
        return authorized_database.get_collection(HISTORY_COLLECTION_NAME)
