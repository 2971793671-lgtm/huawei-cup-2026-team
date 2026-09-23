import csv
import hashlib
import json
import lzma
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = [
    ("A1", "A_data_value/slimpajama_quality_signal_sample.jsonl.xz"),
    ("A2", "A_data_value/slimpajama_quality_extended/arxiv_part-6777d8857c6e-000486.jsonl.xz"),
    ("A3", "A_data_value/slimpajama_quality_extended/github_part-6777d8857c6e-000275.jsonl.xz"),
    ("A4", "A_data_value/regmix_tables/train_mixture_1m.csv"),
    ("A5", "A_data_value/regmix_tables/train_pile_loss_1m.csv"),
    ("A6", "A_data_value/regmix_tables/test_mixture_1m.csv"),
    ("A7", "A_data_value/regmix_tables/test_pile_loss_1m.csv"),
    ("A8", "A_data_value/regmix_tables/test_mixture_60m.csv"),
    ("A9", "A_data_value/regmix_tables/test_pile_loss_60m.csv"),
    ("A10", "A_data_value/regmix_tables/test_mixture_1B.csv"),
    ("A11", "A_data_value/regmix_tables/test_pile_loss_1B.csv"),
    ("A12", "A_data_value/regmix_tables/est_mixture_10b.csv"),
    ("A13", "A_data_value/regmix_tables/est_pile_loss_10b.csv"),
    ("A14", "A_data_value/regmix_tables/est_mixture_70b.csv"),
    ("A15", "A_data_value/regmix_tables/est_pile_loss_70b.csv"),
    ("A16", "A_data_value/domain_mapping_guide.csv"),
]

INT_RE = re.compile(r"^[+-]?\d+$")
NUM_RE = re.compile(r"^[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?$")


def scalar_type(value):
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, int):
        return "integer"
    if isinstance(value, float):
        return "number"
    if isinstance(value, str):
        return "string"
    if isinstance(value, list):
        return "array"
    if isinstance(value, dict):
        return "object"
    return type(value).__name__


def csv_scalar_type(value):
    value = value.strip()
    if not value:
        return "empty"
    if INT_RE.fullmatch(value):
        return "integer"
    if NUM_RE.fullmatch(value):
        return "number"
    if value.lower() in {"true", "false"}:
        return "boolean"
    return "string"


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def scan_csv(path):
    fields = []
    types = defaultdict(set)
    missing = Counter()
    row_count = 0
    width_errors = []
    index_values = []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle, strict=True)
        try:
            fields = next(reader)
        except StopIteration:
            return {
                "format": "csv",
                "record_count": 0,
                "field_count": 0,
                "fields": [],
                "observed_types": {},
                "missing_counts": {},
                "width_errors": [],
                "duplicate_header": [],
            }
        duplicate_header = sorted({name for name in fields if fields.count(name) > 1})
        for row in reader:
            row_count += 1
            if len(row) != len(fields):
                width_errors.append(
                    {"row": row_count + 1, "observed": len(row), "expected": len(fields)}
                )
                continue
            for name, value in zip(fields, row):
                kind = csv_scalar_type(value)
                types[name].add(kind)
                if kind == "empty":
                    missing[name] += 1
            if "index" in fields:
                index_values.append(row[fields.index("index")])
    result = {
        "format": "csv",
        "record_count": row_count,
        "field_count": len(fields),
        "fields": fields,
        "observed_types": {name: sorted(kinds) for name, kinds in types.items()},
        "missing_counts": dict(missing),
        "width_errors": width_errors[:10],
        "duplicate_header": duplicate_header,
    }
    if "index" in fields:
        result["index_unique_count"] = len(set(index_values))
        result["index_duplicate_count"] = len(index_values) - len(set(index_values))
    return result


