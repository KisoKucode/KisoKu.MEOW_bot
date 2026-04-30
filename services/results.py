from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, Optional, TypeVar

T = TypeVar('T')

@dataclass
class ServiceResult(Generic[T]):
    success: bool
    data: Optional[T] = None
    error: Optional[str] = None

    @classmethod
    def ok(cls, data: Optional[T] = None) -> ServiceResult[T]:
        return cls(success=True, data=data)

    @classmethod
    def fail(cls, error: str) -> ServiceResult[T]:
        return cls(success=False, error=error)
