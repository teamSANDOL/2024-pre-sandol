from collections import abc

class FacadeJSON:
    def __init__(self, mapping):
        self.__data = dict(mapping)

    def __getattr__(self, name):
        if hasattr(self.__data, name):
            return getattr(self.__data, name)
        else:
            return FacadeJSON.build(self.__data[name])

    @classmethod
    def build(cls, obj):
        if isinstance(obj, abc.Mapping):
            return cls(obj)
        elif isinstance(obj, abc.MutableSequence):
            return [cls.build(item) for item in obj]
        else:
            return obj

    def to_json(self):
        if isinstance(self.__data, abc.Mapping):
            return {key: value.to_json()
            if isinstance(value, FacadeJSON) else value for key, value in self.__data.items()}
        elif isinstance(self.__data, abc.MutableSequence):
            return [item.to_json() if isinstance(item, FacadeJSON) else item for item in self.__data]
        else:
            return self.__data

    def add(self, new_block):
        if isinstance(self.__data, dict) and 'template' in self.__data:
            template = self.__data['template']
            if isinstance(template, dict) and 'outputs' in template:
                outputs = template['outputs']
                if isinstance(outputs, list):
                    outputs.append(new_block)
                    return

        raise ValueError("Invalid structure for adding output")
