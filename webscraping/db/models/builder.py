import uuid
from sqlalchemy import ARRAY, String, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column  # type: ignore[attr-defined]
from sqlalchemy.dialects.postgresql import UUID
from webscraping.db.database import Base

# Keyboard Switches Table


class Switch(Base):  # type: ignore
    __tablename__ = "switches"

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True,
                                    default=uuid.uuid4)
    name: Mapped[str] = mapped_column(unique=False, nullable=False)
    price: Mapped[Numeric] = mapped_column(Numeric(10, 2), unique=False,
                                           nullable=True)
    manufacturer: Mapped[str] = mapped_column(unique=False, nullable=True)
    switch_type: Mapped[str] = mapped_column(unique=False, nullable=False)
    actuation_force: Mapped[Numeric] = mapped_column(Numeric(10, 2),
                                                     unique=False, 
                                                     nullable=True)
    travel_distance: Mapped[Numeric] = mapped_column(Numeric(10, 2),
                                                     unique=False,
                                                     nullable=True)
    vendor: Mapped[list[str]] = mapped_column(ARRAY(String), unique=False, 
                                              nullable=True)
    img_url: Mapped[str] = mapped_column(unique=False, nullable=True)
    availability: Mapped[bool] = mapped_column(unique=False, nullable=True)


# Keyboard Keycaps Table


class Keycap(Base):  # type: ignore
    __tablename__ = "keycaps"

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True,
                                    default=uuid.uuid4)
    name: Mapped[str] = mapped_column(unique=False, nullable=False)
    price: Mapped[Numeric] = mapped_column(Numeric(10, 2), unique=False,
                                           nullable=True)
    manufacturer: Mapped[str] = mapped_column(unique=False, nullable=True)
    vendor: Mapped[list[str]] = mapped_column(ARRAY(String), unique=False,
                                              nullable=True)
    colors: Mapped[list[str]] = mapped_column(ARRAY(String), unique=False,
                                              nullable=True)
    layout: Mapped[list[str]] = mapped_column(ARRAY(String), unique=False,
                                              nullable=True)
    material: Mapped[str] = mapped_column(unique=False, nullable=True)
    profile: Mapped[list[str]] = mapped_column(ARRAY(String), unique=False, 
                                               nullable=True)
    img_url: Mapped[str] = mapped_column(unique=False, nullable=True)
    availability: Mapped[bool] = mapped_column(unique=False, nullable=True)

# Keyboard Lubricants Table


class Lubricant(Base):  # type: ignore
    __tablename__ = "lubricants"

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(unique=False, nullable=False)
    price: Mapped[Numeric] = mapped_column(Numeric(10, 2), unique=False, nullable=True)
    img_url: Mapped[str] = mapped_column(unique=False, nullable=True)
    availability: Mapped[bool] = mapped_column(unique=False, nullable=True)

# Keyboard Kits Table


class Kits(Base):  # type: ignore
    __tablename__ = "kits"

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True,
                                    default=uuid.uuid4)
    name: Mapped[str] = mapped_column(unique=False, nullable=False)
    price: Mapped[Numeric] = mapped_column(Numeric(10, 2), unique=False,
                                           nullable=True)
    manufacturer: Mapped[str] = mapped_column(unique=False, nullable=True)
    vendor: Mapped[list[str]] = mapped_column(ARRAY(String), unique=False,
                                              nullable=True)

    layout_size: Mapped[list[str]] = mapped_column(ARRAY(String),
                                                   unique=False, 
                                                   nullable=True)
    layout_standard: Mapped[list[str]] = mapped_column(ARRAY(String),
                                                       unique=False, 
                                                       nullable=True)
    layout_ergonomic: Mapped[str] = mapped_column(unique=False, nullable=True)

    hotswappable: Mapped[bool] = mapped_column(unique=False, nullable=True)
    knob_support: Mapped[bool] = mapped_column(unique=False, nullable=True)
    rgb_support: Mapped[bool] = mapped_column(unique=False, nullable=True)
    display_support: Mapped[bool] = mapped_column(unique=False, nullable=True)

    connection: Mapped[list[str]] = mapped_column(ARRAY(String), unique=False,
                                                  nullable=True)
    mount_style: Mapped[str] = mapped_column(unique=False, nullable=True)
    material: Mapped[str] = mapped_column(unique=False, nullable=True)
    img_url: Mapped[str] = mapped_column(unique=False, nullable=True)
    availability: Mapped[bool] = mapped_column(unique=False, nullable=True)


class Builds(Base):  # type: ignore
    __tablename__ = "builds"

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    build_name: Mapped[str] = mapped_column(unique=False, nullable=True)
    kit_choice: Mapped[str] = mapped_column(unique=False, nullable=True)
    switch_choice: Mapped[str] = mapped_column(unique=False, nullable=True)
    keycap_choice: Mapped[str] = mapped_column(unique=False, nullable=True)
    lubricant_choice: Mapped[str] = mapped_column(unique=False, nullable=True)
