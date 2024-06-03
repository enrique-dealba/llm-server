import json
import unittest
from datetime import datetime, timezone
from typing import Optional, Union
from unittest.mock import patch

from pydantic import BaseModel, Field

from client import Client
from templates import ObjectiveTime
from utils import (
    calculate_filling_percentage,
    clean_json_str,
    combine_jsons,
    combine_models,
    extract_field_from_prompt,
    extract_json_objective,
    extract_list_from_prompt,
    extract_objective,
    extract_time_from_prompt,
    get_current_time,
    get_model_fields_and_descriptions,
    get_partial_json,
    is_json_like,
    model_to_json,
    parse_partial_json,
    post_process_model,
    preprocess_json,
    process_fields,
    process_lists,
    process_times,
    settings,
)


class TestTime(unittest.TestCase):
    """Test get_current_time function."""

    @patch("utils.datetime")
    def test_get_current_time(self, mock_datetime):
        """Test if get_current_time returns the expected time."""
        mock_now = datetime(2024, 5, 31, 12, 0, 0, tzinfo=timezone.utc)
        mock_datetime.now.return_value = mock_now

        expected_time = str(mock_now)
        actual_time = get_current_time()

        self.assertEqual(actual_time, expected_time)


class SampleModel(BaseModel):
    """Sample model with four fields."""

    field1: str = Field(description="description1")
    field2: int = Field(description="description2")
    field3: float = Field(description="description3")
    field4: str = Field(default="default", description="description4")


class TestGetModelFieldsAndDescriptions(unittest.TestCase):
    """Test get_model_fields_and_descriptions function."""

    def test_get_model_fields_and_descriptions(self):
        """Test if function returns correct field descriptions."""
        expected_output = [
            ("field1", "description1"),
            ("field2", "description2"),
            ("field3", "description3"),
            ("field4", "description4"),
        ]
        self.assertEqual(
            get_model_fields_and_descriptions(SampleModel), expected_output
        )

    def test_empty_description(self):
        """Test model with fields without descriptions."""

        class NoDescriptionModel(BaseModel):
            field1: str
            field2: int

        expected_output = [("field1", ""), ("field2", "")]
        self.assertEqual(
            get_model_fields_and_descriptions(NoDescriptionModel), expected_output
        )

    def test_missing_schema_extra(self):
        """Test model without schema_extra."""

        class NoSchemaExtraModel(BaseModel):
            field1: str
            field2: int

        expected_output = [("field1", ""), ("field2", "")]
        self.assertEqual(
            get_model_fields_and_descriptions(NoSchemaExtraModel), expected_output
        )


class Foo(BaseModel):
    """Foo model with two fields."""

    foo_name: str = Field(description="Name of the foo.")
    foo_id: str = Field(description="ID of the foo, usually 3 digits.")


class FooTemplate(BaseModel):
    """FooTemplate model with optional fields."""

    foo_name: Optional[str] = None
    foo_id: Optional[str] = None


class TestCombineModels(unittest.TestCase):
    """Test combine_models function."""

    def test_combine_models_with_non_empty_values(self):
        """Test combining models with non-empty values."""
        instance1 = Foo(foo_name="Foo1", foo_id="001")
        instance2 = Foo(foo_name="Foo2", foo_id="002")
        combined_instance = combine_models([instance1, instance2])
        self.assertEqual(combined_instance.foo_name, "Foo1")
        self.assertEqual(combined_instance.foo_id, "001")

    def test_combine_models_with_some_none_values(self):
        """Test combining models with some None values."""
        instance1 = FooTemplate(foo_name="Foo1")
        instance2 = FooTemplate(foo_id="002")
        combined_instance = combine_models([instance1, instance2])
        self.assertEqual(combined_instance.foo_name, "Foo1")
        self.assertEqual(combined_instance.foo_id, "002")

    def test_combine_models_with_all_none_values(self):
        """Test combining models with all None values."""
        instance1 = FooTemplate()
        instance2 = FooTemplate()
        combined_instance = combine_models([instance1, instance2])
        self.assertIsNone(combined_instance.foo_name)
        self.assertIsNone(combined_instance.foo_id)

    def test_combine_models_with_empty_list(self):
        """Test combining models with empty list."""
        with self.assertRaises(ValueError):
            combine_models([])


class TestPreprocessJson(unittest.TestCase):
    """Test preprocess_json function."""

    def test_preprocess_json(self):
        """Test preprocessing JSON with and without trailing comma."""
        # Test case with trailing comma in JSON string
        json_str_with_trailing_comma = '{"key1": "value1", "key2": "value2",}'
        expected_result = '{"key1": "value1", "key2": "value2"}'
        self.assertEqual(preprocess_json(json_str_with_trailing_comma), expected_result)

        # Test case with no trailing comma in JSON string
        json_str_without_trailing_comma = '{"key1": "value1", "key2": "value2"}'
        self.assertEqual(
            preprocess_json(json_str_without_trailing_comma),
            json_str_without_trailing_comma,
        )


