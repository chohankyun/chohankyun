# -*- coding: utf-8 -*-
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.messages.storage.base import Message


class MessageStorage(FallbackStorage):
    def add(self, level, message, extra_tags=''):
        obj_message = Message(level, message, extra_tags)
        if obj_message in self._loaded_messages:
            self._loaded_messages.remove(obj_message)
        super(MessageStorage, self).add(level, message, extra_tags='')
