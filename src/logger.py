class Logger:
    def __init__(self, groups=None, auto_groups=None):
        self.groups = groups
        self.auto_groups = auto_groups
        assert groups is not None or auto_groups is not None
        self.object_ids = dict()
        self.reset()
    
    def reset(self):
        self.history = dict()
    
    def get_auto_group_name(self, object):
        for group_name, type in self.auto_groups.items():
            if isinstance(object, type):
                return group_name
        
        print("WARNING: No group name for type '%s', discarding logs" % (type(object).__name__))
        return None

    def get_auto_object_id(self, object, group_name):
        if group_name not in self.object_ids: self.object_ids[group_name] = list()
        if hash(object) not in self.object_ids[group_name]: self.object_ids[group_name].append(hash(object))

        return self.object_ids[group_name].index(hash(object))
    
    def get_object_history(self, object):
        assert self.groups is not None
        for group, objects in self.groups.items():
            if object in objects:
                id = objects.index(object)
                return self.history[group][id]

    def __call__(self, object, values, t):
        group_name = None
        id = None
        if self.auto_groups is not None:
            group_name = self.get_auto_group_name(object)
            if group_name is None:
                return
            id = self.get_auto_object_id(object, group_name)
        else:
            for group, objects in self.groups.items():
                if object in objects:
                    group_name = group
                    id = objects.index(object)
        
        assert group_name is not None and id is not None

        if group_name not in self.history: self.history[group_name] = dict()
        if id not in self.history[group_name]: self.history[group_name][id] = dict()

        for key, value in values.items():
            if key not in self.history[group_name][id]: self.history[group_name][id][key] = list()
            self.history[group_name][id][key].append(dict(time=t, value=value))