class TestPartialJson(unittest.TestCase):
    """Test parse_partial_json function."""

    def test_parse_partial_json_complete_data(self):
        """Test parsing complete JSON data."""
        json_str = '{"foo_name": "FooBar", "foo_id": "123"}'
        result = parse_partial_json(json_str, Foo)
        expected = Foo(foo_name="FooBar", foo_id="123")
        self.assertEqual(result, expected)

    def test_parse_partial_json_partial_data(self):
        """Test parsing partial JSON data."""
        json_str = '{"foo_name": "FooBar"}'
        result = parse_partial_json(json_str, FooTemplate)
        expected = FooTemplate(foo_name="FooBar")
        self.assertEqual(result, expected)

    def test_parse_partial_json_none_field(self):
        """Test parsing JSON with None field."""
        json_str = '{"foo_name": "FooBar", "foo_id": "None"}'
        result = parse_partial_json(json_str, FooTemplate)
        expected = FooTemplate(foo_name="FooBar", foo_id=None)
        self.assertEqual(result, expected)


class TestModel(BaseModel):
    """Test model with three fields."""

    name: str = Field(description="Name of the test model.")
    value: float = Field(description="A float value.")
    ids: list[int] = Field(description="List of integer IDs.")


class TestTemplate(BaseModel):
    """Test template with optional fields."""

    name: Optional[str] = None
    value: Optional[float] = None
    ids: Optional[list[int]] = None


class TestGetPartialJson(unittest.TestCase):
    """Test get_partial_json function."""

    def test_get_partial_json_complete_data(self):
        """Test getting partial JSON with complete data."""
        json_str = '{"name": "TestName", "value": 123.45, "ids": [1, 2, 3]}'
        result = get_partial_json(json_str, TestModel)
        expected = TestModel(name="TestName", value=123.45, ids=[1, 2, 3])
        self.assertEqual(result, expected)

    def test_get_partial_json_partial_data(self):
        """Test getting partial JSON with partial data."""
        json_str = '{"name": "TestName", "value": 123.45}'
        result = get_partial_json(json_str, TestTemplate)
        expected = TestTemplate(name="TestName", value=123.45)
        self.assertEqual(result, expected)

    def test_get_partial_json_with_trailing_comma(self):
        """Test getting partial JSON with trailing comma."""
        json_str = '{"name": "TestName", "value": 123.45, "ids": [1, 2, 3],}'
        result = get_partial_json(json_str, TestModel)
        expected = TestModel(name="TestName", value=123.45, ids=[1, 2, 3])
        self.assertEqual(result, expected)

    def test_get_partial_json_without_curly_with_comma(self):
        """Test getting partial JSON without closing curly brace."""
        json_str = '{"name": "TestName", "value": 123.45, "ids": [1, 2, 3],'
        result = get_partial_json(json_str, TestModel)
        expected = TestModel(name="TestName", value=123.45, ids=[1, 2, 3])
        self.assertEqual(result, expected)

    def test_get_partial_json_with_missing_closing_brace(self):
        """Test getting partial JSON with missing closing brace."""
        json_str = '{"name": "TestName", "value": 123.45, "ids": [1, 2, 3]'
        result = get_partial_json(json_str, TestModel)
        self.assertIsNone(result)  # This should be None as the JSON is invalid


class TestCleanJsonString(unittest.TestCase):
    """Test clean_json_str function."""

    def test_clean_json_str_removes_leading_trailing_whitespace(self):
        """Test removing leading and trailing whitespace."""
        self.assertEqual(clean_json_str('  {"key": "value"}  '), '{"key": "value"}')

    def test_clean_json_str_removes_single_line_comments(self):
        """Test removing single-line comments."""
        self.assertEqual(
            clean_json_str('{"key": "value"} // comment'), '{"key": "value"}'
        )

    def test_clean_json_str_removes_multi_line_comments(self):
        """Test removing multi-line comments."""
        self.assertEqual(
            clean_json_str('{"key": "value"} /* multi-line \n comment */'),
            '{"key": "value"}',
        )

    def test_clean_json_str_removes_trailing_commas(self):
        """Test removing trailing commas."""
        self.assertEqual(clean_json_str('{"key": "value",}'), '{"key": "value"}')

    def test_clean_json_str_removes_dots_outside_quotes(self):
        """Test removing dots outside quotes."""
        self.assertEqual(clean_json_str('{"key": "value".}'), '{"key": "value"}')

    def test_clean_json_str_combined(self):
        """Test removing whitespace, comments, and trailing commas."""
        json_str = """
        {
            "key1": "value1", // comment
            "key2": "value2", /* multi-line
            comment */
        }
        """
        cleaned_json = clean_json_str(json_str)
        # Remove any remaining whitespace for comparison
        cleaned_json = cleaned_json.replace(" ", "").replace("\n", "").replace("\t", "")
        expected_output = '{"key1":"value1","key2":"value2"}'
        self.assertEqual(cleaned_json, expected_output.replace(" ", ""))

    def test_clean_json_str_empty_string(self):
        """Test cleaning an empty string."""
        self.assertEqual(clean_json_str(""), "")

    def test_clean_json_str_only_whitespace(self):
        """Test cleaning a string with only whitespace."""
        self.assertEqual(clean_json_str("   "), "")

    def test_clean_json_str_no_changes_needed(self):
        """Test cleaning a string that needs no changes."""
        self.assertEqual(clean_json_str('{"key": "value"}'), '{"key": "value"}')


