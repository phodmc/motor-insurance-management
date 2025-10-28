import sqlalchemy as sa
import sqlalchemy.orm as so
from app import app, db
from app.models import (
    User,
    Participant,
    Policy,
    Vehicle,
    ParticipantGender,
    TransactionBranch,
    TransactionType,
    CoverageType,
    PolicyStatus,
)


@app.shell_context_processor
def make_shell_context():
    return dict(
        app=app,
        db=db,
        User=User,
        Participant=Participant,
        Policy=Policy,
        Vehicle=Vehicle,
        ParticipantGender=ParticipantGender,
        TransactionBranch=TransactionBranch,
        TransactionType=TransactionType,
        CoverageType=CoverageType,
        PolicyStatus=PolicyStatus,
    )
