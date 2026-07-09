from dataclasses import dataclass, field
from typing import Dict, List

from vision.world.object_state import ObjectState


@dataclass
class WorldModel:

    objects: Dict[str, ObjectState] = field(default_factory=dict)

    timestamp: float = 0.0

    def add(self, obj):
        self.objects[obj.object_id] = obj

    def remove(self, object_id):
        self.objects.pop(object_id, None)

    def get(self, object_id):
        return self.objects.get(object_id)

    def all_objects(self):
        return list(self.objects.values())

    def category(self, category):
        return [
            obj
            for obj in self.objects.values()
            if obj.category == category
        ]
