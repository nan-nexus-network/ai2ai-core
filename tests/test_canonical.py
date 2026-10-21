# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 NAN AI2AI-SI2SI contributors

"""Kiem thu chuan hoa du lieu va bam co phan tach mien (domain separation).

Muc tieu chinh: chung minh rang hai van de cua bam v0.1 da duoc sua:
  1. "Hai blob JSON noi truc tiep" -> khong co dau phan cach, khong co domain
     separator. Da thay bang length-prefixed framing + domain separator.
  2. Cung mot noi dung nhung khac domain -> phai cho bam KHAC NHAU.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nan_ai2ai import canonical  # noqa: E402


class TestCanonicalJson(unittest.TestCase):

    def test_key_order_does_not_matter(self):
        a = canonical.canonical_json({"b": 2, "a": 1})
        b = canonical.canonical_json({"a": 1, "b": 2})
        self.assertEqual(a, b)

    def test_no_whitespace_between_tokens(self):
        out = canonical.canonical_json({"a": 1, "b": [1, 2]}).decode()
        self.assertNotIn(" ", out)
        self.assertEqual(out, '{"a":1,"b":[1,2]}')

    def test_unicode_is_not_escaped(self):
        out = canonical.canonical_json({"x": "Tiếng Việt"}).decode("utf-8")
        self.assertIn("Tiếng Việt", out)

    def test_same_object_same_bytes(self):
        obj = {"z": [3, 1, 2], "a": {"k": "v"}}
        self.assertEqual(canonical.canonical_json(obj), canonical.canonical_json(obj))

    def test_different_content_different_bytes(self):
        self.assertNotEqual(
            canonical.canonical_json({"a": 1}), canonical.canonical_json({"a": 2}))


class TestDigestInput(unittest.TestCase):

    def test_domain_separator_changes_digest(self):
        a = canonical.digest_of("domain-a", b"payload")
        b = canonical.digest_of("domain-b", b"payload")
        self.assertNotEqual(a, b)

    def test_length_prefix_prevents_boundary_confusion(self):
        """Hai phan tach khac nhau khong duoc cho cung mot bam."""
        first = canonical.digest_input("d", b"ab", b"cd")
        second = canonical.digest_input("d", b"abc", b"d")
        self.assertNotEqual(first, second)

    def test_order_of_parts_matters(self):
        self.assertNotEqual(
            canonical.digest_input("d", b"x", b"y"),
            canonical.digest_input("d", b"y", b"x"))

    def test_number_of_parts_matters(self):
        self.assertNotEqual(
            canonical.digest_input("d", b"xy"),
            canonical.digest_input("d", b"x", b"y"))

    def test_empty_domain_rejected(self):
        with self.assertRaises(ValueError):
            canonical.digest_input("", b"x")

    def test_non_bytes_part_rejected(self):
        with self.assertRaises(TypeError):
            canonical.digest_input("d", "khong phai bytes")

    def test_length_prefix_is_four_bytes_big_endian(self):
        out = canonical.digest_input("d", b"abc")
        self.assertEqual(out[0:1], b"d")
        self.assertEqual(out[1:2], b"\x00")
        self.assertEqual(out[2:6], (3).to_bytes(4, "big"))
        self.assertEqual(out[6:], b"abc")

    def test_digest_of_is_hex_sha256(self):
        value = canonical.digest_of("d", b"x")
        self.assertEqual(len(value), 64)
        int(value, 16)


class TestTaskAndResultDomains(unittest.TestCase):

    def test_task_and_result_digests_differ(self):
        """Task va result la hai vai tro khac nhau -> digest phai khac nhau."""
        payload = {"same": "content"}
        task = canonical.digest_of(canonical.DOMAIN_RECEIPT, canonical.canonical_json(payload))
        result = canonical.digest_of(canonical.DOMAIN_RECEIPT + "/result",
                                     canonical.canonical_json(payload))
        self.assertNotEqual(task, result)


if __name__ == "__main__":
    unittest.main()
