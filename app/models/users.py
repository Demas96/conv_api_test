import sqlalchemy
from sqlalchemy.dialects.postgresql import UUID


metadata = sqlalchemy.MetaData()


users_table = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(100)),
)


tokens_table = sqlalchemy.Table(
    "tokens",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column(
        "token",
        UUID(as_uuid=False),
        server_default=sqlalchemy.text("gen_random_uuid()"),
        unique=True,
        nullable=False,
        index=True,
    ),
    sqlalchemy.Column("expires", sqlalchemy.DateTime()),
    sqlalchemy.Column("user_id", sqlalchemy.ForeignKey("users.id")),
)


audio_table = sqlalchemy.Table(
    "audio",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(100)),
    sqlalchemy.Column(
            "token",
            UUID(as_uuid=False),
            server_default=sqlalchemy.text("gen_random_uuid()"),
            unique=True,
            nullable=False,
            index=True,
        ),
    sqlalchemy.Column("path", sqlalchemy.String),
    sqlalchemy.Column("user_id", sqlalchemy.ForeignKey("users.id")),
)