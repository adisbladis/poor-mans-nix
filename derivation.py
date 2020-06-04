from __future__ import annotations
from typing import Dict, List
import itertools
import libstore
import os.path
import inspect
import hashlib
import base64
import json


# STORE_PATH = "/haxx/store"
STORE_PATH = "haxx/store"


class BaseDerivation:

    def __init__(self):
        for attr, anno in self._attrs.items():
            if isinstance(anno, str) and anno.startswith("Optional"):
                continue
            if not hasattr(self, attr):
                raise ValueError(
                    f"Derivation '{self.__class__.__name__}' missing required attr '{attr}'"
                )

    def write_drv(self, name):
        drv_name = ".".join((name, "drv"))
        drv_path = os.path.join(
            STORE_PATH,
            drv_name,
        )
        libstore.write_drv(drv_path, dict(self))

    @property
    def _attrs(self) -> Dict:
        """Get required attributes from inheritance chain"""
        required_attrs = {}
        for cls in self.__class__.mro():
            if hasattr(cls, "__annotations__"):
                required_attrs.update(cls.__annotations__)
        return required_attrs

    def __iter__(self):
        def process_value(value):
            if inspect.isclass(value) and issubclass(value, BaseDerivation):
                return str(value())
            elif isinstance(value, list):
                return [process_value(v) for v in value]
            else:
                return value

        for attr in self._attrs:
            value = getattr(self, attr)
            yield (attr, process_value(value))


class Derivation(BaseDerivation):

    pname: str
    version: str
    build_inputs: List[Derivation]
    src: Optional[Derivation]

    def __init__(self):
        if not hasattr(self, "build_inputs"):
            self.build_inputs = []
        if not hasattr(self, "src"):
            self.src = None
        super().__init__()

    def __dict__(self):
        return {
            "pname": self.pname,
        }

    def __str__(self):
        m = hashlib.sha256()
        m.update(STORE_PATH.encode())
        m.update(self.pname.encode())
        m.update(self.version.encode())
        for i in self.build_inputs:
            m.update(str(i).encode())

        name = "-".join((m.hexdigest(), self.pname, self.version,))

        self.write_drv(name)

        return name


class FixedOutputDerivation(BaseDerivation):
    url: str
    sha256: str

    def __str__(self):
        name = "-".join((self.sha256, os.path.basename(self.url)))
        self.write_drv(name)
        return name