class TestIsJsonLike(unittest.TestCase):
    """Test is_json_like function."""

    def test_valid_json_like(self):
        """Test valid JSON-like strings."""
        self.assertTrue(is_json_like('{"key": "value"}'))
        self.assertTrue(is_json_like('{"key": 123}'))
        self.assertTrue(is_json_like('{"key": null}'))
        self.assertTrue(is_json_like('{"key": {"nested_key": "nested_value"}'))
        self.assertTrue(is_json_like('{"key": [1, 2, 3]}'))
        self.assertTrue(is_json_like('{"key": "value",}'))  # Trailing comma
        self.assertTrue(is_json_like('{"key": "value",'))  # Missing closing brace
        self.assertTrue(is_json_like('{"key": "value", "key2": }'))  # Missing value
        self.assertTrue(is_json_like('{"key": [1, 2,]}'))  # Invalid JSON array

    def test_invalid_json_like(self):
        """Test invalid JSON-like strings."""
        self.assertFalse(is_json_like('{key: "value"}'))  # Missing quotes around key
        self.assertFalse(is_json_like('{"key": value}'))  # Missing quotes around value
        self.assertFalse(is_json_like('{"key" "value"}'))  # Missing colon
        self.assertFalse(is_json_like("random string"))  # Not JSON-like at all
        self.assertFalse(is_json_like('{"key": "value"'))  # Missing brace and comma


class TestExtractJsonObjective(unittest.TestCase):
    """Test extract_json_objective function."""

    def test_extract_json_objective_valid_input(self):
        """Test extracting objective from valid JSON input."""
        input_string = """
        Some text before the JSON...
        {
            "objective": "ObjectiveTest",
            "other_field": "value"
        }
        """
        result = extract_json_objective(input_string)
        self.assertEqual(result, "ObjectiveTest")

    def test_extract_json_objective_missing_objective_field(self):
        """Test extracting objective from JSON without objective field."""
        input_string = """
        {
            "other_field": "value"
        }
        """
        result = extract_json_objective(input_string)
        self.assertIsNone(result)

    def test_extract_json_objective_partial_json(self):
        """Test extracting objective from partial JSON."""
        input_string = """
        {
            "objective": "ObjectiveTest",
            "other_field": "value"
        """
        result = extract_json_objective(input_string)
        self.assertEqual(result, "ObjectiveTest")


class TestCombineJsons(unittest.TestCase):
    """Test combine_jsons function."""

    def test_combine_jsons_valid_input(self):
        """Test combining JSON strings with valid input."""
        json_str_list = [
            '{"foo_name": "Foo1", "foo_id": "001"}',
            '{"foo_name": "Foo2", "foo_id": "002"}',
        ]
        result = combine_jsons(json_str_list, Foo)
        expected = Foo(foo_name="Foo1", foo_id="001")
        self.assertEqual(result, expected)

    def test_combine_jsons_partial_data(self):
        """Test combining JSON strings with partial data."""
        json_str_list = ['{"foo_name": "Foo1"}', '{"foo_id": "002"}']
        result = combine_jsons(json_str_list, FooTemplate)
        expected = FooTemplate(foo_name="Foo1", foo_id="002")
        self.assertEqual(result, expected)

    @patch.object(settings, "USE_MISTRAL", True)
    def test_combine_jsons_with_mistral_slashes(self):
        """Test combining JSONs with Mistral backslashes."""
        json_str_list = [
            '{\\"foo\_name\\": \\"Foo1\\", \\"foo\_id\\": \\"001\\"}',
            '{\\"foo\_name\\": \\"Foo2\\", \\"foo\_id\\": \\"002\\"}',
        ]
        result = combine_jsons(json_str_list, Foo)
        expected = Foo(foo_name="Foo1", foo_id="001")
        self.assertEqual(result, expected)


class MockModel(BaseModel):
    """Mock model with optional fields."""

    field1: Optional[str] = None
    field2: Optional[list[str]] = None
    field3: Optional[int] = None
    field4: Optional[float] = None
    field5: Optional[datetime] = None


