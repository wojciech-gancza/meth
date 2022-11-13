# -------------------------------------------------------------------

# matagenerator 
# WGan 2022
# Open source
# freeware

import unittest
import os

from meth       import  code_generator,     code_block,     \
                        target_content,     file_lines,     \
                        result_file,        line_content,   \
                        code_block,         list_walker,    \
                        code_generator
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
    def copy_file(source, target):
        with open(source, "r") as source_file:
            file_content = source_file.read()
            with open(target, "w") as target_file:
                target_file.write(file_content)
    
    @staticmethod
    def compare_file(pattern, found):
        with open(pattern, "r") as pattern_file:
            pattern_content = pattern_file.read()
            with open(found, "r") as found_file:
                found_content = found_file.read()
                return pattern_content == found_content
                
    @staticmethod
    def delete_file(name):
        if os.path.exists(name):
            os.remove(name)
    
    @staticmethod
    def read_file(name):
        with open(name, "r") as file:
            return file.read()

class test_of_functionality(unittest.TestCase):

    def test_of_generation_of_file_01(self):
        template            = "../test/01-1-source_template.cpp"
        previous_result     = "../test/01-2-existing_content.cpp"
        expected_result     = "../test/01-3-expected_result.cpp"
        generated_result    = "../test/_generated/01-3-result.cpp"
        
        test_tools.copy_file(previous_result, generated_result)
        
        builder = code_generator(globals())
        builder.set_template(template)
        builder.define("name", general_name("hello World"))
        builder.define("fname", "a_function")
        builder.define("enum_list", ["FIRST", "SECOND", "THIRD", "AND_FINALLY_FORTH", "LAST"])
        builder.generate(generated_result)
          
        self.assertTrue(test_tools.compare_file(expected_result, generated_result))

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

class test_of_file_lines(unittest.TestCase):

    def test_of_reading_exisitng_file(self):
        file_name = "../test/02-1-example_of_file.txt"
        file = file_lines(file_name)
        self.assertEqual(len(file), 4)
        self.assertEqual(file[1], "with few lines")

    def test_of_reading_nonexisitng_file(self):
        file_name = "../test/02-2-example_of_file.txt"
        try:
            file = file_lines(file_name)
            self.assertTrue(False)
        except FileNotFoundError as err:
            pass
        except Exception:
            self.assertTrue(False)

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

class test_of_result_file(unittest.TestCase):

    def test_of_storing_multiline_message(self):
        data_to_store = [   
            "First line", 
            "Second line", 
            "",
            "End of file" ]
        generated_result = "../test/_generated/02-1-result.cpp"
        test_tools.delete_file(generated_result)
        file = result_file(data_to_store)
        file.store(generated_result)
        file_content = test_tools.read_file(generated_result)
        self.assertEqual(file_content, "\n".join(data_to_store))

class test_of_line_content(unittest.TestCase):

    def test_get_placeholder(self):
        line = line_content("// -vvv")
        placeholder = line.get_placeholder()
        self.assertTrue(placeholder is None)
        line = line_content("${placeholder}")
        placeholder = line.get_placeholder()
        self.assertEqual(placeholder.start(0), 0)
        self.assertEqual(placeholder.end(0), 14)
        line = line_content("something ${placeholder} and something else")
        placeholder = line.get_placeholder()
        self.assertEqual("${placeholder}", str(line)[placeholder.start(0):placeholder.end()])
        line = line_content("something ${place${inner}holder} and something else")
        placeholder = line.get_placeholder()
        self.assertEqual("${inner}", str(line)[placeholder.start(0):placeholder.end()])        
        
    def test_is_persistent_block_begin(self):
        line = line_content("// -vvv")
        self.assertTrue(line.is_persistent_block_begin())
        line = line_content("// -^^^")
        self.assertFalse(line.is_persistent_block_begin())
        line = line_content("// -vvv any trailing text")
        self.assertTrue(line.is_persistent_block_begin())
        line = line_content("      // -vvv trailing witespaces")
        self.assertTrue(line.is_persistent_block_begin())
        line = line_content("      // just a comment")
        self.assertFalse(line.is_persistent_block_begin())
        line = line_content("// -vv")
        self.assertFalse(line.is_persistent_block_begin())
        line = line_content("")
        self.assertFalse(line.is_persistent_block_begin())
        
    def test_is_persistent_block_end(self):
        line = line_content("// -^^^")
        self.assertTrue(line.is_persistent_block_end())
        line = line_content("// -vvv")
        self.assertFalse(line.is_persistent_block_end())
        line = line_content("// -^^^ any trailing text")
        self.assertTrue(line.is_persistent_block_end())
        line = line_content("      // -^^^ trailing witespaces")
        self.assertTrue(line.is_persistent_block_end())
        line = line_content("      // just a comment")
        self.assertFalse(line.is_persistent_block_end())
        line = line_content("// -^^")
        self.assertFalse(line.is_persistent_block_end())
        line = line_content("")
        self.assertFalse(line.is_persistent_block_end())   
        
    def test_get_string(self):
        text = "any text in one line"
        line = line_content(text)
        line_text = str(line)
        self.assertEqual(text, line_text)

class test_of_code_block(unittest.TestCase):

    def test_of_code_block_content(self):
        block = code_block(["first", "second", "third", "fourth"])
        self.assertTrue(type(block) is code_block)
        self.assertEqual(block.get_list_of_lines(), ["first", "second", "third", "fourth"])
        
"""     
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
