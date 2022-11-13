# -------------------------------------------------------------------

# matagenerator 
# WGan 2022
# Open source
# freeware

import os
import re

from tools import general_name

# file loaded into memory in forn of list of lines.
# whole file content is read during construction.
# futher modification of file is not reflected in object
class file_lines(list):

    def __init__(self, file_name):
        with open(file_name, encoding = 'utf-8') as file:
            for line in file.readlines():
                self.append(line.rstrip())
     
# class used as accessor to content of the result file 
# (if file exists)
class target_content(file_lines):

    def __init__(self, file_name):
        if os.path.exists(file_name):
            file_lines.__init__(self, file_name)
     
# file to store as result file. File is overwritten 
# when store operation is called
class result_file:

    def __init__(self, file_content):
        self.lines = file_content

    def store(self, file_name):
        with open(file_name, "w", encoding = 'utf-8') as file:
            for line in self.lines:
                file.write(str(line) + "\n")

# line content with additional information
class line_content:

    def __init__(self, text):
        self.text = str(text)
        
    def __str__(self):
        return self.text
        
    def is_persistent_block_begin(self):
        return re.match("^\s*// -vvv.*", self.text)
      
    def is_persistent_block_end(self):
        return re.match("^\s*// -\^\^\^.*", self.text)
        
    def get_placeholder(self):
        return re.search("[$][{][^}]*[}]", self.text)

# just a class to denote that the code lines should be 
# threated as code, so no decoration between lines is performed
# but the lines are interpreted
class code_block:
    
    def __init__(self, list_od_lines):
        self.list_of_lines = list_od_lines
        
    def get_list_of_lines(self):
        return self.list_of_lines

# just gives string from the list. One by obe
class list_walker:

    def __init__(self, list_of_lines):
        self.lines_array = list_of_lines
        self.lines_count = len(self.lines_array)
        self.current_line = 0
        
    def is_end(self):
        return (self.current_line == self.lines_count)
    
    def get_line(self):
        if self.is_end():
            return None
        else:
            line = self.lines_array[self.current_line]
            self.current_line = self.current_line + 1
            return line_content(line)
            
    # replace last read line by the given list. It also back line pointer
    # to point to first line of added array
    def push_back(self, lines):
        self.lines_array = self.lines_array[:self.current_line-1] + lines + self.lines_array[self.current_line:]
        self.current_line = self.current_line - 1
        self.lines_count = len(self.lines_array)

    def go_to_line_with(self, content):
        self.current_line = 0
        while not self.is_end():
            source_line = self.get_line()
            if str(content).strip() == str(source_line).strip():
                break
                
    def go_to_end_of_content_block(self):
        while not self.is_end():
            line = self.get_line()
            if line.is_persistent_block_end():
                break

# main functionality - generator creating output files
class code_generator:

    def __init__(self, global_dictionary):
        self.symbols = {  }
        self.template_file_name = ""
        self.global_dictionary = global_dictionary
        
    def define(self, name, value):
        self.symbols[str(name)] = value
        
    def set_template(self, template_file_name):
        self.template_file_name = template_file_name
     
    def generate(self, result_file_name):
        template = file_lines(self.template_file_name)
        transformed = self._transform(template)
        stored_file = target_content(result_file_name)
        output_content = self._combine_with_user_code(transformed, stored_file)  
        output = result_file(output_content)
        output.store(result_file_name)
        
    def _transform(self, template):
        walker = list_walker(template)
        while not walker.is_end():
            line = walker.get_line()
            replacement = self._process_line(line)
            if replacement:
                walker.push_back(replacement)
        return walker.lines_array
 
    def _combine_with_user_code(self, transformd_template, existing_file):
        generated = list_walker(transformd_template)
        previous = list_walker(existing_file)
        result = [ ]
        while not generated.is_end():
            line = generated.get_line()
            result.append(str(line))
            if line.is_persistent_block_begin():
                previous.go_to_line_with(line)
                if previous.is_end():
                    self._copy_lines(generated, result)
                else:
                    self._copy_lines(previous, result)
                    generated.go_to_end_of_content_block()
        return result

    # transfroms single line to output. Returns 'True' when the line result is 
    # not the end of block and the content can be processed
    def _process_line(self, line):
        placeholder_match = line.get_placeholder()
        line_text = str(line)
        if placeholder_match:
            before = line_text[:placeholder_match.start(0)]
            after = line_text[placeholder_match.end(0):]
            expression = line_text[placeholder_match.start(0)+2:placeholder_match.end(0)-1]
            value = self._calculate_result(expression)
            return self._combine_lines_from(before, value, after)   
        return None
    
    # calculate result of expression to place in created text
    def _calculate_result(self, expression):
        return eval(expression, self.global_dictionary, self.symbols)

    def _combine_lines_from(self, before, value, after):
        if type(value) is list:
            list_len = len(value)
            if list_len == 0:
                return [ before+after ]
            if list_len == 1:
                return [ before+str(value[0])+after ]
            else:
                result = self._combine_lines_from(before, value[0], ",")
                prefix = self._whitespace_text(before)
                for scalar in value[1:-1]:
                    result = result + self._combine_lines_from(prefix, scalar, ",")
                result = result + self._combine_lines_from(prefix, value[-1], ",")
                return result
        elif type(value) is code_block:
            result = [ ]
            for line in value.get_list_of_lines():
                result = result + self._combine_lines_from(before, line, after)
            return result
        else:
            return [ before+str(value)+after ]
            
    def _whitespace_text(self, text):
        return re.sub("\S", " ", text)
    
    def _copy_lines(self, source, target):
        while not source.is_end():
            line = source.get_line()
            target.append(str(line))
            if line.is_persistent_block_end():
                return
    
# ----------------------------------------------------------