class TestCalculateFillingPercentage(unittest.TestCase):
    """Test calculate_filling_percentage function."""

    def test_all_fields_filled(self):
        """Test filling percentage with all fields filled."""
        model_instance = MockModel(
            field1="value1",
            field2=["value2"],
            field3=123,
            field4=45.67,
            field5=datetime.now(),
        )
        result = calculate_filling_percentage(model_instance)
        self.assertEqual(result, 1.0)

    def test_no_fields_filled(self):
        """Test filling percentage with no fields filled."""
        model_instance = MockModel()
        result = calculate_filling_percentage(model_instance)
        self.assertEqual(result, 0.0)

    def test_some_fields_filled(self):
        """Test filling percentage with some fields filled."""
        model_instance = MockModel(field1="value1", field3=123)
        result = calculate_filling_percentage(model_instance)
        self.assertEqual(result, 2 / 5)

    def test_model_instance_none(self):
        """Test filling percentage with model instance None."""
        result = calculate_filling_percentage(None)
        self.assertEqual(result, 0.0)

    def test_model_instance_empty(self):
        """Test filling percentage with empty model instance."""

        class EmptyModel(BaseModel):
            pass

        model_instance = EmptyModel()
        result = calculate_filling_percentage(model_instance)
        self.assertEqual(result, 0.0)


# Sample data for testing
objectives = {"test_obj": {"prompts": ["Sample user prompt"]}}


class TestExtractFieldFromPrompt(unittest.TestCase):
    """Test extract_field_from_prompt function."""

    @patch("client.Client.generate_text")
    def test_extract_field_success(self, mock_generate_text):
        """Test extracting field successfully."""
        # Setup mock response
        mock_generate_text.return_value = {"text": '{"field_value"}'}

        # Input values
        prompt = "User provided prompt"
        field_name = "field_name"
        field_desc = "A description of the field"
        example = "example_value"
        obj = "SearchObjective"
        client = Client()

        # Expected output
        expected_output = '{"field_value"}'

        # Test
        result = extract_field_from_prompt(
            prompt, field_name, field_desc, example, obj, client
        )
        self.assertEqual(result, expected_output)
        mock_generate_text.assert_called_once()

    @patch("client.Client.generate_text")
    def test_extract_field_unexpected_response_format(self, mock_generate_text):
        """Test extracting field with unexpected response format."""
        # Setup mock response
        mock_generate_text.return_value = {}

        # Input values
        prompt = "User provided prompt"
        field_name = "field_name"
        field_desc = "A description of the field"
        example = "example_value"
        obj = "SearchObjective"
        client = Client()

        # Test
        with self.assertRaises(ValueError):
            extract_field_from_prompt(
                prompt, field_name, field_desc, example, obj, client
            )
        mock_generate_text.assert_called_once()

    @patch("client.Client.generate_text")
    def test_extract_field_detail_in_response(self, mock_generate_text):
        """Test extracting field with detail in response."""
        # Setup mock response
        mock_generate_text.return_value = {"detail": "Detail message"}

        # Input values
        prompt = "User provided prompt"
        field_name = "field_name"
        field_desc = "A description of the field"
        example = "example_value"
        obj = "SearchObjective"
        client = Client()

        # Expected output
        expected_output = "Detail message"

        # Test
        result = extract_field_from_prompt(
            prompt, field_name, field_desc, example, obj, client
        )
        self.assertEqual(result, expected_output)
        mock_generate_text.assert_called_once()


