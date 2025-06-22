#--------------------------------------------------------------------------

import unittest
import meth
import methtools
import generator
import generatortools
import os
import time

#--------------------------------------------------------------------------
# backlog:
#--------------------------------------------------------------------------
# -! simple types generator
#   -- collection type
#   -- registry of all generated types
#   -- adding tool files (when required)
#   ++ bitflags type 
#   ++ enum type
#   ++ integer type
#   ++ record type
#   ++ float type (based on float/double)
#   ++ string type
#   ++ timepoint type
#   ++ patterns refactoring
#   ++ time duration type
# -- configuration
#   -- configuration types: key, value, node, nodes
#   -- add reading objects from cofiguration (all types)
# ++ fixing problems
#   ++ converting string->enum - check length of the string first. Problem with too bix index
# ++ main part of metagenerator
#   ++ functionality as previos version +...
#--------------------------------------------------------------------------

class TestEnvironment:

    def __init__(self, subdirectory):
        self.script_path = generatortools.AbsolutePath( __file__).parent()
        self.patterns_path = self.script_path.create_changed_by("patterns")
        self.output_path = self.script_path.create_changed_by("development/testdata/outputs")
        self.cpp_output_path = self.script_path.create_changed_by("development/test-of-generated-code")
        self.sample_files_path = self.script_path.create_changed_by("development/testdata/" + subdirectory)

    def check_output_file(self, file_name):
        file_to_check = methtools.FileContent(self.output_path.get_as_directory() + file_name)
        sample_file = methtools.FileContent(self.sample_files_path.get_as_directory() + file_name + ".good")
        return file_to_check.text == sample_file.text
    
    def prepare_old_output_file(self, file_name):
        file_copy = methtools.FileContent(self.sample_files_path.get_as_directory() + file_name + ".before")
        copied_file = methtools.OutputFile(self.output_path.get_as_directory() + file_name)
        copied_file.save(file_copy.text)
        os.utime(copied_file.file_name ,(1330712280, 1330712292))

    def is_output_file_old(self, file_name):
        modification_time = time.ctime(os.path.getmtime(self.output_path.get_as_directory() + file_name))
        modification_year = modification_time[-4:]
        return (modification_year == "2012")

#==========================================================================