def scan_jsonl_xz(path):
    fields = set()
    presence = Counter()
    types = defaultdict(set)
    field_count_distribution = Counter()
    domain_counts = Counter()
    row_count = 0
    parse_errors = []
    duplicate_key_records = 0
    nonblank_line_count = 0
    nonfinite_token_counts = Counter()

    def pairs_hook(pairs):
        nonlocal duplicate_key_records
        names = [name for name, _ in pairs]
        if len(names) != len(set(names)):
            duplicate_key_records += 1
        return dict(pairs)

    def parse_constant(value):
        nonfinite_token_counts[value] += 1
        return float(value)

    with lzma.open(path, "rt", encoding="utf-8", errors="strict") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            nonblank_line_count += 1
            try:
                obj = json.loads(
                    line,
                    object_pairs_hook=pairs_hook,
                    parse_constant=parse_constant,
                )
            except Exception as exc:
                parse_errors.append({"line": line_number, "error_type": type(exc).__name__})
                continue
            row_count += 1
            if not isinstance(obj, dict):
                types["<root>"].add(scalar_type(obj))
                continue
            field_count_distribution[len(obj)] += 1
            for name, value in obj.items():
                fields.add(name)
                presence[name] += 1
                types[name].add(scalar_type(value))
            if isinstance(obj.get("_source_domain"), str):
                domain_counts[obj["_source_domain"]] += 1
    return {
        "format": "jsonl.xz",
        "record_count": row_count,
        "field_count": len(fields),
        "fields": sorted(fields),
        "observed_types": {name: sorted(kinds) for name, kinds in sorted(types.items())},
        "field_presence_counts": dict(sorted(presence.items())),
        "record_field_count_distribution": dict(sorted(field_count_distribution.items())),
        "domain_counts": dict(sorted(domain_counts.items())),
        "duplicate_key_record_count": duplicate_key_records,
        "parse_error_count": len(parse_errors),
        "parse_error_types": sorted({item["error_type"] for item in parse_errors}),
        "nonblank_line_count": nonblank_line_count,
        "nonfinite_token_counts": dict(nonfinite_token_counts),
    }


def scan(path):
    return scan_jsonl_xz(path) if path.suffix == ".xz" else scan_csv(path)


def file_path(relative_path):
    return ROOT / "data" / "origin" / "real_attachments" / relative_path


result = {"root": "data/origin/real_attachments", "files": [], "relations": []}
for dataset_id, relative_path in FILES:
    path = file_path(relative_path)
    metadata = scan(path)
    metadata.update(
        {
            "dataset_id": dataset_id,
            "relative_path": relative_path,
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
        }
    )
    result["files"].append(metadata)


by_id = {item["dataset_id"]: item for item in result["files"]}
for mixture, loss in [("A4", "A5"), ("A6", "A7"), ("A8", "A9"), ("A10", "A11"), ("A12", "A13"), ("A14", "A15")]:
    def index_values(relative_path):
        values = []
        with file_path(relative_path).open("r", encoding="utf-8-sig", newline="") as handle:
            for row in csv.DictReader(handle):
                values.append(row.get("index", ""))
        return values

    mixture_indices = index_values(by_id[mixture]["relative_path"])
    loss_indices = index_values(by_id[loss]["relative_path"])
    mixture_set = set(mixture_indices)
    loss_set = set(loss_indices)
    result["relations"].append(
        {
            "mixture": mixture,
            "loss": loss,
            "mixture_index_count": len(mixture_indices),
            "loss_index_count": len(loss_indices),
            "mixture_index_unique": len(mixture_set),
            "loss_index_unique": len(loss_set),
            "exact_index_set_match": mixture_set == loss_set,
            "intersection_count": len(mixture_set & loss_set),
            "mixture_only_count": len(mixture_set - loss_set),
            "loss_only_count": len(loss_set - mixture_set),
        }
    )


result["quality_summary"] = {
    dataset_id: {
        key: by_id[dataset_id].get(key)
        for key in (
            "record_count",
            "field_count",
            "fields",
            "observed_types",
            "domain_counts",
            "record_field_count_distribution",
            "parse_error_count",
            "duplicate_key_record_count",
        )
    }
    for dataset_id in ("A1", "A2", "A3")
}
print(json.dumps(result, ensure_ascii=False, indent=2))