class TestProcessFields(unittest.TestCase):
    """Test process_fields function."""

    @patch("utils.get_model_fields_and_descriptions")
    @patch("utils.extract_field_from_prompt")
    @patch("utils.clean_field_response")
    @patch("utils.is_json_like")
    def test_process_fields_success(
        self,
        mock_is_json_like,
        mock_clean_field_response,
        mock_extract_field_from_prompt,
        mock_get_model_fields_and_descriptions,
    ):
        """Test processing fields successfully."""
        # Setup mock responses
        mock_get_model_fields_and_descriptions.return_value = [
            ("field1", "desc1"),
            ("field2", "desc2"),
        ]
        mock_extract_field_from_prompt.side_effect = [
            '{"field1_value"}',
            '{"field2_value"}',
        ]
        mock_clean_field_response.side_effect = ['{"field1_value"}', '{"field2_value"}']
        mock_is_json_like.side_effect = [True, True]

        # Input values
        prompt = "User provided prompt"
        objective = "SearchObjective"
        client = Client()

        # Expected output
        expected_output = ['{"field1_value"}', '{"field2_value"}']

        # Test
        with patch.dict(
            "utils.objectives",
            {objective: {"base_model": "model_name", "example_fields": ["ex1", "ex2"]}},
        ):
            result = process_fields(prompt, objective, client)
            self.assertEqual(result, expected_output)
            mock_get_model_fields_and_descriptions.assert_called_once_with("model_name")
            self.assertEqual(mock_extract_field_from_prompt.call_count, 2)
            self.assertEqual(mock_clean_field_response.call_count, 2)
            self.assertEqual(mock_is_json_like.call_count, 2)

    @patch("utils.get_model_fields_and_descriptions")
    def test_process_fields_mismatch_examples_fields(
        self, mock_get_model_fields_and_descriptions
    ):
        """Test processing fields with mismatched examples."""
        # Setup mock response
        mock_get_model_fields_and_descriptions.return_value = [
            ("field1", "desc1"),
            ("field2", "desc2"),
        ]

        # Input values
        prompt = "User provided prompt"
        objective = "SearchObjective"
        client = Client()

        # Test
        with patch.dict(
            "utils.objectives",
            {objective: {"base_model": "model_name", "example_fields": ["ex1"]}},
        ):
            with self.assertRaises(ValueError):
                process_fields(prompt, objective, client)
            mock_get_model_fields_and_descriptions.assert_called_once_with("model_name")

    @patch("utils.get_model_fields_and_descriptions")
    @patch("utils.extract_field_from_prompt")
    @patch("utils.clean_field_response")
    @patch("utils.is_json_like")
    def test_process_fields_failed_extraction(
        self,
        mock_is_json_like,
        mock_clean_field_response,
        mock_extract_field_from_prompt,
        mock_get_model_fields_and_descriptions,
    ):
        """Test processing fields with failed extraction."""
        # Setup mock responses
        mock_get_model_fields_and_descriptions.return_value = [("field1", "desc1")]
        mock_extract_field_from_prompt.return_value = "Invalid response"
        mock_clean_field_response.return_value = "Invalid response"
        mock_is_json_like.return_value = False

        # Input values
        prompt = "User provided prompt"
        objective = "SearchObjective"
        client = Client()

        # Expected output
        expected_output = []

        # Test
        with patch.dict(
            "utils.objectives",
            {objective: {"base_model": "model_name", "example_fields": ["ex1"]}},
        ):
            result = process_fields(prompt, objective, client)
            self.assertEqual(result, expected_output)
            mock_get_model_fields_and_descriptions.assert_called_once_with("model_name")
            self.assertEqual(mock_extract_field_from_prompt.call_count, 3)
            self.assertEqual(mock_clean_field_response.call_count, 3)
            self.assertEqual(mock_is_json_like.call_count, 6)


class TestExtractListFromPrompt(unittest.TestCase):
    """Test extract_list_from_prompt function."""

    @patch("client.Client.generate_text")
    def test_extract_list_success(self, mock_generate_text):
        """Test extracting list successfully."""
        # Setup mock response
        mock_generate_text.return_value = {"text": '["RME01", "LMNT01"]'}

        # Input values
        prompt = "User provided prompt"
        field_name = "time_field"
        field_desc = "A description of the time field"
        client = Client()

        # Expected output
        expected_output = '["RME01", "LMNT01"]'

        # Test
        result = extract_list_from_prompt(prompt, field_name, field_desc, client)
        self.assertEqual(result, expected_output)
        mock_generate_text.assert_called_once()

    @patch("client.Client.generate_text")
    def test_extract_list_unexpected_response_format(self, mock_generate_text):
        """Test extracting list with unexpected response format."""
        # Setup mock response
        mock_generate_text.return_value = {}

        # Input values
        prompt = "User provided prompt"
        field_name = "time_field"
        field_desc = "A description of the time field"
        client = Client()

        # Test
        with self.assertRaises(ValueError):
            extract_list_from_prompt(prompt, field_name, field_desc, client)
        mock_generate_text.assert_called_once()

    @patch("client.Client.generate_text")
    def test_extract_list_detail_in_response(self, mock_generate_text):
        """Test extracting list with detail in response."""
        # Setup mock response
        mock_generate_text.return_value = {"detail": "Detail message"}

        # Input values
        prompt = "User provided prompt"
        field_name = "time_field"
        field_desc = "A description of the time field"
        client = Client()

        # Expected output
        expected_output = "Detail message"

        # Test
        result = extract_list_from_prompt(prompt, field_name, field_desc, client)
        self.assertEqual(result, expected_output)
        mock_generate_text.assert_called_once()


