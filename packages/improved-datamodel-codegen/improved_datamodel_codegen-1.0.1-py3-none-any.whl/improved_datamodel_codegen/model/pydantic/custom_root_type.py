from typing import ClassVar

from improved_datamodel_codegen.model.pydantic.base_model import BaseModel


class CustomRootType(BaseModel):
    TEMPLATE_FILE_PATH: ClassVar[str] = 'pydantic/BaseModel_root.jinja2'
    BASE_CLASS: ClassVar[str] = 'pydantic.BaseModel'
