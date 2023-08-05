from pyevsim.behavior_model_executor import BehaviorModelExecutor
from pyevsim.system_simulator import SysExecutor
from pyevsim.definition import *

from worker import WorkerModel
from worker_remove import WorkerRemoveModel
from worker_flush import WorkerFlushModel
from telegram_manager import TelegramManagerModel

from instance.config import *

import pymongo

class ModelManager():
    def __init__(self, inst_t, dest_t, mname, ename, engine:SysExecutor, tmanager:TelegramManagerModel):
        self.engine = engine
        self.tele_manager = tmanager

        self.worker_remove_model = WorkerRemoveModel(inst_t, dest_t, mname, ename, self)
        self.worker_flush_model = WorkerFlushModel(inst_t, dest_t, WorkerFlushConfig.model_name, ename)
        
        #self.db_url = f"mongodb://{DBConfig.ip}:{DBConfig.port}@{DBConfig.pwd}"
        self.db_url = f"mongodb://{DBConfig.ip}:{DBConfig.port}"
        
        self.human_info_db = pymongo.MongoClient(self.db_url)[DBConfig.human_db_name]
        self.site_info_db = pymongo.MongoClient(self.db_url)[DBConfig.site_db_name]
        
        self.engine.register_entity(self.worker_flush_model)
        self.engine.register_entity(self.worker_remove_model)

        self.worker_info_map = {}

    def check_worker_in_map(self, human_id) -> bool:
        if human_id in self.worker_info_map:
            return True
        
        else: return False

    def insert_worker(self, human_id):
        human_info = self.human_info_db[DBConfig.human_info_collection].find_one({'human_id':human_id})
        worker_model = WorkerModel(0, Infinite, human_info['human_id'], self.engine.get_name(), human_info)
        self.worker_info_map[human_info['human_id']] = worker_model
        
        #self.engine.insert_input_port(self.model_name)
        self.engine.register_entity(worker_model)

        # coupling relation 
        self.engine.coupling_relation(worker_model, human_info['human_id'], self.worker_remove_model, "remove_worker")
        self.engine.coupling_relation(worker_model, 'msg', self.tele_manager, 'alert')


        self.engine.coupling_relation(worker_model, "health_info", self.worker_flush_model, "health_info")
        self.engine.coupling_relation(worker_model, human_info['human_id'], self.worker_flush_model, "flush")
        pass

    def remove_worker(self, human_info):
        self.human_info_db[DBConfig.human_info_collection].update_one({'human_id':human_info['human_id']}, {'$set':human_info})
        self.engine.remove_entity(human_info['human_id'])
        del self.worker_info_map[human_info['human_id']]

        pass