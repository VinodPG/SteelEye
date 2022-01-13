from databases import Database
import sqlalchemy

DATABASE_URL="sqlite:///test.db"
database = Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

trades = sqlalchemy.Table(
    "trade",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("asset_class", sqlalchemy.String),
    sqlalchemy.Column("counterparty", sqlalchemy.String),
    sqlalchemy.Column("instrument_id", sqlalchemy.String),
    sqlalchemy.Column("instrument_name", sqlalchemy.String),
    sqlalchemy.Column("trade_date_time", sqlalchemy.String),
    sqlalchemy.Column("buySellIndicator", sqlalchemy.String),
    sqlalchemy.Column("price", sqlalchemy.Float),
    sqlalchemy.Column("quantity", sqlalchemy.Integer),
    sqlalchemy.Column("trade_id", sqlalchemy.String),
    sqlalchemy.Column("trader", sqlalchemy.String)
)


engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)
