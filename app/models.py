from typing import Optional
from werkzeug.security import generate_password_hash, check_password_hash
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

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

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
    risk_type: so.Mapped[RiskType] = so.mapped_column(sa.Enum(RiskType), nullable=False)
    # usage_type
    usage_type: so.Mapped[UsageType] = so.mapped_column(
        sa.Enum(UsageType), nullable=False
    )
    # coverage_type
    coverage_type: so.Mapped[CoverageType] = so.mapped_column(
        sa.Enum(CoverageType), nullable=False
    )
    # transaction_type
    transaction_type: so.Mapped[TransactionType] = so.mapped_column(
        sa.Enum(TransactionType), nullable=False
    )
    # transaction_branch
    transaction_branch: so.Mapped[TransactionBranch] = so.mapped_column(
        sa.Enum(TransactionBranch), nullable=False
    )

    start_date: so.Mapped[datetime.date] = so.mapped_column(
        sa.Date, default=lambda: datetime.date.today()
    )

    cover_period: so.Mapped[int] = so.mapped_column(sa.Integer, default=365)
    end_date: so.Mapped[datetime.date] = so.mapped_column(
        sa.Date,
        default=lambda: datetime.date.today()
        + datetime.timedelta(days=Policy.cover_period),
    )
    premium: so.Mapped[float] = so.mapped_column(sa.Float, default=0.0)
    status: so.Mapped[PolicyStatus] = so.mapped_column(
        sa.Enum(PolicyStatus), default=PolicyStatus.ACTIVE
    )

    vehicle_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey(Vehicle.id), nullable=False
    )
    vehicle: so.Mapped[Vehicle] = so.relationship("Vehicle", back_populates="policies")

    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), nullable=False)
    created_by: so.Mapped[User] = so.relationship("User", back_populates="policies")

    def __repr__(self):
        return f"<Policy {self.id}>"
