from dataclasses import dataclass
from typing import Optional, Any, List


@dataclass
class Transformation:

    name: Optional[str] = None
    description: Optional[str] = None
    default: Optional[Any] = None


class Mapper:

    _path = None

    _map = {}

    @classmethod
    def parse(cls, data):
        return [cls.transform(item) for item in data[cls._path]]

    @classmethod
    def transform(cls, data):
        extract = {}
        for path, transformation in cls._map.items():
            value = data.get(path, transformation.default)
            name = transformation.name
            if not name:
                name = path.split('.')[-1]
            extract[name] = value
        return extract

    @classmethod
    def fieldnames(cls) -> List[str]:
        fieldnames = []
        for path, transformation in cls._map.items():
            name = transformation.name
            if not name:
                name = path.split('.')[-1]
            fieldnames.append(name)
        return fieldnames
