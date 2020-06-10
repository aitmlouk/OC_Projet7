"""
parserquery module tests,
use pytest
"""

import grandpyapp.utils.parserquery as script


class TestParseQuery:

    TEXT_TO_PARSE_QUERY = "dis moi tout sur Rennes"
    TEXT_TO_PARSE_OTHER_WORDS = "bonjour grandpy rennes"
    TEXT_TO_SLUYGIFY = "àèôùûï/{ ok +-*/?."
    TEXT_TO_PARSE_JSON_WORDS = "grandpy allons absolument"
    TEXT_TO_PARSE_FULL = "Grand py, dis moi tout sur RêNNES?"

    QUERY_TO_DELETE = ['dis moi tout sur']
    OTHER_WORDS = ['grandpy', 'bonjour']

    def test_slugify(self):
        parser_query = script.ParserQuery(self.TEXT_TO_SLUYGIFY)
        text_slugify = parser_query.slugify_text(parser_query.text_to_parse)
        assert text_slugify == "aeouui ok"

    def test_delete_expression_with_true(self):
        parser_query = script.ParserQuery(self.TEXT_TO_PARSE_QUERY)
        parser_query.delete_expression(self.QUERY_TO_DELETE, True)
        assert parser_query.text_to_parse == "Rennes"

    def test_delete_expression_with_false(self):
        parser_query = script.ParserQuery(self.TEXT_TO_PARSE_OTHER_WORDS)
        parser_query.delete_expression(self.OTHER_WORDS)
        assert parser_query.text_to_parse == "rennes"

    def test_read_json(self):
        parser_query = script.ParserQuery("test json")
        assert parser_query.read_json()

    def test_delete_words(self):
        parser_query = script.ParserQuery(self.TEXT_TO_PARSE_JSON_WORDS)
        parser_query.delete_words()
        assert parser_query.text_to_parse == "grandpy"

    def test_clean_text(self):
        parser_query = script.ParserQuery(self.TEXT_TO_PARSE_FULL)
        parser_query.clean_text()
        assert parser_query.text_parsed == "rennes"
