"""Load the Olist dataset into PostgreSQL (ADR 0003).

Run from backend/:  uv run python -m data_copilot.seed

Idempotent: one transaction empties every table and loads it again, so
running it twice gives the same database and a failed run changes nothing.
"""

import csv
import hashlib
import io
import urllib.request
import zipfile
from collections.abc import Iterable, Iterator
from pathlib import Path

import psycopg
from faker import Faker

from data_copilot.config import OWNER_ROLE, REPO_ROOT, get_settings

DATASET_URL = (
    "https://github.com/agustin-1998/data-copilot/releases/download/"
    "data-olist-v1/olist-brazilian-ecommerce.zip"
)
DATASET_SHA256 = "967e41e04fc306fe604e2a693f488995a8b41e5047418f8a5c8e4abd6deca784"
DATASET_PATH = REPO_ROOT / "db" / "data" / "olist-brazilian-ecommerce.zip"

# Same seed, same fake people, every time.
FAKER_SEED = 42

# Categories that the dataset's translation table does not cover.
EXTRA_CATEGORY_TRANSLATIONS = {
    "pc_gamer": "pc_gamer",
    "portateis_cozinha_e_preparadores_de_alimentos": "kitchen_portables_and_food_preparers",
}

# Brazilian states and their regions.
REGIONS = [
    ("AC", "Acre", "North"),
    ("AL", "Alagoas", "Northeast"),
    ("AM", "Amazonas", "North"),
    ("AP", "Amapá", "North"),
    ("BA", "Bahia", "Northeast"),
    ("CE", "Ceará", "Northeast"),
    ("DF", "Distrito Federal", "Center-West"),
    ("ES", "Espírito Santo", "Southeast"),
    ("GO", "Goiás", "Center-West"),
    ("MA", "Maranhão", "Northeast"),
    ("MG", "Minas Gerais", "Southeast"),
    ("MS", "Mato Grosso do Sul", "Center-West"),
    ("MT", "Mato Grosso", "Center-West"),
    ("PA", "Pará", "North"),
    ("PB", "Paraíba", "Northeast"),
    ("PE", "Pernambuco", "Northeast"),
    ("PI", "Piauí", "Northeast"),
    ("PR", "Paraná", "South"),
    ("RJ", "Rio de Janeiro", "Southeast"),
    ("RN", "Rio Grande do Norte", "Northeast"),
    ("RO", "Rondônia", "North"),
    ("RR", "Roraima", "North"),
    ("RS", "Rio Grande do Sul", "South"),
    ("SC", "Santa Catarina", "South"),
    ("SE", "Sergipe", "Northeast"),
    ("SP", "São Paulo", "Southeast"),
    ("TO", "Tocantins", "North"),
]

# Load order respects the foreign keys.
TABLES = [
    "regions",
    "customers",
    "sellers",
    "products",
    "orders",
    "order_items",
    "order_payments",
    "order_reviews",
]


# --- Download -------------------------------------------------------------


