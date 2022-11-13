# -------------------------------------------------------------------

# matagenerator 
# WGan 2022
# Open source
# freeware

import unittest

from meth import code_generator, code_block
from tools import general_name

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

class test_of_functionality(unittest.TestCase):

    def _copy_file(self, source, target):
        with open(source, "r") as source_file:
            file_content = source_file.read()
            with open(target, "w") as target_file:
                target_file.write(file_content)
    
    def _compare_file(self, pattern, found):
        with open(pattern, "r") as pattern_file:
            pattern_content = pattern_file.read()
            with open(found, "r") as found_file:
                found_content = found_file.read()
                return pattern_content == found_content

    def test_of_generation_of_file_01(self):
        template            = "../test/01-1-source_template.cpp"
        previous_result     = "../test/01-2-existing_content.cpp"
        expected_result     = "../test/01-3-expected_result.cpp"
        generated_result    = "../test/_generated/01-3-result.cpp"
        self._copy_file(previous_result, generated_result)
        
        builder = code_generator(globals())
        builder.set_template(template)
        builder.define("name", general_name("hello World"))
        builder.define("fname", "a_function")
        builder.define("enum_list", ["FIRST", "SECOND", "THIRD", "AND_FINALLY_FORTH", "LAST"])
        builder.generate(generated_result)
          
        self.assertTrue(self._compare_file(expected_result, generated_result))

# -------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main()

# -------------------------------------------------------------------
