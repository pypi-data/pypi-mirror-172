from django.test import TestCase

from taskmonitor.helpers import (
    compress_list,
    dict_sort_keys,
    extract_app_name,
    truncate_dict,
    truncate_list,
    truncate_result,
)


class TestExtractAppName(TestCase):
    def test_can_extract_from_normal_task_name(self):
        # when
        result = extract_app_name("alpha.tasks.task_name")
        # then
        self.assertEqual(result, "alpha")

    def test_can_extract_from_long_task_name(self):
        # when
        result = extract_app_name("omega.alpha.tasks.task_name")
        # then
        self.assertEqual(result, "alpha")

    def test_can_extract_from_extra_long_task_name(self):
        # when
        result = extract_app_name("echo.omega.alpha.tasks.task_name")
        # then
        self.assertEqual(result, "alpha")

    def test_can_extract_from_custom_task_name(self):
        # when
        result = extract_app_name("alpha.task_name")
        # then
        self.assertEqual(result, "alpha")

    def test_should_return_empty_string_if_no_match_1(self):
        # when
        result = extract_app_name("dummy")
        # then
        self.assertEqual(result, "")

    def test_should_return_empty_string_if_no_match_2(self):
        # when
        result = extract_app_name("tasks.dummy")
        # then
        self.assertEqual(result, "")


class TestTruncateList(TestCase):
    def test_should_copy_unnested_list(self):
        # when
        result = truncate_list([1, "alpha", 3])
        # then
        self.assertListEqual(result, [1, "alpha", 3])

    def test_should_truncate_nested_list(self):
        # when
        result = truncate_list([1, [1, 2], 3])
        # then
        self.assertListEqual(result, [1, [], 3])

    def test_should_truncate_nested_dict(self):
        # when
        result = truncate_list([1, {"alpha": 1}, 3])
        # then
        self.assertListEqual(result, [1, {}, 3])

    def test_should_truncate_tuple(self):
        # when
        result = truncate_list([1, (1, 2), 3])
        # then
        self.assertListEqual(result, [1, [], 3])

    def test_should_truncate_mix(self):
        # when
        result = truncate_list([1, [1, 2], {"alpha": 1}, (1, 2), 3])
        # then
        self.assertListEqual(result, [1, [], {}, [], 3])


class TestTruncateDict(TestCase):
    def test_should_copy_unnested_dict(self):
        # when
        result = truncate_dict({"a": 1, "b": "blue"})
        # then
        self.assertDictEqual(result, {"a": 1, "b": "blue"})

    def test_should_truncate_nested_lists(self):
        # when
        result = truncate_dict({"a": [1, 2, 3]})
        # then
        self.assertDictEqual(result, {"a": []})

    def test_should_truncate_nested_dict(self):
        # when
        result = truncate_dict({"a": {"aa": 1, "ab": 2}})
        # then
        self.assertDictEqual(result, {"a": {}})

    def test_should_truncate_mixed(self):
        # when
        result = truncate_dict({"a": 1, "b": {"ba": 1}, "c": [1, 2]})
        # then
        self.assertDictEqual(result, {"a": 1, "b": {}, "c": []})


class TestSortDict(TestCase):
    def test_should_sort_normal_keys(self):
        # when
        result = dict_sort_keys({"a": 1, "C": 3, "b": 2})
        # then
        expected = {"a": 1, "b": 2, "C": 3}
        self.assertDictEqual(result, expected)
        self.assertListEqual(list(result.keys()), list(expected.keys()))


class TestTruncateResult(TestCase):
    def test_should_copy_scalar_values(self):
        # when
        result = truncate_result("alpha")
        # then
        self.assertEqual(result, "alpha")

    def test_should_truncate_nested_lists(self):
        # when
        result = truncate_result([1, [1, 2], {"alpha": 1}, (1, 2), 3])
        # then
        self.assertListEqual(result, [1, [], {}, [], 3])

    def test_should_truncate_nested_dicts(self):
        # when
        result = truncate_result({"a": 1, "b": {"ba": 1}, "c": [1, 2]})
        # then
        self.assertDictEqual(result, {"a": 1, "b": {}, "c": []})

    def test_should_truncate_and_compress_nested_lists(self):
        # when
        result = truncate_result([[1, 2], {"alpha": 1}, (1, 2)])
        # then
        self.assertListEqual(result, [])


class TestCompressList(TestCase):
    def test_should_copy_non_empty_list_1(self):
        # when
        result = compress_list([1, 2])
        # then
        self.assertListEqual(result, [1, 2])

    def test_should_copy_non_empty_list_2(self):
        # when
        result = compress_list([1, []])
        # then
        self.assertListEqual(result, [1, []])

    def test_should_compress_list_of_empty_containers(self):
        # when
        result = compress_list([[], {}, tuple(), set()])
        # then
        self.assertListEqual(result, [])

    def test_should_keep_booleans(self):
        # when
        result = compress_list([False, []])
        # then
        self.assertListEqual(result, [False, []])
