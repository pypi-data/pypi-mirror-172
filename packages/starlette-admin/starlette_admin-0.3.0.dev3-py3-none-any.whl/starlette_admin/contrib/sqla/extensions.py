from typing import Any, Dict, Optional, Type

from pydantic import ValidationError
from sqlmodel import SQLModel
from starlette.requests import Request
from starlette_admin.contrib.sqla.view import ModelView
from starlette_admin.fields import FileField
from starlette_admin.helpers import pydantic_error_to_form_validation_errors


class SQLModelView(ModelView):
    def __init__(
        self,
        model: Type[SQLModel],
        icon: Optional[str] = None,
        name: Optional[str] = None,
        label: Optional[str] = None,
        identity: Optional[str] = None,
    ):
        super().__init__(model, icon, name, label, identity)

    async def validate(self, request: Request, data: Dict[str, Any]) -> None:
        """Validate data without file fields"""
        fields_to_exclude = [f.name for f in self.fields if isinstance(f, FileField)]
        self.model.validate(
            {k: v for k, v in data.items() if k not in fields_to_exclude}
        )

    def handle_exception(self, exc: Exception) -> None:
        if isinstance(exc, ValidationError):
            raise pydantic_error_to_form_validation_errors(exc)
        return super().handle_exception(exc)  # pragma: no cover
