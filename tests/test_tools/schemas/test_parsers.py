import unittest

from ai_cmd.tools.schemas.parsers import DocstringParser


class TestDocstringParser(unittest.TestCase):

    def test_parse_empty_docstring(self):
        description, params = DocstringParser.parse("")
        self.assertEqual(description, "")
        self.assertEqual(params, {})

    def test_parse_simple_description(self):
        docstring = """This is a simple description."""
        description, params = DocstringParser.parse(docstring)
        self.assertEqual(description, "This is a simple description.")
        self.assertEqual(params, {})

    def test_parse_with_parameters(self):
        docstring = """This is a description.\n\n        Args:
            param1: Description of param1
            param2: Description of param2
        """
        description, params = DocstringParser.parse(docstring)
        self.assertEqual(description, "This is a description.")
        self.assertEqual(
            params,
            {"param1": "Description of param1", "param2": "Description of param2"},
        )

    def test_parse_with_multiple_lines_description(self):
        docstring = """This is the first line of the description.
        This is the second line.

        Args:
            param1: Description of param1
        """
        description, params = DocstringParser.parse(docstring)
        self.assertEqual(
            description,
            "This is the first line of the description. This is the second line.",
        )
        self.assertEqual(params, {"param1": "Description of param1"})

    def test_parse_with_parameter_without_description(self):
        docstring = """This is a description.\n\n        Args:
            param1:
        """
        description, params = DocstringParser.parse(docstring)
        self.assertEqual(description, "This is a description.")
        self.assertEqual(params, {"param1": ""})

    def test_parse_with_args_section(self):
        docstring = """This is a description.\n\n        Args:
            param1: Description of param1
        """
        description, params = DocstringParser.parse(docstring)
        self.assertEqual(description, "This is a description.")
        self.assertEqual(params, {"param1": "Description of param1"})

    def test_parse_with_parameters_section(self):
        docstring = """This is a description.\n\n        Parameters:
            param1: Description of param1
        """
        description, params = DocstringParser.parse(docstring)
        self.assertEqual(description, "This is a description.")
        self.assertEqual(params, {"param1": "Description of param1"})

    def test_parse_with_params_section(self):
        docstring = """This is a description.\n\n        Params:
            param1: Description of param1
        """
        description, params = DocstringParser.parse(docstring)
        self.assertEqual(description, "This is a description.")
        self.assertEqual(params, {"param1": "Description of param1"})

    def test_parse_google_docstring(self):
        docstring = """This is a description.\n\n        Args:
            param1 (str): Description of param1
        """
        description, params = DocstringParser.parse(docstring)
        self.assertEqual(description, "This is a description.")
        self.assertEqual(params, {"param1": "Description of param1"})

    def test_parse_numpy_docstring(self):
        docstring = """This is a description.\n\n        Parameters
        ----------
        param1 : str
            Description of param1
        """
        description, params = DocstringParser.parse(docstring)
        self.assertEqual(description, "This is a description.")
        self.assertEqual(params, {"param1": "Description of param1"})

    def test_parse_docstring_with_unicode(self):
        docstring = """This is a description with ünicode.\n\n        Args:
            param1: Description of param1 with ünicode
        """
        description, params = DocstringParser.parse(docstring)
        self.assertEqual(description, "This is a description with ünicode.")
        self.assertEqual(params, {"param1": "Description of param1 with ünicode"})

    def test_parse_docstring_with_special_chars(self):
        docstring = """This is a description with !@#$%^&*().\n\n        Args:
            param1: Description of param1 with !@#$%^&*()
        """
        description, params = DocstringParser.parse(docstring)
        self.assertEqual(description, "This is a description with !@#$%^&*().")
        self.assertEqual(params, {"param1": "Description of param1 with !@#$%^&*()"})

    def test_parse_docstring_with_rst_format(self):
        docstring = """This is a description.\n\n        :param param1: Description of param1
        :type param1: str
        """
        description, params = DocstringParser.parse(docstring)
        self.assertEqual(description, "This is a description.")
        self.assertEqual(params, {"param": "Description of param1"})

    def test_parse_docstring_with_multiline_param_description(self):
        docstring = """This is a description.\n\n        Args:
            param1: This is the first line of the description for param1.\n                This is the second line.
        """
        description, params = DocstringParser.parse(docstring)
        self.assertEqual(description, "This is a description.")
        self.assertEqual(
            params,
            {
                "param1": "This is the first line of the description for param1. This is the second line."
            },
        )

    def test_parse_docstring_with_complex_type_hint(self):
        docstring = """This is a description.\n\n        Args:
            param1 (list[str]): Description of param1
        """
        description, params = DocstringParser.parse(docstring)
        self.assertEqual(description, "This is a description.")
        self.assertEqual(params, {"param1": "Description of param1"})


if __name__ == "__main__":
    unittest.main()
