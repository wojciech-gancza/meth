# -------------------------------------------------------------------

# matagenerator 
# WGan 2022
# Open source
# freeware

import os
import re

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
class result_file(list):

    def store(self, file_name):
        with open(file_name, "w", encoding = 'utf-8') as file:
            for line in self:
                file.write(str(line) + "\n")

# line content with additional information
class line_content:

    def __init__(self, text):
        self.text = text
        
    def __str__(self):
        return self.text
        
    def is_persistent_block_begin(self):
        return re.match("^\s*// -vvv.*", self.text)
      
    def is_persistent_block_end(self):
        return re.match("^\s*// -\^\^\^.*", self.text)
       
# transform template line and store it in output list
class line_processor:

    def __init__(self, line, symbols):
        self.text = str(line)
        self.symbols = symbols
    
    # process replaces each occurance of ${ ... } by the value of python
    # expression ... (calculated by eval function, so all known variables
    # function objects and classes can be used. More placeholders in line are 
    # allowed. 
    def process(self, output):
        if self.text == "":
            output.append(self.text)
        text = self.text
        while text:
            match = re.search("[$][{][^}]*[}]", text)
            if not match:
                output.append(text)
                return
            before = text[:match.start(0)]
            after = text[match.end(0):]
            expression = text[match.start(0)+2:match.end(0)-1]
            value = eval(expression, self.symbols)
            if type(value) is list:
                separator = ","
                if len(value) > 1:
                    prefix = self._get_prefix(before)
                    for scalar in value[:-1]:
                        output.append(before + scalar + separator)
                        before = prefix
                text = before + str(value[-1]) + after
            else:
                text = before + str(value) + after         
       
    def _get_prefix(self, string):
        result = ""
        for char in string:
            if char.isspace():
                result = result + char
            else:
                result = result + ' '
        return result
    
    
# just gives string from the list. One by obe
class list_reader:

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

    def go_to_line_with(self, content):
        while not self.is_end():
            source_line = self.get_line()
            if str(content).strip() == str(source_line).strip():
                break
                
    def go_to_end_of_content_block(self):
        while not self.is_end():
            line = self.get_line()
            if line.is_persistent_block_end():
                break

    def copy_till_block_end(self, output):
        while not self.is_end():
            line = self.get_line()
            output.append(line)
            if line.is_persistent_block_end():
                break
                
    def process_till_block_end(self, output, symbols):
        while not self.is_end():
            line = line_content(self.get_line())
            processor = line_processor(line, symbols)
            processor.process(output)
            if line.is_persistent_block_end():
                        break

class generator:

    def __init__(self):
        self.symbols = {  }
        self.template_file_name = ""
        
    def define(self, name, value):
        self.symbols[str(name)] = value
        
    def set_template(self, template_file_name):
        self.template_file_name = template_file_name
        
    def generate(self, result_file_name):
        template = file_lines(self.template_file_name)
        stored_file = target_content(result_file_name)
        output = result_file()
        template_lines = list_reader(template)
        while not template_lines.is_end():
            line = template_lines.get_line()
            processor = line_processor(line, self.symbols)
            processor.process(output)
            if line.is_persistent_block_begin():
                block_source = list_reader(stored_file)
                block_source.go_to_line_with(line)
                if not block_source.is_end():
                    block_source.copy_till_block_end(output)
                    template_lines.go_to_end_of_content_block()
                else:
                    template_lines.process_till_block_end(output, self.symbols)
        output.store(result_file_name)
    
# ----------------------------------------------------------

class general_name:

    def __init__(self, name):
        self.bare_name = name.split()
        
    def CamelCase(self):
        return "".join([x.capitalize() for x in self.bare_name])
        

# Main functionality of source file generator. It 
builder = generator()
builder.set_template("../test/source.cpp")
builder.define("name", general_name("hello World"))
builder.define("enum_list", ["FIRST", "SECOND", "THIRD"])
builder.generate("../test/_generated/result.cpp")

