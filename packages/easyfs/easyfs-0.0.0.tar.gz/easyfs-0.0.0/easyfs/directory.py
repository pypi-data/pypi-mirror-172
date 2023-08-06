from ast import Str

from typing import Any, Dict, Iterator, Mapping, Optional, Union
from uuid import uuid4
from fsspec.implementations.dirfs import DirFileSystem
from fsspec.implementations.memory import MemoryFileSystem


import tempfile
import fsspec
from easyfs.file import File
import os
from collections.abc import MutableMapping

_memfs = MemoryFileSystem()


class Directory(MutableMapping):
    def __init__(
        self,
        objects: Optional[Mapping[str, Union[bytes, File, "Directory"]]] = None,
        root_subdir: Optional[str] = None,
        allow_override: bool = True,
    ) -> None:
        if root_subdir is None:
            self.id = str(uuid4())
        else:
            self.id = root_subdir

        self.allow_override = allow_override
        self.fs = DirFileSystem(self.id, _memfs)
        self.fs_map = fsspec.get_mapper(f"memory://{self.id}")
        if objects is not None:
            for key, obj in objects.items():
                self[key] = obj

    def create(self, path: str) -> None:
        local_mapper = fsspec.get_mapper(f"file://{path}")
        for k, v in self.as_dict().items():
            local_mapper[k] = v

    def clone(self) -> "Directory":
        return Directory(root_subdir=None, objects=self.as_dict())

    def as_dict(self) -> Dict[str, bytes]:
        return dict(self.fs_map)

    def __setitem__(self, key: str, value: Union[File, "Directory", bytes]):
        """Store value in key"""
        if isinstance(value, bytes):
            value = File(value)

        if isinstance(value, File):
            if key == ".":
                raise ValueError(f"not allowed file name: {key}")

            if not self.allow_override and key in self:
                raise ValueError(f"already exists: {key}")

            self.fs_map[key] = value.content
        elif isinstance(value, Directory):
            for k, val in fsspec.get_mapper(f"memory://{value.id}").items():
                if key == ".":
                    cur_key = k
                else:
                    cur_key = os.path.join(key, k)
                if not self.allow_override and cur_key in self:
                    raise ValueError(f"already exists: {cur_key}")
                self.fs_map[cur_key] = val

    def __getitem__(self, key: str, default=None):
        if key == ".":
            key = "/"
        value = self.fs_map.get(key, default)
        if isinstance(value, bytes):
            return File(content=value)
        elif value is None:
            return Directory(root_subdir=os.path.join(self.id, key))

    def __len__(self) -> int:
        return self.fs_map.__len__()

    def __delitem__(self, key: str) -> None:
        return self.fs_map.__delitem__(key)

    def __contains__(self, value: object) -> bool:
        return self.fs_map.__contains__(value)

    def __iter__(self) -> Iterator[Str]:
        return self.fs_map.__iter__()

    @classmethod
    def from_local(cls, path: str) -> "Directory":
        local_mapper = fsspec.get_mapper(f"file://{os.path.abspath(path)}")
        return cls(objects=local_mapper)

    @classmethod
    def from_cookiecutter(
        cls,
        template: str,
        config_file: Optional[str] = None,
        default_config: Optional[Dict[str, Any]] = None,
        extra_context: Optional[Dict[str, Any]] = None,
        directory: Optional[str] = None,
        password: Optional[str] = None,
    ) -> "Directory":
        try:
            from cookiecutter.cli import cookiecutter
        except ImportError:
            raise ValueError("cookiecutter is not installed")

        with tempfile.TemporaryDirectory() as temp_dir:
            cookiecutter(
                template=template,
                no_input=True,
                output_dir=temp_dir,
                config_file=config_file,
                default_config=default_config,
                directory=directory,
                extra_context=extra_context,
                password=password,
            )
            return cls.from_local(temp_dir)