class TestProcessLists(unittest.TestCase):
    """Test process_lists function."""

    @patch("utils.get_model_fields_and_descriptions")
    @patch("utils.extract_list_from_prompt")
    @patch("utils.clean_field_response")
    @patch("utils.is_json_like")
    def test_process_lists_success(
        self,
        mock_is_json_like,
        mock_clean_field_response,
        mock_extract_list_from_prompt,
        mock_get_model_fields_and_descriptions,
    ):
        """Test processing lists successfully."""
        # Setup mock responses
        mock_get_model_fields_and_descriptions.return_value = [
            ("list1", "desc1"),
            ("list2", "desc2"),
        ]
        mock_extract_list_from_prompt.side_effect = [
            '["item1", "item2"]',
            '["item3", "item4"]',
        ]
        mock_clean_field_response.side_effect = [
            '["item1", "item2"]',
            '["item3", "item4"]',
        ]
        mock_is_json_like.side_effect = [True, True]

        # Input values
        prompt = "User provided prompt"
        objective = "SearchObjective"
        client = Client()

        # Expected output
        expected_output = ['["item1", "item2"]', '["item3", "item4"]']

        # Test
        with patch.dict("utils.objectives", {objective: {"list_fields": "list_model"}}):
            result = process_lists(prompt, objective, client)
            self.assertEqual(result, expected_output)
            mock_get_model_fields_and_descriptions.assert_called_once_with("list_model")
            self.assertEqual(mock_extract_list_from_prompt.call_count, 2)
            self.assertEqual(mock_clean_field_response.call_count, 2)
            self.assertEqual(mock_is_json_like.call_count, 2)

    def test_process_lists_no_list_fields(self):
        """Test processing lists with no list fields."""
        # Input values
        prompt = "User provided prompt"
        objective = "SearchObjective"
        client = Client()

        # Expected output
        expected_output = []

        # Test
        with patch.dict("utils.objectives", {objective: {"list_fields": None}}):
            result = process_lists(prompt, objective, client)
            self.assertEqual(result, expected_output)

    @patch("utils.get_model_fields_and_descriptions")
    @patch("utils.extract_list_from_prompt")
    @patch("utils.clean_field_response")
    @patch("utils.is_json_like")
    def test_process_lists_failed_extraction(
        self,
        mock_is_json_like,
        mock_clean_field_response,
        mock_extract_list_from_prompt,
        mock_get_model_fields_and_descriptions,
    ):
        """Test processing lists with failed extraction."""
        # Setup mock responses
        mock_get_model_fields_and_descriptions.return_value = [("list1", "desc1")]
        mock_extract_list_from_prompt.return_value = "Invalid response"
        mock_clean_field_response.return_value = "Invalid response"
        mock_is_json_like.return_value = False

        # Input values
        prompt = "User provided prompt"
        objective = "SearchObjective"
        client = Client()

        # Expected output
        expected_output = []

        # Test
        with patch.dict("utils.objectives", {objective: {"list_fields": "list_model"}}):
            result = process_lists(prompt, objective, client)
            self.assertEqual(result, expected_output)
            mock_get_model_fields_and_descriptions.assert_called_once_with("list_model")
            self.assertEqual(mock_extract_list_from_prompt.call_count, 3)
            self.assertEqual(mock_clean_field_response.call_count, 3)
            self.assertEqual(mock_is_json_like.call_count, 6)


class TestExtractTimeFromPrompt(unittest.TestCase):
    """Test extract_time_from_prompt function."""

    @patch("utils.get_current_time")
    @patch("client.Client.generate_text")
    def test_extract_time_success(self, mock_generate_text, mock_get_current_time):
        """Test extracting time successfully."""
        # Setup mock responses
        mock_get_current_time.return_value = "2024-05-21 19:22:22.650000+00:00"
        mock_generate_text.return_value = {"text": '"2024-05-21 19:22:22.650000+00:00"'}

        # Input values
        prompt = "User provided prompt"
        field_name = "time_field"
        field_desc = "A description of the time field"
        client = Client()

        # Expected output
        expected_output = '"2024-05-21 19:22:22.650000+00:00"'

        # Test
        result = extract_time_from_prompt(prompt, field_name, field_desc, client)
        self.assertEqual(result, expected_output)
        mock_generate_text.assert_called_once()
        mock_get_current_time.assert_called_once()

    @patch("utils.get_current_time")
    @patch("client.Client.generate_text")
    def test_extract_time_unexpected_response_format(
        self, mock_generate_text, mock_get_current_time
    ):
        """Test extracting time with unexpected response format."""
        # Setup mock responses
        mock_get_current_time.return_value = "2024-05-21 19:22:22.650000+00:00"
        mock_generate_text.return_value = {}

        # Input values
        prompt = "User provided prompt"
        field_name = "time_field"
        field_desc = "A description of the time field"
        client = Client()

        # Test
        with self.assertRaises(ValueError):
            extract_time_from_prompt(prompt, field_name, field_desc, client)
        mock_generate_text.assert_called_once()
        mock_get_current_time.assert_called_once()

    @patch("utils.get_current_time")
    @patch("client.Client.generate_text")
    def test_extract_time_detail_in_response(
        self, mock_generate_text, mock_get_current_time
    ):
        """Test extracting time with detail in response."""
        # Setup mock responses
        mock_get_current_time.return_value = "2024-05-21 19:22:22.650000+00:00"
        mock_generate_text.return_value = {"detail": "Detail message"}

        # Input values
        prompt = "User provided prompt"
        field_name = "time_field"
        field_desc = "A description of the time field"
        client = Client()

        # Expected output
        expected_output = "Detail message"

        # Test
        result = extract_time_from_prompt(prompt, field_name, field_desc, client)
        self.assertEqual(result, expected_output)
        mock_generate_text.assert_called_once()
        mock_get_current_time.assert_called_once()


