class DynamicImport:
    def __init__(self, module_prefix, module_name):
        self.module_name = module_name
        # __import__ method used to fetch module
        self.module = __import__(module_prefix + '.' + module_name,
                                 fromlist=[module_name])

    def load_class(self):
        sp = self.module_name.split("_")
        class_name = ""
        for key in sp:
            class_name = class_name + key.lower().capitalize()
        class_name = class_name + "Class"
        my_class = getattr(self.module, class_name)()
        return my_class
