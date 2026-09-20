from __future__ import annotations

import uuid

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base
from app.models.base import UUIDPrimaryKeyMixin


class UserSiteAssignment(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "user_site_assignments"
    __table_args__ = (
        UniqueConstraint("user_id", "mine_site_id", name="user_site_assignments_unique"),
    )

    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    mine_site_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("mine_sites.id", ondelete="CASCADE"),
        nullable=False,
    )
