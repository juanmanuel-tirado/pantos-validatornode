"""initial_database_schema

Revision ID: 578d480b68dc
Revises: None
Create Date: 2023-03-06 10:27:01.447393

"""
import alembic
import sqlalchemy as sa  # type: ignore

# revision identifiers, used by Alembic.
revision = '578d480b68dc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    alembic.op.create_table(
        'blockchains', sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.Text(), nullable=False),
        sa.Column('last_block_number', sa.BigInteger(), nullable=False),
        sa.PrimaryKeyConstraint('id'))
    alembic.op.create_table('transfer_status',
                            sa.Column('id', sa.Integer(), nullable=False),
                            sa.Column('name', sa.Text(), nullable=False),
                            sa.PrimaryKeyConstraint('id'))
    alembic.op.create_table(
        'forwarder_contracts', sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('blockchain_id', sa.Integer(), nullable=False),
        sa.Column('address', sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(
            ['blockchain_id'],
            ['blockchains.id'],
        ), sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('blockchain_id', 'address'))
    alembic.op.create_table(
        'hub_contracts', sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('blockchain_id', sa.Integer(), nullable=False),
        sa.Column('address', sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(
            ['blockchain_id'],
            ['blockchains.id'],
        ), sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('blockchain_id', 'address'))
    alembic.op.create_table(
        'token_contracts', sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('blockchain_id', sa.Integer(), nullable=False),
        sa.Column('address', sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(
            ['blockchain_id'],
            ['blockchains.id'],
        ), sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('blockchain_id', 'address'))
    alembic.op.create_table(
        'transfers', sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('source_blockchain_id', sa.Integer(), nullable=False),
        sa.Column('destination_blockchain_id', sa.Integer(), nullable=False),
        sa.Column('sender_address', sa.Text(), nullable=False),
        sa.Column('recipient_address', sa.Text(), nullable=False),
        sa.Column('source_token_contract_id', sa.Integer(), nullable=False),
        sa.Column('destination_token_contract_id', sa.Integer(),
                  nullable=False),
        sa.Column('amount', sa.Numeric(precision=78, scale=0), nullable=False),
        sa.Column('validator_nonce', sa.Numeric(precision=78, scale=0),
                  nullable=True),
        sa.Column('source_hub_contract_id', sa.Integer(), nullable=False),
        sa.Column('destination_hub_contract_id', sa.Integer(), nullable=True),
        sa.Column('destination_forwarder_contract_id',
                  sa.Integer(), nullable=True),
        sa.Column('task_id', sa.Text(), nullable=True),
        sa.Column('source_transfer_id', sa.Numeric(precision=78, scale=0),
                  nullable=False),
        sa.Column('destination_transfer_id', sa.Numeric(precision=78, scale=0),
                  nullable=True),
        sa.Column('source_transaction_id', sa.Text(), nullable=False),
        sa.Column('destination_transaction_id', sa.Text(), nullable=True),
        sa.Column('source_block_number', sa.BigInteger(), nullable=False),
        sa.Column('destination_block_number', sa.BigInteger(), nullable=True),
        sa.Column('nonce', sa.BigInteger(), nullable=True),
        sa.Column('status_id', sa.Integer(), nullable=False),
        sa.Column('created', sa.DateTime(), nullable=False),
        sa.Column('updated', sa.DateTime(), nullable=True),
        sa.CheckConstraint(
            'source_blockchain_id != destination_blockchain_id'),
        sa.ForeignKeyConstraint(
            ['destination_blockchain_id'],
            ['blockchains.id'],
        ),
        sa.ForeignKeyConstraint(
            ['destination_forwarder_contract_id'],
            ['forwarder_contracts.id'],
        ),
        sa.ForeignKeyConstraint(
            ['destination_hub_contract_id'],
            ['hub_contracts.id'],
        ),
        sa.ForeignKeyConstraint(
            ['destination_token_contract_id'],
            ['token_contracts.id'],
        ),
        sa.ForeignKeyConstraint(
            ['source_blockchain_id'],
            ['blockchains.id'],
        ),
        sa.ForeignKeyConstraint(
            ['source_hub_contract_id'],
            ['hub_contracts.id'],
        ),
        sa.ForeignKeyConstraint(
            ['source_token_contract_id'],
            ['token_contracts.id'],
        ), sa.ForeignKeyConstraint(
            ['status_id'],
            ['transfer_status.id'],
        ), sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('destination_blockchain_id',
                            'destination_transaction_id'),
        sa.UniqueConstraint('destination_blockchain_id',
                            'destination_transfer_id'),
        sa.UniqueConstraint('destination_forwarder_contract_id',
                            'validator_nonce', name='unique_validator_nonce'),
        sa.UniqueConstraint('source_blockchain_id', 'source_transaction_id'),
        sa.UniqueConstraint('source_blockchain_id', 'source_transfer_id'),
        sa.UniqueConstraint('task_id'))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    alembic.op.drop_table('transfers')
    alembic.op.drop_table('token_contracts')
    alembic.op.drop_table('hub_contracts')
    alembic.op.drop_table('forwarder_contracts')
    alembic.op.drop_table('transfer_status')
    alembic.op.drop_table('blockchains')
    # ### end Alembic commands ###
