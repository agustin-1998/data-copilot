"""The seed loads the same Olist data every time (ADR 0003)."""

from pathlib import Path

import psycopg
import pytest

from data_copilot import seed

EXPECTED_COUNTS = {
    "regions": 27,
    "customers": 99_441,
    "sellers": 3_095,
    "products": 32_951,
    "orders": 99_441,
    "order_items": 112_650,
    "order_payments": 103_886,
    "order_reviews": 99_224,
}


@pytest.fixture(scope="module")
def seeded_twice() -> tuple[dict[str, int], dict[str, int]]:
    """Run the seed two times in a row and keep both row counts."""
    return seed.main(), seed.main()


def test_seed_loads_the_expected_rows(seeded_twice) -> None:
    first, _ = seeded_twice
    assert first == EXPECTED_COUNTS


def test_running_the_seed_twice_gives_the_same_database(seeded_twice, owner: psycopg.Connection) -> None:
    first, second = seeded_twice
    assert second == first
    # Same fake person as on every other run, thanks to the fixed Faker seed.
    first_customer = owner.execute(
        "SELECT customer_name, customer_email FROM customers ORDER BY customer_id LIMIT 1"
    ).fetchone()
    seed.main()
    assert owner.execute(
        "SELECT customer_name, customer_email FROM customers ORDER BY customer_id LIMIT 1"
    ).fetchone() == first_customer


def test_one_real_person_gets_one_fake_identity(seeded_twice, owner: psycopg.Connection) -> None:
    people_with_two_identities = owner.execute(
        """
        SELECT count(*) FROM (
            SELECT customer_unique_id
            FROM customers
            GROUP BY customer_unique_id
            HAVING count(DISTINCT (customer_name, customer_email, customer_phone)) > 1
        ) AS conflicts
        """
    ).fetchone()[0]
    assert people_with_two_identities == 0


def test_fake_emails_only_use_example_domains(seeded_twice, owner: psycopg.Connection) -> None:
    other_domains = owner.execute(
        "SELECT count(*) FROM customers WHERE customer_email !~ '@example\\.(com|net|org)$'"
    ).fetchone()[0]
    assert other_domains == 0


def test_categories_are_in_english(seeded_twice, owner: psycopg.Connection) -> None:
    categories = {row[0] for row in owner.execute("SELECT DISTINCT product_category_name FROM products")}
    assert "health_beauty" in categories
    assert "kitchen_portables_and_food_preparers" in categories
    assert "beleza_saude" not in categories


def test_review_comments_are_not_stored(owner: psycopg.Connection) -> None:
    columns = {
        row[0]
        for row in owner.execute(
            "SELECT column_name FROM information_schema.columns WHERE table_name = 'order_reviews'"
        )
    }
    assert "review_comment_title" not in columns
    assert "review_comment_message" not in columns


def test_a_file_with_the_wrong_checksum_is_rejected(tmp_path: Path) -> None:
    tampered = tmp_path / "dataset.zip"
    tampered.write_bytes(b"not the olist dataset")
    with pytest.raises(ValueError, match="Checksum mismatch"):
        seed.verify_checksum(tampered)
