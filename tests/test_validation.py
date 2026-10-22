# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 NAN AI2AI-SI2SI contributors

"""Kiem thu bo kiem tra cau truc (subset cua JSON Schema Draft 2020-12).

Muc tieu chinh: bo nay phai **bat duoc loi thuc su** cua v0.1, truoc do
``sanitize_and_validate`` chi kiem tra *su ton tai* cua truong:

    route = ""              -> v0.1: hop le   | bo nay: FAIL
    route = 12345           -> v0.1: hop le   | bo nay: FAIL
    cargo_type = None       -> v0.1: hop le   | bo nay: FAIL
    max_latency_hours = "x" -> v0.1: hop le   | bo nay: FAIL
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nan_ai2ai import validation  # noqa: E402


# --- Schema duoc dung trong demo ---
PACKET_SCHEMA = {
    "type": "object",
    "required": ["context_id", "tool_call"],
    "additionalProperties": False,
    "properties": {
        "context_id": {"type": "string", "minLength": 3, "maxLength": 256},
        "tool_call": {
            "type": "object",
            "required": ["name"],
            "additionalProperties": False,
            "properties": {
                "name": {"type": "string", "minLength": 1, "maxLength": 128},
                "arguments": {
                    "type": "object",
                    "required": ["route", "cargo_type"],
                    "additionalProperties": False,
                    "properties": {
                        "route": {"type": "string", "minLength": 1, "maxLength": 128},
                        "cargo_type": {"type": "string", "minLength": 1, "maxLength": 64},
                        "max_latency_hours": {
                            "type": "integer", "minimum": 1, "maximum": 720},
                    },
                },
            },
        },
    },
}


def packet(**overrides):
    base = {
        "context_id": "did:eco_a:agent_01",
        "tool_call": {
            "name": "query_asean_logistics_slot",
            "arguments": {"route": "DaNang_to_Singapore", "cargo_type": "Electronics"},
        },
    }
    base.update(overrides)
    return base


class TestValidPackets(unittest.TestCase):

    def test_valid_packet_passes(self):
        self.assertEqual(validation.validate(packet(), PACKET_SCHEMA), [])

    def test_valid_packet_with_optional_field(self):
        p = packet()
        p["tool_call"]["arguments"]["max_latency_hours"] = 24
        self.assertEqual(validation.validate(p, PACKET_SCHEMA), [])

    def test_validate_or_raise_passes(self):
        validation.validate_or_raise(packet(), PACKET_SCHEMA)


class TestTypeChecking(unittest.TestCase):
    """Cac lo hổng v0.1 da chung minh bang chay ma."""

    def test_empty_string_route_is_rejected(self):
        p = packet()
        p["tool_call"]["arguments"]["route"] = ""
        self.assertTrue(validation.validate(p, PACKET_SCHEMA))

    def test_numeric_route_is_rejected(self):
        p = packet()
        p["tool_call"]["arguments"]["route"] = 12345
        self.assertTrue(validation.validate(p, PACKET_SCHEMA))

    def test_none_cargo_type_is_rejected(self):
        p = packet()
        p["tool_call"]["arguments"]["cargo_type"] = None
        self.assertTrue(validation.validate(p, PACKET_SCHEMA))

    def test_non_numeric_max_latency_hours_is_rejected(self):
        p = packet()
        p["tool_call"]["arguments"]["max_latency_hours"] = "KHONG_PHAI_SO_AM_TIEN"
        errors = validation.validate(p, PACKET_SCHEMA)
        self.assertTrue(errors)
        self.assertIn("max_latency_hours", errors[0])

    def test_boolean_is_not_an_integer(self):
        p = packet()
        p["tool_call"]["arguments"]["max_latency_hours"] = True
        self.assertTrue(validation.validate(p, PACKET_SCHEMA))


class TestRanges(unittest.TestCase):

    def test_below_minimum_is_rejected(self):
        p = packet()
        p["tool_call"]["arguments"]["max_latency_hours"] = 0
        self.assertTrue(validation.validate(p, PACKET_SCHEMA))

    def test_above_maximum_is_rejected(self):
        p = packet()
        p["tool_call"]["arguments"]["max_latency_hours"] = 100000
        self.assertTrue(validation.validate(p, PACKET_SCHEMA))

    def test_too_long_route_is_rejected(self):
        p = packet()
        p["tool_call"]["arguments"]["route"] = "A" * 500
        self.assertTrue(validation.validate(p, PACKET_SCHEMA))

    def test_exclusive_bounds(self):
        schema = {"type": "integer", "exclusiveMinimum": 0, "exclusiveMaximum": 10}
        self.assertTrue(validation.validate(0, schema))
        self.assertTrue(validation.validate(10, schema))
        self.assertEqual(validation.validate(5, schema), [])


class TestAllowlist(unittest.TestCase):

    def test_unknown_top_level_field_is_rejected(self):
        p = packet(extra_field="x")
        self.assertTrue(validation.validate(p, PACKET_SCHEMA))

    def test_unknown_argument_is_rejected(self):
        p = packet()
        p["tool_call"]["arguments"]["sneaky"] = "x"
        self.assertTrue(validation.validate(p, PACKET_SCHEMA))

    def test_missing_required_field_is_rejected(self):
        p = packet()
        del p["tool_call"]["arguments"]["route"]
        errors = validation.validate(p, PACKET_SCHEMA)
        self.assertTrue(errors)
        self.assertIn("route", errors[0])

    def test_missing_top_level_field_is_rejected(self):
        p = packet()
        del p["context_id"]
        self.assertTrue(validation.validate(p, PACKET_SCHEMA))

    def test_additional_properties_true_allows_extra(self):
        schema = {"type": "object", "properties": {"a": {"type": "string"}}}
        self.assertEqual(validation.validate({"a": "x", "b": 1}, schema), [])


class TestOperationIdSchema(unittest.TestCase):
    """operation_id la khoa idempotency - bat buoc co trong goi tin Bridge."""

    def test_module_schema_requires_operation_id(self):
        from nan_ai2ai import validation as v
        schema = v.bridge_packet_schema(["route", "cargo_type"])
        self.assertIn("operation_id", schema["required"])
        self.assertIn("operation_id", schema["properties"])

    def test_packet_without_operation_id_fails_module_schema(self):
        from nan_ai2ai import validation as v
        schema = v.bridge_packet_schema(["route", "cargo_type"])
        packet = {
            "context_id": "did:eco_a:agent_01",
            "tool_call": {"name": "q", "arguments": {"route": "R", "cargo_type": "C"}},
        }
        self.assertTrue(v.validate(packet, schema))

    def test_packet_with_operation_id_passes_module_schema(self):
        from nan_ai2ai import validation as v
        schema = v.bridge_packet_schema(["route", "cargo_type"])
        packet = {
            "context_id": "did:eco_a:agent_01",
            "operation_id": "op_1",
            "tool_call": {"name": "q", "arguments": {"route": "R", "cargo_type": "C"}},
        }
        self.assertEqual(v.validate(packet, schema), [])

    def test_empty_operation_id_fails_module_schema(self):
        from nan_ai2ai import validation as v
        schema = v.bridge_packet_schema(["route", "cargo_type"])
        packet = {
            "context_id": "did:eco_a:agent_01",
            "operation_id": "",
            "tool_call": {"name": "q", "arguments": {"route": "R", "cargo_type": "C"}},
        }
        self.assertTrue(v.validate(packet, schema))

    def test_unknown_required_argument_is_rejected(self):
        from nan_ai2ai import validation as v
        with self.assertRaises(ValueError):
            v.bridge_packet_schema(["khong_co_trong_kho_dac_biet"])


class TestAnnotationKeywords(unittest.TestCase):
    """Tu khoa chi mang tinh CHU THICH (khong co nghia ganh validation) duoc bo qua."""

    def test_description_is_accepted_as_no_op(self):
        schema = {"type": "string", "description": "mo ta"}
        self.assertEqual(validation.validate("x", schema), [])

    def test_title_is_accepted_as_no_op(self):
        schema = {"type": "integer", "title": "so"}
        self.assertEqual(validation.validate(5, schema), [])

    def test_annotation_keywords_are_listed_separately(self):
        self.assertIn("description", validation.ANNOTATION_KEYWORDS)
        self.assertNotIn("description", validation.KNOWN_UNSUPPORTED)

    def test_validation_affecting_keyword_is_still_rejected(self):
        with self.assertRaises(validation.ValidationError):
            validation.validate(1, {"if": {"type": "integer"}})


class TestUnsupportedKeywords(unittest.TestCase):

    def test_unsupported_keyword_is_reported_not_ignored(self):
        schema = {"type": "object", "$ref": "#/definitions/x"}
        with self.assertRaises(validation.ValidationError) as ctx:
            validation.validate({"a": 1}, schema)
        self.assertIn("$ref", str(ctx.exception))

    def test_if_then_else_is_reported(self):
        with self.assertRaises(validation.ValidationError):
            validation.validate(1, {"if": {"type": "integer"}})

    def test_unknown_keyword_is_reported(self):
        with self.assertRaises(validation.ValidationError):
            validation.validate(1, {"totallyMadeUp": True})


class TestMisc(unittest.TestCase):

    def test_enum_and_const(self):
        self.assertTrue(validation.validate("z", {"enum": ["a", "b"]}))
        self.assertEqual(validation.validate("a", {"enum": ["a", "b"]}), [])
        self.assertTrue(validation.validate("z", {"const": "a"}))
        self.assertEqual(validation.validate("a", {"const": "a"}), [])

    def test_pattern_and_property_names(self):
        self.assertTrue(validation.validate("abc", {"type": "string", "pattern": "^z"}))
        schema = {"type": "object", "propertyNames": {"pattern": "^did:"}}
        self.assertTrue(validation.validate({"bad": 1}, schema))

    def test_array_items_and_bounds(self):
        schema = {"type": "array", "minItems": 1, "maxItems": 3,
                  "items": {"type": "integer"}}
        self.assertEqual(validation.validate([1, 2], schema), [])
        self.assertTrue(validation.validate([], schema))
        self.assertTrue(validation.validate([1, 2, 3, 4], schema))
        self.assertTrue(validation.validate([1, "x"], schema))

    def test_multiple_of(self):
        self.assertEqual(validation.validate(10, {"type": "integer", "multipleOf": 5}), [])
        self.assertTrue(validation.validate(11, {"type": "integer", "multipleOf": 5}))

    def test_error_contains_path(self):
        p = packet()
        p["tool_call"]["arguments"]["route"] = 1
        errors = validation.validate(p, PACKET_SCHEMA)
        self.assertIn("tool_call.arguments.route", errors[0])


if __name__ == "__main__":
    unittest.main()
