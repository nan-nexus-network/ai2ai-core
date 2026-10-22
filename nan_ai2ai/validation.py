# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 NAN AI2AI-SI2SI contributors

"""Kiem tra cau truc bang thu vien chuan Python (khong phai JSON Schema day du).

Quyet dinh thiet ke (xem ``docs/ADR_002_SIGNED_RECEIPT_AND_TRUST_MODEL.md``)
---------------------------------------------------------------------------
Dung an ``docs/ADR_001.md`` (L37) noi "JSON Schema Draft 2020-12", trong khi
``Issue #1`` (L19) yeu cau "chi su dung thu vien chuan cua Python". Hai yeu cau
do xung dot: **JSON Schema Draft 2020-12 day du khong the chay bang stdlib**.

Cach phan giai da chon: **cai dat mot SUBSET cua Draft 2020-12 bang stdlib**,
va sua lai tu cho cua ADR-001 de noi ro rang day **khong phai** mot bo trien
khai Draft 2020-12 day du. Muc dich:

  1. Thay the **blocklist tu** bang **allowlist schema** (loai "kiem tra duyet
     doi mot chuoi" - hong doi voi "chi nhan dung nhung truong duoc phep").
  2. Giu dung cam ket "Zero Dependencies" da cong bo trong README.
  3. Khong tu nhat la chuan hoa day du: **tu noi ro phan con lai**.

Subset ho tro
-------------
``type`` (string/integer/number/object/array/boolean/null) · ``required`` ·
``properties`` · ``additionalProperties`` (bool) · ``enum`` · ``const`` ·
``minimum`` / ``maximum`` / ``exclusiveMinimum`` / ``exclusiveMaximum`` ·
``minLength`` / ``maxLength`` · ``minItems`` / ``maxItems`` · ``pattern`` ·
``items`` · ``propertyNames`` (regex) · ``multipleOf``

Subset **KHONG** ho tro (va khong nen gia lap)
------------------------------------------------
``$ref`` / ``$defs`` / ``$dynamicRef`` · ``if``/``then``/``else`` ·
``dependentSchemas`` / ``dependentRequired`` · ``unevaluatedProperties`` /
``unevaluatedItems`` · ``contains`` / ``minContains`` / ``maxContains`` ·
``uniqueItems`` · ``format`` (ghi chu khong assert) · ``contentEncoding`` /
``contentMediaType`` · ``prefixItems`` · ``patternProperties`` ·
``propertyNames`` dang "schema" phuc tap.

Neu mot schema su dung tu khoa ngoai subset, ``validate`` se **bao loi
explicit** thay vi im lang bo qua - tranh tinh trang "schema co ve hop le
nhung thuc te khong kiem tra gi".
"""

from __future__ import annotations

import re
from typing import Any, Dict, List, Mapping, Sequence, Tuple

__all__ = [
    "ANNOTATION_KEYWORDS",
    "ValidationError",
    "SUPPORTED_KEYWORDS",
    "bridge_packet_schema",
    "validate",
    "validate_or_raise",
]


#: Kho dac biet rong cua truong ``arguments`` trong goi tin MCP-style.
#: Moi truong duoc phep deu phai co ten nam trong kho nay - nhung ten **khong**
#: duoc biet se bi tu choi vi khong co trong schema (allowlist, khong blacklist).
ARGUMENT_SPECS: Mapping[str, Mapping[str, Any]] = {
    "route": {"type": "string", "minLength": 1, "maxLength": 128},
    "cargo_type": {"type": "string", "minLength": 1, "maxLength": 64},
    "max_latency_hours": {"type": "integer", "minimum": 1, "maximum": 720},
}


def bridge_packet_schema(
    required_arg_fields: Sequence[str] = ("route", "cargo_type"),
) -> Dict[str, Any]:
    """Schema cho goi tin MCP-style ma Bridge nhan vao.

    ``required_arg_fields`` phai la **tap con** cua :data:`ARGUMENT_SPECS`.
    Neu truong bat buoc khong co trong kho dac biet, hàm nem ``ValueError``
    thay vi tao schema cho phep bat ky thu gi - bo kiem tra nay dua tren
    *allowlist*, nen truong la khong duoc phep thi phai duoc **da dang ky truoc**.
    """
    unknown = [f for f in required_arg_fields if f not in ARGUMENT_SPECS]
    if unknown:
        raise ValueError(
            "Truong khong nam trong kho dac biet: %s. Hay dang ky truong nay vao "
            "nan_ai2ai.validation.ARGUMENT_SPECS truoc khi dung." % ", ".join(unknown))
    return {
        "type": "object",
        "required": ["context_id", "tool_call", "operation_id"],
        "additionalProperties": False,
        "properties": {
            "context_id": {"type": "string", "minLength": 3, "maxLength": 256},
            # Khoa idempotency: cung mot operation_id thi chi thuc hien mot lan.
            "operation_id": {"type": "string", "minLength": 1, "maxLength": 128},
            "tool_call": {
                "type": "object",
                "required": ["name"],
                "additionalProperties": False,
                "properties": {
                    "name": {"type": "string", "minLength": 1, "maxLength": 128},
                    "arguments": {
                        "type": "object",
                        "required": list(required_arg_fields),
                        "additionalProperties": False,
                        "properties": {k: dict(v) for k, v in ARGUMENT_SPECS.items()},
                    },
                },
            },
        },
    }


