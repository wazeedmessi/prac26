import csv
from pathlib import Path

from clean_customers import clean_customers


def test_clean_customers(tmp_path):
    source = Path("customers.csv")
    output = tmp_path / "customers_clean.csv"

    clean_customers(source, output)

    with output.open(newline="") as handle:
        rows = list(csv.DictReader(handle))

    assert rows[0]["name"] == "David"
    assert rows[0]["email"] == "user2@example.com"
    assert rows[1]["name"] == "David"
    assert rows[9]["city"] == "Unknown"
    assert rows[11]["amount"] == "5378"
    assert rows[18]["email"] == "user20@example.com"
    assert rows[24]["amount"] == "5327"
