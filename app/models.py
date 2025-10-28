from typing import Optional
import enum
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db

from datetime import datetime, timezone


class UserType(enum.Enum):
    UNDERWRITER = "underwriter"
    CASHIER = "cashier"
    MANAGER = "manager"
    ADMIN = "admin"


class ParticipantGender(enum.Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class PolicyStatus(enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    EXPIRED = "expired"
    CANCELLED = "cancelled"


class RiskType(enum.Enum):
    MOTOR = "motor"
    TRAVEL = "travel"
    MEDICAL = "medical"


class UsageType(enum.Enum):
    PRIVATE = "private"
    COMMERCIAL = "commercial"


class CoverageType(enum.Enum):
    THIRD_PARTY = "third_party"
    COMPREHENSIVE = "comprehensive"


class TransactionType(enum.Enum):
    NEW_BUSINESS = "new_business"
    RENEWAL = "renewal"
    CANCELLATION = "cancellation"
    CLAIM = "claim"
    PAYMENT = "payment"
    REFUND = "refund"
    OTHER = "other"


class TransactionBranch(enum.Enum):
    KAIRABA = "kairaba"
    BRUSUBI = "brusubi"
    TALLINDING = "tallinding"
    BANJUL = "banjul"
    BRIKAMA = "brikama"
    SERREKUNDA = "serrekunda"
    COASTAL_ROAD = "coastal_road"


class User(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    first_name: so.Mapped[str] = so.mapped_column(sa.String(32), index=True)
    last_name: so.Mapped[str] = so.mapped_column(sa.String(32), index=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(128), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    user_type: so.Mapped[UserType] = so.mapped_column(
        sa.Enum(UserType), default=UserType.UNDERWRITER
    )
    policies: so.WriteOnlyMapped["Policy"] = so.relationship(
        back_populates="created_by"
    )

    def __repr__(self):
        return f"<User {self.username}>"


class Participant(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    first_name: so.Mapped[str] = so.mapped_column(sa.String(32), index=True)
    last_name: so.Mapped[str] = so.mapped_column(sa.String(32), index=True)
    email: so.Mapped[Optional[str]] = so.mapped_column(
        sa.String(128), index=True, unique=True
    )
    gender: so.Mapped[ParticipantGender] = so.mapped_column(
        sa.Enum(ParticipantGender), default=ParticipantGender.OTHER
    )
    age: so.Mapped[int] = so.mapped_column(sa.Integer, default=0)
    phone: so.Mapped[str] = so.mapped_column(sa.String(16), default="")
    address: so.Mapped[str] = so.mapped_column(sa.String(128), default="")
    nationality: so.Mapped[str] = so.mapped_column(sa.String(32), default="")
    occupation: so.Mapped[str] = so.mapped_column(sa.String(64), default="")
    vehicles: so.WriteOnlyMapped["Vehicle"] = so.relationship(back_populates="owner")

    def __repr__(self):
        return f"<Participant {self.email}>"


class Vehicle(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    make: so.Mapped[str] = so.mapped_column(sa.String(32), index=True)
    model: so.Mapped[str] = so.mapped_column(sa.String(32), index=True)
    year: so.Mapped[int] = so.mapped_column(sa.Integer, default=0)
    color: so.Mapped[str] = so.mapped_column(sa.String(32), default="")
    license_plate: so.Mapped[str] = so.mapped_column(sa.String(16), default="")
    owner_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey(Participant.id), nullable=False
    )
    owner: so.Mapped[Participant] = so.relationship(back_populates="vehicles")
    policies: so.WriteOnlyMapped["Policy"] = so.relationship(back_populates="vehicle")

    def __repr__(self):
        return f"<Vehicle {self.license_plate}>"


class Policy(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    # risk_type
    # usage_type
    # coverage_type
    # transaction_type
    # transaction_branch
    start_date: so.Mapped[datetime.date] = so.mapped_column(
        sa.Date, default=datetime.date.today()
    )
    end_date: so.Mapped[datetime.date] = so.mapped_column(
        sa.Date, default=datetime.date.today() + datetime.timedelta(days=365)
    )
    premium: so.Mapped[float] = so.mapped_column(sa.Float, default=0.0)
    status: so.Mapped[PolicyStatus] = so.mapped_column(
        sa.Enum(PolicyStatus), default=PolicyStatus.ACTIVE
    )
    # participant_id: so.Mapped[int] = so.mapped_column(
    #     sa.ForeignKey("participant.id"), nullable=False
    # )
    # participant: so.Mapped[Participant] = so.relationship(
    #     "Participant", back_populates="policies"
    # )
    vehicle_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey(Vehicle.id), nullable=False
    )
    vehicle: so.Mapped[Vehicle] = so.relationship("Vehicle", back_populates="policies")

    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), nullable=False)
    created_by: so.Mapped[User] = so.relationship("User", back_populates="policies")

    def __repr__(self):
        return f"<Policy {self.id}>"