#: Cac tu khoa ma bo kiem tra nay thuc su thuc hien.
SUPPORTED_KEYWORDS = frozenset({
    "type", "required", "properties", "additionalProperties", "enum", "const",
    "minimum", "maximum", "exclusiveMinimum", "exclusiveMaximum",
    "minLength", "maxLength", "minItems", "maxItems", "pattern", "items",
    "propertyNames", "multipleOf",
})

#: Cac tu khoa **chi mang tinh chu thich**, KHONG co nghia ganh validation
#: trong Draft 2020-12 -> duoc bo qua mot cach an toan (khong the lam sai
#: ket qua kiem tra). Vi du: 'title', 'description'.
ANNOTATION_KEYWORDS = frozenset({
    "title", "description", "$comment",
})

#: Cac tu khoa bi biet la co trong Draft 2020-12 nhung KHONG duoc ho tro
#: va **co the anh huong ket qua validation** -> neu gap, bao loi ro rang
#: thay vi bo qua am tham.
KNOWN_UNSUPPORTED = frozenset({
    "$ref", "$defs", "$dynamicRef", "$dynamicAnchor", "$anchor", "$id",
    "if", "then", "else", "dependentSchemas", "dependentRequired",
    "unevaluatedProperties", "unevaluatedItems", "contains", "minContains",
    "maxContains", "uniqueItems", "format", "contentEncoding",
    "contentMediaType", "contentSchema", "prefixItems", "patternProperties",
    "default", "examples", "deprecated", "readOnly", "writeOnly", "$schema",
})


class ValidationError(ValueError):
    """Sai luật cau truc."""

    def __init__(self, path: str, message: str) -> None:
        super().__init__("%s: %s" % (path or "<root>", message))
        self.path = path
        self.message = message


def _type_matches(value: Any, expected: str) -> bool:
    if expected == "string":
        return isinstance(value, str)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, (list, tuple))
    if expected == "null":
        return value is None
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    raise ValidationError("", "Tu khoa 'type' chua gia tri hop le: %r" % expected)


def _check_keywords(schema: Mapping[str, Any], path: str) -> None:
    """Tu cho moi tu khoa ngoai subset, thay vi im lang bo qua."""
    for key in schema:
        if key in SUPPORTED_KEYWORDS or key in ANNOTATION_KEYWORDS:
            continue
        if key in KNOWN_UNSUPPORTED:
            raise ValidationError(
                path,
                "Schema dung tu khoa '%s' chua duoc ho tro boi bo kiem tra nay. "
                "Day la SUBSET cua JSON Schema Draft 2020-12, khong phai ban trien "
                "khai day du. Hay rut gon schema hoac bo tu khoa nay di." % key,
            )
        raise ValidationError(path, "Tu khoa schema la khong: %r" % key)


def _validate(value: Any, schema: Mapping[str, Any], path: str, errors: List[str]) -> None:
    if not isinstance(schema, Mapping):
        raise ValidationError(path, "Schema phai la doi tuong JSON")
    _check_keywords(schema, path)

    if "type" in schema:
        expected = schema["type"]
        options = expected if isinstance(expected, list) else [expected]
        if not any(_type_matches(value, opt) for opt in options):
            errors.append("%s: kieu duoc ki la %s, thuc te la %s" % (
                path or "<root>", "/".join(options), type(value).__name__))
            return

    if "const" in schema and value != schema["const"]:
        errors.append("%s: phai bang hang %r" % (path or "<root>", schema["const"]))

    if "enum" in schema and value not in schema["enum"]:
        errors.append("%s: gia tri %r khong thuoc tap cho phep" % (
            path or "<root>", value))

    if isinstance(value, str):
        _validate_string(value, schema, path, errors)
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        _validate_number(value, schema, path, errors)
    if isinstance(value, dict):
        _validate_object(value, schema, path, errors)
    if isinstance(value, (list, tuple)):
        _validate_array(value, schema, path, errors)