def sha256_of(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for block in iter(lambda: file.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def verify_checksum(path: Path, expected: str = DATASET_SHA256) -> None:
    actual = sha256_of(path)
    if actual != expected:
        raise ValueError(f"Checksum mismatch for {path.name}: expected {expected}, got {actual}")


def ensure_dataset(path: Path = DATASET_PATH) -> Path:
    """Download the zip unless a verified copy is already there."""
    if path.exists():
        verify_checksum(path)
        return path

    path.parent.mkdir(parents=True, exist_ok=True)
    partial = path.with_suffix(".part")
    print(f"Downloading {DATASET_URL}")
    with urllib.request.urlopen(DATASET_URL, timeout=120) as response, partial.open("wb") as out:
        while block := response.read(1 << 20):
            out.write(block)
    try:
        verify_checksum(partial)
    except ValueError:
        partial.unlink()
        raise
    partial.rename(path)
    return path


# --- Reading and cleaning -------------------------------------------------


def read_csv(archive: zipfile.ZipFile, name: str) -> Iterator[dict[str, str]]:
    # utf-8-sig drops the byte order mark some of the files start with.
    with archive.open(name) as raw:
        yield from csv.DictReader(io.TextIOWrapper(raw, encoding="utf-8-sig", newline=""))


def text_or_none(value: str) -> str | None:
    return value or None


def int_or_none(value: str) -> int | None:
    # Some integer columns are written as "40.0" in the source.
    return int(float(value)) if value else None


def category_translations(archive: zipfile.ZipFile) -> dict[str, str]:
    rows = read_csv(archive, "product_category_name_translation.csv")
    translations = {row["product_category_name"]: row["product_category_name_english"] for row in rows}
    return translations | EXTRA_CATEGORY_TRANSLATIONS


def fake_identities(unique_ids: Iterable[str]) -> dict[str, tuple[str, str, str]]:
    """One fake (name, email, phone) per real person, always the same ones."""
    Faker.seed(FAKER_SEED)
    fake = Faker("pt_BR")
    # safe_email only uses example.com, example.net and example.org.
    return {uid: (fake.name(), fake.safe_email(), fake.phone_number()) for uid in sorted(set(unique_ids))}


def customer_rows(archive: zipfile.ZipFile) -> Iterator[tuple]:
    customers = list(read_csv(archive, "olist_customers_dataset.csv"))
    identities = fake_identities(row["customer_unique_id"] for row in customers)
    for row in customers:
        name, email, phone = identities[row["customer_unique_id"]]
        yield (
            row["customer_id"],
            row["customer_unique_id"],
            row["customer_zip_code_prefix"],
            row["customer_city"],
            row["customer_state"],
            name,
            email,
            phone,
        )


def seller_rows(archive: zipfile.ZipFile) -> Iterator[tuple]:
    for row in read_csv(archive, "olist_sellers_dataset.csv"):
        yield (row["seller_id"], row["seller_zip_code_prefix"], row["seller_city"], row["seller_state"])


def product_rows(archive: zipfile.ZipFile) -> Iterator[tuple]:
    translations = category_translations(archive)
    for row in read_csv(archive, "olist_products_dataset.csv"):
        category = row["product_category_name"]
        yield (
            row["product_id"],
            translations[category] if category else None,
            # The source spells "length" as "lenght".
            int_or_none(row["product_name_lenght"]),
            int_or_none(row["product_description_lenght"]),
            int_or_none(row["product_photos_qty"]),
            int_or_none(row["product_weight_g"]),
            int_or_none(row["product_length_cm"]),
            int_or_none(row["product_height_cm"]),
            int_or_none(row["product_width_cm"]),
        )


def order_rows(archive: zipfile.ZipFile) -> Iterator[tuple]:
    for row in read_csv(archive, "olist_orders_dataset.csv"):
        yield (
            row["order_id"],
            row["customer_id"],
            row["order_status"],
            row["order_purchase_timestamp"],
            text_or_none(row["order_approved_at"]),
            text_or_none(row["order_delivered_carrier_date"]),
            text_or_none(row["order_delivered_customer_date"]),
            text_or_none(row["order_estimated_delivery_date"]),
        )


def order_item_rows(archive: zipfile.ZipFile) -> Iterator[tuple]:
    for row in read_csv(archive, "olist_order_items_dataset.csv"):
        yield (
            row["order_id"],
            int(row["order_item_id"]),
            row["product_id"],
            row["seller_id"],
            row["shipping_limit_date"],
            row["price"],
            row["freight_value"],
        )


def order_payment_rows(archive: zipfile.ZipFile) -> Iterator[tuple]:
    for row in read_csv(archive, "olist_order_payments_dataset.csv"):
        yield (
            row["order_id"],
            int(row["payment_sequential"]),
            row["payment_type"],
            int(row["payment_installments"]),
            row["payment_value"],
        )


def order_review_rows(archive: zipfile.ZipFile) -> Iterator[tuple]:
    # The comment title and message are left out on purpose (ADR 0003).
    for row in read_csv(archive, "olist_order_reviews_dataset.csv"):
        yield (
            row["review_id"],
            row["order_id"],
            int(row["review_score"]),
            row["review_creation_date"],
            text_or_none(row["review_answer_timestamp"]),
        )


# --- Loading --------------------------------------------------------------


def copy_rows(conn: psycopg.Connection, table: str, rows: Iterable[tuple]) -> None:
    # COPY loads all rows in one statement, much faster than one INSERT per row.
    with conn.cursor().copy(f"COPY {table} FROM STDIN") as copy:
        for row in rows:
            copy.write_row(row)


def load(conn: psycopg.Connection, archive: zipfile.ZipFile) -> dict[str, int]:
    """Replace every table's content in one transaction and return the row counts."""
    with conn.transaction():
        conn.execute(f"TRUNCATE {', '.join(TABLES)}")
        copy_rows(conn, "regions", REGIONS)
        copy_rows(conn, "customers", customer_rows(archive))
        copy_rows(conn, "sellers", seller_rows(archive))
        copy_rows(conn, "products", product_rows(archive))
        copy_rows(conn, "orders", order_rows(archive))
        copy_rows(conn, "order_items", order_item_rows(archive))
        copy_rows(conn, "order_payments", order_payment_rows(archive))
        copy_rows(conn, "order_reviews", order_review_rows(archive))
    return {table: conn.execute(f"SELECT count(*) FROM {table}").fetchone()[0] for table in TABLES}


def main() -> dict[str, int]:
    path = ensure_dataset()
    with zipfile.ZipFile(path) as archive, psycopg.connect(**get_settings().connect_kwargs(OWNER_ROLE)) as conn:
        counts = load(conn, archive)
    for table, count in counts.items():
        print(f"{table:<16}{count:>9,}")
    return counts


if __name__ == "__main__":
    main()
