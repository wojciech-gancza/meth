# -------------------------------------------------------------------

# matagenerator 
# WGan 2022
# Open source
# freeware

import unittest

from meth       import  code_generator,     code_block,     target_content
from tools      import  general_name

# -------------------------------------------------------------------

# functios and classes needed for test

def generate_some_code_with_placeholders_and_user_code_block():
    return code_block([ "void ${fname}", 
                            "{", 
                            "    // -vvv ${fname} user code", 
                            "    // by default - do nothing",
                            "    // -^^^ end of user code. do not modify",
                            "}"])

# -------------------------------------------------------------------

# functional tests

class test_tools:

    @staticmethod
    def _copy_file(source, target):
        with open(source, "r") as source_file:
            file_content = source_file.read()
            with open(target, "w") as target_file:
                target_file.write(file_content)
    
    @staticmethod
    def _compare_file(pattern, found):
        with open(pattern, "r") as pattern_file:
            pattern_content = pattern_file.read()
            with open(found, "r") as found_file:
                found_content = found_file.read()
                return pattern_content == found_content

class test_of_functionality(unittest.TestCase):

    def test_of_generation_of_file_01(self):
        template            = "../test/01-1-source_template.cpp"
        previous_result     = "../test/01-2-existing_content.cpp"
        expected_result     = "../test/01-3-expected_result.cpp"
        generated_result    = "../test/_generated/01-3-result.cpp"
        
        test_tools._copy_file(previous_result, generated_result)
        
        builder = code_generator(globals())
        builder.set_template(template)
        builder.define("name", general_name("hello World"))
        builder.define("fname", "a_function")
        builder.define("enum_list", ["FIRST", "SECOND", "THIRD", "AND_FINALLY_FORTH", "LAST"])
        builder.generate(generated_result)
          
        self.assertTrue(test_tools._compare_file(expected_result, generated_result))

class test_of_general_name_tool(unittest.TestCase):

    def setUp(self):
        self.id1 = general_name("")
        self.id2 = general_name("hello")
        self.id3 = general_name("more then one word")
        self.id4 = general_name("few Words DENOTED difFerently") 

    def test_of_CamelCase(self):
        self.assertEqual(self.id1.CamelCase(), "")
        self.assertEqual(self.id2.CamelCase(), "Hello")
        self.assertEqual(self.id3.CamelCase(), "MoreThenOneWord")
        self.assertEqual(self.id4.CamelCase(), "FewWordsDenotedDifferently")

    def test_of_lowercaseCamel(self):
        self.assertEqual(self.id1.lowercaseCamel(), "")
        self.assertEqual(self.id2.lowercaseCamel(), "hello")
        self.assertEqual(self.id3.lowercaseCamel(), "moreThenOneWord")
        self.assertEqual(self.id4.lowercaseCamel(), "fewWordsDenotedDifferently")

    def test_of_lowercase(self):
        self.assertEqual(self.id1.lowercase(), "")
        self.assertEqual(self.id2.lowercase(), "hello")
        self.assertEqual(self.id3.lowercase(), "more_then_one_word")
        self.assertEqual(self.id4.lowercase(), "few_words_denoted_differently")

    def test_of_UPPERCASE(self):
        self.assertEqual(self.id1.UPPERCASE(), "")
        self.assertEqual(self.id2.UPPERCASE(), "HELLO")
        self.assertEqual(self.id3.UPPERCASE(), "MORE_THEN_ONE_WORD")
        self.assertEqual(self.id4.UPPERCASE(), "FEW_WORDS_DENOTED_DIFFERENTLY")

"""
class test_of_file_lines(unittest.TestCase):

    def test_not_implemented(self):
        self.assertTrue(False, "Test not implemented")
"""

class test_of_target_content(unittest.TestCase):

    def test_of_reading_exisitng_file(self):
        file_name = "../test/02-1-example_of_file.txt"
        file = target_content(file_name)
        self.assertEqual(len(file), 4)
        self.assertEqual(file[1], "with few lines")

    def test_of_reading_nonexisitng_file(self):
        file_name = "../test/02-2-example_of_file.txt"
        file = target_content(file_name)
        self.assertEqual(len(file), 0)

"""     
class test_of_result_file(unittest.TestCase):

    def test_not_implemented(self):
        self.assertTrue(False, "Test not implemented")

class test_of_line_content(unittest.TestCase):

    def test_not_implemented(self):
        self.assertTrue(False, "Test not implemented")

class test_of_code_block(unittest.TestCase):

    def test_not_implemented(self):
        self.assertTrue(False, "Test not implemented")
        
class test_of_list_walker(unittest.TestCase):

    def test_not_implemented(self):
        self.assertTrue(False, "Test not implemented")
    
class test_of_code_generator(unittest.TestCase):

    def test_not_implemented(self):
        self.assertTrue(False, "Test not implemented")
"""    
    
# -------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main()

# -------------------------------------------------------------------