class TestProcessTimes(unittest.TestCase):
    """Test process_times function."""

    @patch("utils.get_model_fields_and_descriptions")
    @patch("utils.extract_time_from_prompt")
    @patch("utils.clean_json_str")
    @patch("utils.is_json_like")
    def test_process_times_success(
        self,
        mock_is_json_like,
        mock_clean_json_str,
        mock_extract_time_from_prompt,
        mock_get_model_fields_and_descriptions,
    ):
        """Test processing times successfully."""
        # Setup mock responses
        mock_get_model_fields_and_descriptions.return_value = [
            ("time1", "desc1"),
            ("time2", "desc2"),
        ]
        mock_extract_time_from_prompt.side_effect = [
            '{"start_time": "2023-06-01T09:00:00"}',
            '{"end_time": "2023-06-01T17:00:00"}',
        ]
        mock_clean_json_str.side_effect = [
            '{"start_time": "2023-06-01T09:00:00"}',
            '{"end_time": "2023-06-01T17:00:00"}',
        ]
        mock_is_json_like.side_effect = [True, True]

        # Input values
        prompt = "User provided prompt"
        client = Client()

        # Expected output
        expected_output = [
            '{"start_time": "2023-06-01T09:00:00"}',
            '{"end_time": "2023-06-01T17:00:00"}',
        ]

        # Test
        result = process_times(prompt, client)
        self.assertEqual(result, expected_output)
        mock_get_model_fields_and_descriptions.assert_called_once_with(ObjectiveTime)
        self.assertEqual(mock_extract_time_from_prompt.call_count, 2)
        self.assertEqual(mock_clean_json_str.call_count, 2)
        self.assertEqual(mock_is_json_like.call_count, 2)

    @patch("utils.get_model_fields_and_descriptions")
    @patch("utils.extract_time_from_prompt")
    @patch("utils.clean_json_str")
    @patch("utils.is_json_like")
    def test_process_times_failed_extraction(
        self,
        mock_is_json_like,
        mock_clean_json_str,
        mock_extract_time_from_prompt,
        mock_get_model_fields_and_descriptions,
    ):
        """Test processing times with failed extraction."""
        # Setup mock responses
        mock_get_model_fields_and_descriptions.return_value = [("time1", "desc1")]
        mock_extract_time_from_prompt.return_value = "Invalid response"
        mock_clean_json_str.return_value = "Invalid response"
        mock_is_json_like.return_value = False

        # Input values
        prompt = "User provided prompt"
        client = Client()

        # Expected output
        expected_output = []

        # Test
        result = process_times(prompt, client)
        self.assertEqual(result, expected_output)
        mock_get_model_fields_and_descriptions.assert_called_once_with(ObjectiveTime)
        self.assertEqual(mock_extract_time_from_prompt.call_count, 3)
        self.assertEqual(mock_clean_json_str.call_count, 3)
        self.assertEqual(mock_is_json_like.call_count, 6)

    @patch("utils.get_model_fields_and_descriptions")
    @patch("utils.extract_time_from_prompt")
    @patch("utils.clean_json_str")
    @patch("utils.is_json_like")
    def test_process_times_success_cleaned_response(
        self,
        mock_is_json_like,
        mock_clean_json_str,
        mock_extract_time_from_prompt,
        mock_get_model_fields_and_descriptions,
    ):
        """Test processing times with cleaned response."""
        # Setup mock responses
        mock_get_model_fields_and_descriptions.return_value = [("time1", "desc1")]
        mock_extract_time_from_prompt.return_value = (
            '{"cleaned_time": "2023-06-01T12:00:00"}'
        )
        mock_clean_json_str.return_value = '{"cleaned_time": "2023-06-01T12:00:00"}'
        mock_is_json_like.side_effect = [False, True]

        # Input values
        prompt = "User provided prompt"
        client = Client()

        # Expected output
        expected_output = ['{"cleaned_time": "2023-06-01T12:00:00"}']

        # Test
        result = process_times(prompt, client)
        self.assertEqual(result, expected_output)
        mock_get_model_fields_and_descriptions.assert_called_once_with(ObjectiveTime)
        mock_extract_time_from_prompt.assert_called_once()
        mock_clean_json_str.assert_called_once()
        self.assertEqual(mock_is_json_like.call_count, 2)


# Sample data for testing
cmo_info = {
    "example": "CatalogMaintenanceObjective",
    "description": "Description for CMO",
    "prompts": ["CMO prompt"],
}
pro_info = {
    "example": "PeriodicRevisitObjective",
    "description": "Description for PRO",
    "prompts": ["PRO prompt"],
}
so_info = {
    "example": "SearchObjective",
    "description": "Description for SO",
    "prompts": ["SO prompt"],
}
deo_info = {
    "example": "DataEnrichmentObjective",
    "description": "Description for DEO",
    "prompts": ["DEO prompt"],
}
sco_info = {
    "example": "SpectralClearingObjective",
    "description": "Description for SCO",
    "prompts": ["SCO prompt"],
}


