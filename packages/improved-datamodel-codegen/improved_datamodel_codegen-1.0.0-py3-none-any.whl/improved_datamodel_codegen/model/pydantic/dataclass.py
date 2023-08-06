from typing import ClassVar, Tuple

from improved_datamodel_codegen.imports import Import
from improved_datamodel_codegen.model import DataModel
from improved_datamodel_codegen.model.pydantic.imports import IMPORT_DATACLASS


class DataClass(DataModel):
    TEMPLATE_FILE_PATH: ClassVar[str] = 'pydantic/dataclass.jinja2'
    DEFAULT_IMPORTS: ClassVar[Tuple[Import, ...]] = (IMPORT_DATACLASS,)
