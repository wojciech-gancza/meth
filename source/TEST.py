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
        
class test_of_list_walker(unittest.TestCase):

    def test_of_construction(self):
        lines = [
            "1", 
            "22",
            "333" ]
        walker = list_walker(lines)
        self.assertEqual(walker.lines_array, ["1", "22", "333"])
        self.assertEqual(walker.lines_count, 3)
        self.assertEqual(walker.current_line, 0)
        
    def test_of_checking_end(self):
        lines = [
            "1", 
            "22",
            "333" ]
        walker = list_walker(lines)
        self.assertFalse(walker.is_end())
        walker.get_line()
        self.assertFalse(walker.is_end())
        walker.get_line()
        self.assertFalse(walker.is_end())
        walker.get_line()
        self.assertTrue(walker.is_end())
        
    def test_of_reading_content(self):
        lines = [
            "1", 
            "22",
            "333" ]
        walker = list_walker(lines)
        value = walker.get_line()
        self.assertEqual(str(value), "1")
        self.assertEqual(type(value), line_content)
        value = walker.get_line()
        self.assertEqual(str(value), "22")
        value = walker.get_line()
        self.assertEqual(str(value), "333")
        value = walker.get_line()
        self.assertTrue(value is None)
    
    def test_of_push_back(self):
        lines = [
            "1", 
            "22",
            "333" ]
        walker = list_walker(lines)
        value = walker.get_line()
        value = walker.get_line()
        walker.push_back(["4444", "55555"])
        value = walker.get_line()
        self.assertEqual(str(value), "4444")
        value = walker.get_line()
        self.assertEqual(str(value), "55555")
        value = walker.get_line()
        self.assertEqual(str(value), "333")
        self.assertEqual(walker.lines_array, ["1", "4444", "55555", "333"])
 
    def test_of_searchig_line(self):
        lines = [
            "1", 
            "22   ",
            "333",
            "4444",
            "55555" ]
        walker = list_walker(lines)
        
        walker.go_to_line_with("333")
        value = walker.get_line()
        self.assertEqual(str(value), "4444")
        
        walker.go_to_line_with(" 22")
        value = walker.get_line()
        self.assertEqual(str(value), "333")
        
        walker.go_to_line_with(" 2   2")
        self.assertTrue(walker.is_end())
        
    def test_of_skiping_till_end_of_block(self):
        lines = [
            "a", 
            "b",
            "// -^^^",
            "c",
            "d",
            "// -^^^",
            "e",
            "f" ]
        walker = list_walker(lines)
        
        walker.go_to_end_of_content_block()
        value = walker.get_line()
        self.assertEqual(str(value), "c")
        
        walker.go_to_end_of_content_block()
        value = walker.get_line()
        self.assertEqual(str(value), "e")
        
        walker.go_to_end_of_content_block()
        self.assertTrue(walker.is_end())
        
class test_of_code_generator(unittest.TestCase):
    """
    def test_of_define(self):
        self.assertTrue(False)
        
    def test_of_set_template(self):
        self.assertTrue(False)
     
    def test_of_generate(self):
        self.assertTrue(False)
        
    def test_of_transform(self):
        self.assertTrue(False)
 
    def test_of_combine_with_user_code(self):
        self.assertTrue(False)  
    
    def test_of_process_line(self):
        self.assertTrue(False)
    
    def test_of_calculate_result(self):
        self.assertTrue(False)

    def test_of_combine_lines_from(self):
        self.assertTrue(False)
    """  
    def test_of_whitespace_text(self):
        builder = code_generator(globals())
        
        whitespaced = builder._whitespace_text("   xx")
        self.assertEqual(whitespaced, "     ")
        
        whitespaced = builder._whitespace_text(" \t \r  x x \nssddfd")
        self.assertEqual(whitespaced, " \t \r      \n      ")
        
        whitespaced = builder._whitespace_text("")
        self.assertEqual(whitespaced, "")
    
    def test_of_copy_lines_till_end_of_block(self):
        source = [
            "abcd",
            "1",
            "2",
            "3",
            "// -^^^",
            "end" ]
        target = [ ]
        walker = list_walker(source)
        walker.get_line()
        builder = code_generator(globals())
        builder._copy_lines(walker, target)
        self.assertEqual(target, ["1", "2", "3", "// -^^^"])
        self.assertFalse(walker.is_end())
        line = walker.get_line()
        self.assertEqual(str(line), "end")
        
    def test_of_copy_lines_till_end_data(self):
        source = [
            "abcd",
            "1",
            "2",
            "3",
            "end" ]
        target = [ ]
        walker = list_walker(source)
        walker.get_line()
        builder = code_generator(globals())
        builder._copy_lines(walker, target)
        self.assertEqual(target, ["1", "2", "3", "end"])
        self.assertTrue(walker.is_end())
    
# -------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main()

# -------------------------------------------------------------------