class TestExtractObjective(unittest.TestCase):
    """Test extract_time_from_prompt function."""

    @patch("client.Client.generate_text")
    def test_extract_objective_success(self, mock_generate_text):
        """Test successful extraction of objective."""
        # Setup mock response
        mock_generate_text.return_value = {"text": '{"objective": "SearchObjective"}'}

        # Input values
        prompt = "User provided prompt"
        client = Client()

        # Expected output
        expected_output = '{"objective": "SearchObjective"}'

        # Test
        result = extract_objective(prompt, client)
        self.assertEqual(result, expected_output)
        mock_generate_text.assert_called_once()

    @patch("client.Client.generate_text")
    def test_extract_objective_unexpected_response_format(self, mock_generate_text):
        """Test unexpected extraction of objective."""
        # Setup mock response
        mock_generate_text.return_value = {}

        # Input values
        prompt = "User provided prompt"
        client = Client()

        # Test
        with self.assertRaises(ValueError):
            extract_objective(prompt, client)
        mock_generate_text.assert_called_once()

    @patch("client.Client.generate_text")
    def test_extract_objective_detail_in_response(self, mock_generate_text):
        """Test extracting objective with detail in response."""
        # Setup mock response
        mock_generate_text.return_value = {"detail": "Detail message"}

        # Input values
        prompt = "User provided prompt"
        client = Client()

        # Expected output
        expected_output = "Detail message"

        # Test
        result = extract_objective(prompt, client)
        self.assertEqual(result, expected_output)
        mock_generate_text.assert_called_once()


class TestModelToJson(unittest.TestCase):
    """Test model_to_json function."""

    def test_model_to_json_with_Foo(self):
        """Test converting Foo model to JSON."""
        model = Foo(foo_name="Test Foo", foo_id="123")
        expected_json = json.dumps({"foo_name": "Test Foo", "foo_id": "123"}, indent=2)
        self.assertEqual(model_to_json(model), expected_json)

    def test_model_to_json_with_FooTemplate(self):
        """Test converting FooTemplate model to JSON."""
        model = FooTemplate(foo_name="Test Foo Template")
        expected_json = json.dumps({"foo_name": "Test Foo Template"}, indent=2)
        self.assertEqual(model_to_json(model), expected_json)

    def test_model_to_json_with_FooTemplate_empty(self):
        """Test converting empty FooTemplate model to JSON."""
        model = FooTemplate()
        expected_json = json.dumps({}, indent=2)
        self.assertEqual(model_to_json(model), expected_json)


class TesObjective(BaseModel):
    patience_minutes: Optional[Union[int, str]] = None
    revisits_per_hour: Optional[Union[float, str]] = None
    hours_to_plan: Optional[Union[float, str]] = None
    number_of_frames: Optional[Union[int, str]] = None
    integration_time: Optional[Union[float, str]] = None
    binning: Optional[Union[int, str]] = None
    priority: Optional[Union[int, str]] = None


class TestPostProcessModel(unittest.TestCase):
    def test_post_process_model_with_valid_int_str(self):
        """Test post-process of int Pydantic model."""
        model = TesObjective(
            patience_minutes="10",
            number_of_frames="5",
            binning="2",
            priority="1",
        )
        processed_model = post_process_model(model)
        assert processed_model.patience_minutes == 10
        assert processed_model.number_of_frames == 5
        assert processed_model.binning == 2
        assert processed_model.priority == 1

    def test_post_process_model_with_valid_float_str(self):
        """Test post-process of float Pydantic model."""
        model = TesObjective(
            revisits_per_hour="2.5",
            hours_to_plan="3.7",
            integration_time="1.5",
        )
        processed_model = post_process_model(model)
        assert processed_model.revisits_per_hour == 2.5
        assert processed_model.hours_to_plan == 3.7
        assert processed_model.integration_time == 1.5

    def test_post_process_model_with_invalid_str(self):
        """Test post-process of invalid Pydantic model."""
        model = TesObjective(
            patience_minutes="invalid",
            number_of_frames="not_a_number",
            binning="invalid_binning",
            priority="high",
        )
        processed_model = post_process_model(model)
        assert processed_model.patience_minutes is None
        assert processed_model.number_of_frames is None
        assert processed_model.binning is None
        assert processed_model.priority is None

    def test_post_process_model_with_none_values(self):
        """Test post-process of Pydantic model with Nones."""
        model = TesObjective()
        processed_model = post_process_model(model)
        assert processed_model.patience_minutes is None
        assert processed_model.revisits_per_hour is None
        assert processed_model.hours_to_plan is None
        assert processed_model.number_of_frames is None
        assert processed_model.integration_time is None
        assert processed_model.binning is None
        assert processed_model.priority is None


if __name__ == "__main__":
    unittest.main()
