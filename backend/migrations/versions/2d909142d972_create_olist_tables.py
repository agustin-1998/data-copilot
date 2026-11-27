"""create olist tables

Revision ID: 2d909142d972
Revises:
Create Date: 2026-11-27 18:20:16.510071

Tables mirror the Olist files (ADR 0003), with three changes: product
categories are stored in English, review comments are not stored, and
customers have synthetic personal data. No grants to the reader yet: that
is decided in its own ADR.
"""

from collections.abc import Sequence

from alembic import op

revision: str = "2d909142d972"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TABLE regions (
            state_code  char(2) PRIMARY KEY,
            state_name  text NOT NULL,
            region      text NOT NULL
        );

        CREATE TABLE customers (
            customer_id               text PRIMARY KEY,
            customer_unique_id        text NOT NULL,
            customer_zip_code_prefix  text NOT NULL,
            customer_city             text NOT NULL,
            customer_state            char(2) NOT NULL REFERENCES regions,
            customer_name             text NOT NULL,
            customer_email            text NOT NULL,
            customer_phone            text NOT NULL
        );
        COMMENT ON COLUMN customers.customer_name IS 'Personal data (synthetic).';
        COMMENT ON COLUMN customers.customer_email IS 'Personal data (synthetic).';
        COMMENT ON COLUMN customers.customer_phone IS 'Personal data (synthetic).';

        CREATE TABLE sellers (
            seller_id               text PRIMARY KEY,
            seller_zip_code_prefix  text NOT NULL,
            seller_city             text NOT NULL,
            seller_state            char(2) NOT NULL REFERENCES regions
        );

        CREATE TABLE products (
            product_id                  text PRIMARY KEY,
            product_category_name       text,
            product_name_length         integer,
            product_description_length  integer,
            product_photos_qty          integer,
            product_weight_g            integer,
            product_length_cm           integer,
            product_height_cm           integer,
            product_width_cm            integer
        );
        COMMENT ON COLUMN products.product_category_name IS 'Category in English.';

        CREATE TABLE orders (
            order_id                       text PRIMARY KEY,
            customer_id                    text NOT NULL REFERENCES customers,
            order_status                   text NOT NULL,
            order_purchase_timestamp       timestamp NOT NULL,
            order_approved_at              timestamp,
            order_delivered_carrier_date   timestamp,
            order_delivered_customer_date  timestamp,
            order_estimated_delivery_date  timestamp
        );

        CREATE TABLE order_items (
            order_id             text NOT NULL REFERENCES orders,
            order_item_id        integer NOT NULL,
            product_id           text NOT NULL REFERENCES products,
            seller_id            text NOT NULL REFERENCES sellers,
            shipping_limit_date  timestamp NOT NULL,
            price                numeric(10, 2) NOT NULL,
            freight_value        numeric(10, 2) NOT NULL,
            PRIMARY KEY (order_id, order_item_id)
        );

        CREATE TABLE order_payments (
            order_id              text NOT NULL REFERENCES orders,
            payment_sequential    integer NOT NULL,
            payment_type          text NOT NULL,
            payment_installments  integer NOT NULL,
            payment_value         numeric(10, 2) NOT NULL,
            PRIMARY KEY (order_id, payment_sequential)
        );

        -- review_id repeats across orders in the source, so the key is the pair.
        CREATE TABLE order_reviews (
            review_id                text NOT NULL,
            order_id                 text NOT NULL REFERENCES orders,
            review_score             smallint NOT NULL CHECK (review_score BETWEEN 1 AND 5),
            review_creation_date     timestamp NOT NULL,
            review_answer_timestamp  timestamp,
            PRIMARY KEY (review_id, order_id)
        );
        """
    )


def downgrade() -> None:
    op.execute(
        """
        DROP TABLE order_reviews;
        DROP TABLE order_payments;
        DROP TABLE order_items;
        DROP TABLE orders;
        DROP TABLE products;
        DROP TABLE sellers;
        DROP TABLE customers;
        DROP TABLE regions;
        """
    )
