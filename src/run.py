from __future__ import annotations
import time
import json
from lock import ModuleLock, ModuleData
from module_api.API.runnable import \
    Runnable, \
    create, \
    default_run
from module_api.API.error import ErrorBuffer
from module_api.API.backend import \
    TokenAPI, \
    NotificationAPI, \
    ModuleAPI
import module_api.API.lock as Lock
from module_api.API.display import Display
from module_api.API.display.components import \
    v1_ComponentWithoutTable

class ModuleRunnable(Runnable[ModuleLock]):
    lock_type = ModuleLock
    def init(self):
        module_id = self.lock.header.module_id.get()
        self.token_api = TokenAPI(module_id)
        self.notification_api = NotificationAPI(module_id)
        self.module_api = ModuleAPI(module_id, ModuleData)
        self.error_buffer = ErrorBuffer(self.lock)
        self.display = self.create_display()
        # This piece of code is used to initialize the runnable

    def re_init(self):
        module_id = self.lock.header.module_id.get()
        self.token_api = TokenAPI(module_id)
        self.notification_api = NotificationAPI(module_id)
        self.module_api = ModuleAPI(module_id, ModuleData)
        self.error_buffer = ErrorBuffer(self.lock)
        self.display = self.create_display()
        # This piece of code is used to re-initialize the runnable if it has
        # been stopped before.

    def create_display(self):
        display = Display(
            self.lock,
            v1_ComponentWithoutTable(
                messages  = ["Hello World"]
            )
        )
        return display
    
    def modify_display(self,display):
        display_obj = display.get()
        messages = display_obj['component']['messages']
        messages.append("Hello World")
        display.set(
            component = {
                'messages': messages
            }
        )
        display.save()
        return
        
    def run(self):
        self.lock.change_status('RUNNING')

        while self.lock.status.status.get() != "STOP":
            print("Hello World")
            self.modify_display(self.display)
            self.lock.reload()
            time.sleep(5)
        # Code to run the module
        

    def stop(self):
        self.lock.change_status('STOP')
        # What to do when the module is stopped


if __name__ == '__main__':
    runnable = create(ModuleRunnable)
    default_run(runnable)