def _validate_string(value: str, schema: Mapping[str, Any], path: str,
                     errors: List[str]) -> None:
    if "minLength" in schema and len(value) < schema["minLength"]:
        errors.append("%s: do dai toi thieu %d (thuc te %d)" % (
            path or "<root>", schema["minLength"], len(value)))
    if "maxLength" in schema and len(value) > schema["maxLength"]:
        errors.append("%s: do dai toi da %d (thuc te %d)" % (
            path or "<root>", schema["maxLength"], len(value)))
    if "pattern" in schema and re.search(schema["pattern"], value) is None:
        errors.append("%s: khong khop mau %r" % (path or "<root>", schema["pattern"]))


def _validate_number(value: float, schema: Mapping[str, Any], path: str,
                     errors: List[str]) -> None:
    if "minimum" in schema and value < schema["minimum"]:
        errors.append("%s: nho hon muc toi thieu %r" % (path or "<root>", schema["minimum"]))
    if "maximum" in schema and value > schema["maximum"]:
        errors.append("%s: lon hon muc toi da %r" % (path or "<root>", schema["maximum"]))
    if "exclusiveMinimum" in schema and value <= schema["exclusiveMinimum"]:
        errors.append("%s: phai lon hon %r" % (path or "<root>", schema["exclusiveMinimum"]))
    if "exclusiveMaximum" in schema and value >= schema["exclusiveMaximum"]:
        errors.append("%s: phai nho hon %r" % (path or "<root>", schema["exclusiveMaximum"]))
    if "multipleOf" in schema:
        factor = schema["multipleOf"]
        if factor <= 0:
            errors.append("%s: 'multipleOf' phai la so duong" % (path or "<root>"))
        elif abs(value / factor - round(value / factor)) > 1e-9:
            errors.append("%s: phai la boi so cua %r" % (path or "<root>", factor))


def _validate_object(value: Mapping[str, Any], schema: Mapping[str, Any],
                     path: str, errors: List[str]) -> None:
    for field in schema.get("required", []):
        if field not in value:
            errors.append("%s: thieu truong bat buoc '%s'" % (path or "<root>", field))

    properties = schema.get("properties", {})
    additional = schema.get("additionalProperties", True)

    for key, sub_schema in properties.items():
        if key in value:
            child = "%s.%s" % (path, key) if path else key
            _validate(value[key], sub_schema, child, errors)

    if "propertyNames" in schema:
        pattern = schema["propertyNames"]
        if isinstance(pattern, Mapping) and "pattern" in pattern:
            for key in value:
                if re.search(pattern["pattern"], key) is None:
                    errors.append("%s: ten truong '%s' khong khop mau %r" % (
                        path or "<root>", key, pattern["pattern"]))

    if additional is False:
        for key in value:
            if key not in properties:
                errors.append("%s: truong '%s' khong duoc phep" % (path or "<root>", key))


def _validate_array(value: Sequence[Any], schema: Mapping[str, Any],
                    path: str, errors: List[str]) -> None:
    if "minItems" in schema and len(value) < schema["minItems"]:
        errors.append("%s: so phan tu toi thieu %d (thuc te %d)" % (
            path or "<root>", schema["minItems"], len(value)))
    if "maxItems" in schema and len(value) > schema["maxItems"]:
        errors.append("%s: so phan tu toi da %d (thuc te %d)" % (
            path or "<root>", schema["maxItems"], len(value)))
    item_schema = schema.get("items")
    if isinstance(item_schema, Mapping):
        for index, item in enumerate(value):
            _validate(item, item_schema, "%s[%d]" % (path, index), errors)


def validate(value: Any, schema: Mapping[str, Any]) -> List[str]:
    """Kiem tra ``value`` theo ``schema``. Tra ve danh sach loi (rong = hop le).

    Khong nem loi khi value vi pham; chi nem ``ValidationError`` khi *schema*
    sai (vi du dung tu khoa ngoai subset).
    """
    errors: List[str] = []
    _validate(value, schema, "", errors)
    return errors


def validate_or_raise(value: Any, schema: Mapping[str, Any]) -> None:
    """Kiem tra ``value``; nem ``ValidationError`` neu co loi."""
    errors = validate(value, schema)
    if errors:
        raise ValidationError("", "%d loi cau truc: %s" % (len(errors), "; ".join(errors)))