class Test_SimpleTypesGenerator(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(Test_SimpleTypesGenerator, self).__init__(*args, **kwargs)
        self.environment = TestEnvironment("Test_SimpleTypesGenerator")
        self.generator = generator.PlainOldDataTypes(self.environment.output_path.parent().parent().parent(), self.environment.cpp_output_path)
        self.generator.set_output_path(self.environment.cpp_output_path)
        
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # Tests here just generates example target files. Real test of generator is 
    # as should be - test of generated files. Such test is in separate C++ project
    # which need to be compiled and run to perform tests of generated files.

    def test_GeneratingIntegerType(self):
        variables = {"name": "common : network : port number",
                     "int_class": "uint16_t",
                     "ordered": True}
        self.generator.generate_integer(variables)

    def test_GeneratingEnumType(self):
        variables = {"name": "common : severity",
                     "values": [ "data", "memo", "notice", "info", "trace", "debug", "log", "warning", \
                                 "problem", "error", "fatal", "disaster", "armagedon"],
                     "ordered": True,
                     "default": "info"}
        self.generator.generate_enum(variables)

    def test_GeneratingBitsetType(self):
        variables = {"name": "acoustic : selected output ids",
                     "values": ["audio input l", "audio input r", "radio transmit", "driver handphone", 
                                "driver speaker", "cabin inner speaker", "vehicle outher speaker"] }
        self.generator.generate_bitflags(variables)

    def test_GeneratingFloatingPointType(self):
        variables = {"name": "money : netto",
                     "ordered": True,
                     "float_class": "float",
                     "accuracy": "0.005f",
                     "string_format": ".2"}
        self.generator.generate_floating_point(variables)

    def test_GeneratingStringType(self):
        variables = {"name": "common : text message",
                     "default": "No comments.",
                     "max_size": 4000,
                     "ordered": True}
        self.generator.generate_string(variables)

    def test_GeneratingTimepointType(self):
        variables = {"name": "common : event time", \
                     "text_output_format": "$Y-$M-$D $h:$m:$s.$f",
                     "ordered": True}
        self.generator.generate_timepoint(variables)

    def test_GeneratingTimeDurationType(self):
        variables = {"name": "common : delay", \
                     "text_output_format": "$m:$s.$f",
                     "ordered": True,
                     "default": "std::chrono::milliseconds(10)"}
        self.generator.generate_time_duration(variables)

    def test_GeneratingRecordType(self):
        variables = {"name": "test : just a record",
                     "values": ["common : severity", \
                                "acoustic : selected output ids", \
                                "common : network : port number"],
                     "ordered": True}
        self.generator.generate_record(variables)
        variables = {"name": "test : another record",
                     "values": ["common : severity", \
                                "common : network : port number"],
                     "compareable": False}
        self.generator.generate_record(variables)

    def test_GeneratingCollectionType(self):
        self.generator.generate_string({ \
                "name": "configuration : key",
                "max_size": 255,
                "ordered": True})
        self.generator.generate_string({ \
                "name": "configuration : value",
                "default": "",
                "max_size": 64000,
                "compareable": False })
        self.generator.generate_collection({ \
                "name": "configuration : nodes", \
                "element_type": "configuration : node", \
                "ordered": True })
        self.generator.generate_record({
                "name": "configuration : node",
                "values": ["configuration : key", \
                           "configuration : value", \
                           "configuration : nodes"],
                "ordered": True })

#--------------------------------------------------------------------------

class Test_MetageneratorCoreFunctionalities(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(Test_MetageneratorCoreFunctionalities, self).__init__(*args, **kwargs)
        self.environment = TestEnvironment("Test_MetageneratorCoreFunctionalities")
        self.generator = meth.Metamorph(self.environment.sample_files_path)

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def test_GeneratingSimpleIntegerTypeFile(self):
        variables = {"class_name": "ErrorCode", 
                     "variable_name": "error_code", 
                     "base_type": "uint16_t"}
        self.generator.generate("test_integer.h.pattern", self.environment.output_path.get_as_directory() + "error_code.h", variables)
        self.assertTrue(self.environment.check_output_file("error_code.h"))

    def test_UseListOfValuesAsPlaceholderValue(self):
        variables = {"variable0": [],
                     "variable1": ["only_one_value"],
                     "variable2": ["car", "cdr"],
                     "variable3": ["first_value", "second_value", "third_value"],
                     "variable4": ["first_value", "second_value", "third_value", "and_finally_the_last"] }
        self.generator.generate("test_values_instantiation.h.pattern", self.environment.output_path.get_as_directory() + "multiline_placeholders.h", variables)
        self.assertTrue(self.environment.check_output_file("multiline_placeholders.h"))

    def test_PreserveExistingCodeBlocksChanged(self):
        self.environment.prepare_old_output_file("test_code_blocks_1.h")
        self.generator.generate("test_code_blocks.h.pattern", self.environment.output_path.get_as_directory() + "test_code_blocks_1.h", {} )
        self.assertFalse(self.environment.is_output_file_old("test_code_blocks_1.h"))

    def test_PreserveExistingCodeBlocksNotChanged(self):
        self.environment.prepare_old_output_file("test_code_blocks_2.h")
        self.generator.generate("test_code_blocks.h.pattern", self.environment.output_path.get_as_directory() + "test_code_blocks_2.h", {} )
        self.assertTrue(self.environment.check_output_file("test_code_blocks_2.h"))
        self.assertTrue(self.environment.is_output_file_old("test_code_blocks_2.h"))

    def test_IncludingWithParasmetrization(self):
        variables = {"A": "12345",
                     "B": "XYZ" }
        self.generator.generate("test_include.h.pattern", self.environment.output_path.get_as_directory() + "test_include.h", variables)
        self.assertTrue(self.environment.check_output_file("test_include.h"))

    def test_TestOfConditionals(self):
        variables = {"t": True,
                     "f": False }
        self.generator.generate("test_conditionals.h.pattern", self.environment.output_path.get_as_directory() + "test_conditionals.h", variables)
        self.assertTrue(self.environment.check_output_file("test_conditionals.h"))

    def test_TestOfLoops(self):
        variables = {"list0": [],
                     "listN": ["abc", "ABC", "Xyz"] }
        self.generator.generate("test_loops.h.pattern", self.environment.output_path.get_as_directory() + "test_loops.h", variables)
        self.assertTrue(self.environment.check_output_file("test_conditionals.h"))

#--------------------------------------------------------------------------

class Test_ListFormatting(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(Test_ListFormatting, self).__init__(*args, **kwargs)
        self.environment = TestEnvironment("Test_ListFormatting")
        self.generator = meth.Metamorph(self.environment.sample_files_path)

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def test_UseOfFormattedListsAsPlaceholderValue(self):
        variables = {"format": generatortools.ListFormatter(),
                     "variable0": [],
                     "variableN": ["first_value", "second_value", "third_value", "subsequent", "and_subsequent", "and_finally_the_last"] }
        self.generator.generate("test_formatting.h.pattern", self.environment.output_path.get_as_directory() + "multiline_formatted.h", variables)
        self.assertTrue(self.environment.check_output_file("multiline_formatted.h"))

#--------------------------------------------------------------------------

class Test_UniversalName(unittest.TestCase):

    def test_GettingLowerCaseName(self):
        name = generatortools.Name("monty python : something completly different")
        self.assertEqual(name.lowercase_name(), "something_completly_different")

    def test_GettingUpperCaseName(self):
        name = generatortools.Name("monty python : something completly different")
        self.assertEqual(name.UPPERCASE_NAME(), "SOMETHING_COMPLETLY_DIFFERENT")

    def test_GettingLowerCaseNameWithNamespace1(self):
        name = generatortools.Name("something completly different")
        self.assertEqual(name.lowercase_namespace_and_name(), "something_completly_different")

    def test_GettingLowerCaseNameWithNamespace2(self):
        name = generatortools.Name("monty python : something completly different")
        self.assertEqual(name.lowercase_namespace_and_name(), "monty_python_something_completly_different")

    def test_GettingLowerCaseNameWithNamespace3(self):
        name = generatortools.Name("bbc television : monty python : something completly different")
        self.assertEqual(name.lowercase_namespace_and_name(), "bbc_television_monty_python_something_completly_different")

    def test_GettingLowerCaseNameWithNamespace4(self):
        name = generatortools.Name("something completly different")
        self.assertEqual(name.lowercase_namespace_and_name("monty python"), "monty_python_something_completly_different")

    def test_GettingLowerCaseNameWithNamespace5(self):
        name = generatortools.Name("something completly different")
        self.assertEqual(name.lowercase_namespace_and_name("bbc television : monty python"), "bbc_television_monty_python_something_completly_different")

    def test_GettingLowerCaseNameWithNamespace6(self):
        name = generatortools.Name("bbc television : monty python : something completly different")
        self.assertEqual(name.lowercaseCamelName(), "somethingCompletlyDifferent")

    def test_GettingCamelCaseNameWithNamespace(self):
        name = generatortools.Name("bbc television : monty python : something completly different")
        self.assertEqual(name.UppercaseCamelName(), "SomethingCompletlyDifferent")

    def test_GettingUpperCaseNamespaces2(self):
        name = generatortools.Name("something completly different")
        self.assertEqual(name.UppercaseCamelsNamespaces(), [])

    def test_GettingUpperCaseNamespaces1(self):
        name = generatortools.Name("monty python : something completly different")
        self.assertEqual(name.UppercaseCamelsNamespaces(), ["MontyPython"])

    def test_GettingUpperCaseNamespaces3(self):
        name = generatortools.Name("bbc television : monty python : something completly different")
        self.assertEqual(name.UppercaseCamelsNamespaces(), ["BbcTelevision", "MontyPython"])

#--------------------------------------------------------------------------

class Test_ExistingCodeBlocks(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(Test_ExistingCodeBlocks, self).__init__(*args, **kwargs)
        self.environment = TestEnvironment("Test_ExistingCodeBlocks")

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def test_ReadingCodeBlockByName1(self):
        file_content = methtools.FileContent(self.environment.sample_files_path.get_as_directory() + "file_with_few_code_blocks.cpp")
        existing_code_blocks = methtools.ExistingCodeBlocks(file_content)
        block = existing_code_blocks.pop_code_block("// vvv--- a code block")
        self.assertEqual(block, ["\t\t\tA - first line\n", "\t\t\tB - second line\n"])

    def test_ReadingCodeBlockByName2(self):
        file_content = methtools.FileContent(self.environment.sample_files_path.get_as_directory() + "file_with_few_code_blocks.cpp")
        existing_code_blocks = methtools.ExistingCodeBlocks(file_content)
        block = existing_code_blocks.pop_code_block("// vvv--- a code block with different name")
        self.assertEqual(block, ["\t\tDifferent code block\n"])

    def test_ReadingCodeBlockFromNonExistingFile(self):
        file_content = methtools.FileContent(self.environment.sample_files_path.get_as_directory() + "file_with_code_blocks.cpp")
        existing_code_blocks = methtools.ExistingCodeBlocks(file_content)
        block = existing_code_blocks.pop_code_block("// vvv--- a code block with different name")
        self.assertEqual(block, None)

    def test_ReadingCodeBlocksFromBySameName(self):
        file_content = methtools.FileContent(self.environment.sample_files_path.get_as_directory() + "file_with_few_code_blocks.cpp")
        existing_code_blocks = methtools.ExistingCodeBlocks(file_content)
        block1 = existing_code_blocks.pop_code_block("// vvv--- a code block")
        self.assertEqual(block1, ["\t\t\tA - first line\n", "\t\t\tB - second line\n"])
        block2 = existing_code_blocks.pop_code_block("// vvv--- a code block")
        self.assertEqual(block2, ["\t\t\tC1 - first line\n", "\t\t\tC2 - second line\n"])
        block3 = existing_code_blocks.pop_code_block("// vvv--- a code block")
        self.assertEqual(block3, None)

#--------------------------------------------------------------------------

class Test_CodeBlockReplacer(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(Test_CodeBlockReplacer, self).__init__(*args, **kwargs)
        self.environment = TestEnvironment("Test_CodeBlockReplacer")
        
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def test_ReplacingSomeBlocks(self):
        pattern_file_name = "pattern_code.cpp"
        existing_code_file = "existing_code.cpp"
        output_file_name = "merged_result.cpp"
        pattern_file_content = methtools.FileContent(self.environment.sample_files_path.get_as_directory() + pattern_file_name)
        existing_file = methtools.FileContent(self.environment.sample_files_path.get_as_directory() + existing_code_file)
        code_blocks = methtools.ExistingCodeBlocks(existing_file)
        reader = methtools.LineByLineReader(pattern_file_content.lines)
        text_output = methtools.OutputText()
        replacer = methtools.CodeBlockReplacer(text_output, code_blocks)
        while not reader.is_eof():
            text_line = reader.get_line()
            replacer.append(text_line)
        output_file = methtools.OutputFile(self.environment.output_path.get_as_directory() + output_file_name)
        output_file.save(text_output.get_content())
        self.assertTrue(self.environment.check_output_file(output_file_name))

#--------------------------------------------------------------------------

class Test_AbsolutePathOperations(unittest.TestCase):

    def test_OfExtendingPath(self):
        path = generatortools.AbsolutePath("/XXX/Y/CCC/abcd")
        self.compare_path(path, "/XXX/Y/CCC/abcd")
        self.compare_path(path.parent(), "/XXX/Y/CCC")
        self.compare_path(path.create_changed_by("../../abcdef"), "/XXX/Y/abcdef")
        self.compare_path(path.create_changed_by("abc/def").get_as_directory(), "/XXX/Y/CCC/abcd/abc/def/")

    def test_OfPathDifference(self):
        path = generatortools.AbsolutePath("/XXX/Y/CCC/abcd")
        base = generatortools.AbsolutePath("/XXX/Y/TTT/abcd")
        relative = path.get_relative_to(base).replace("\\", "/")
        self.assertEqual(relative, "../../CCC/abcd")  

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def compare_path(self, path, pattern):
        path_text = str(path)
        if path_text[1] == ':':
            path_text = path_text[2:]
        self.assertEqual(path_text, pattern)

#--------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()

#--------------------------------------------------------------------------
