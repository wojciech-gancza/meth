#--------------------------------------------------------------------------

import re

#--------------------------------------------------------------------------

class FileContent:

    def __init__(self, file_name):
        try:
            with open(file_name) as text_file: 
                self.text = text_file.read()
            self.lines = self.text.splitlines(True)
        except:
            self.text = None
            self.lines = []

    def __str__(self):
        return self.text

#--------------------------------------------------------------------------

class LineByLineReader:

    def __init__(self, array_of_text_lines, position_to_read = 0):
        self.array_of_text_lines = array_of_text_lines
        self.position_to_read = position_to_read
        self.lines_to_read = len(self.array_of_text_lines)

    def is_eof(self):
        return self.position_to_read >= self.lines_to_read

    def get_line(self):
        if self.is_eof():
            return None
        else:
            line = self.array_of_text_lines[self.position_to_read]
            self.position_to_read = self.position_to_read + 1
            return line

    def copy(self):
        return LineByLineReader(self.array_of_text_lines, self.position_to_read)

#--------------------------------------------------------------------------

class FirstReadThis:

    def __init__(self, line_to_read, decorated_reader):
        self.line_to_read = line_to_read
        self.decorated_reader = decorated_reader

    def is_eof(self):
        return self.line_to_read is None and self.decorated_reader.is_eof()

    def get_line(self):
        if self.line_to_read is None:
            return self.decorated_reader.get_line()
        else:
            result = self.line_to_read
            self.line_to_read = None
            return result

#--------------------------------------------------------------------------

class FileReader(LineByLineReader):

    def __init__(self, file_name):
        self.file_content = FileContent(file_name)
        LineByLineReader.__init__(self, self.file_content.lines)

#--------------------------------------------------------------------------

class WholeLineType:

    def __init__(self, text):
        self.is_extra_code_begin = (re.match("\s*// vvv--- .*", text) is not None)
        self.is_extra_code_end = (re.match("\s*// \^\^\^--- .*", text) is not None)
        if self.is_extra_code_begin:
            self.code_block_name = text.strip()
        else:
            self.code_block_name = None

#--------------------------------------------------------------------------

class DecomposedText:

    def __init__(self, text):
        self.whole_text = text
        expression_pattern = "\$\{[^}]*\}" # ${ ... }
        expression_found = re.search(expression_pattern, self.whole_text)
        if expression_found:
            self.before_expression = self.whole_text[:expression_found.span()[0]]
            self.expression = self.whole_text[expression_found.span()[0] + 2: expression_found.span()[1] - 1]
            self.after_expression = self.whole_text[expression_found.span()[1]:]
        else:
            self.expression = None

#--------------------------------------------------------------------------

class ExistingCodeBlocks:

    def __init__(self, file_content):
        self.code_blocks = [ ]
        reader = LineByLineReader(file_content.lines)
        while not reader.is_eof():
            text_line = reader.get_line()
            line_type = WholeLineType(text_line)
            if line_type.is_extra_code_begin:
                code_block_name = line_type.code_block_name
                code_block_content = self._read_code_block(reader)
                self.code_blocks.append( {"code_block_name": code_block_name, "code_block_content": code_block_content } )

    def _read_code_block(self, reader):
        code_block_content = []
        while not reader.is_eof():
            text_line = reader.get_line()
            line_type = WholeLineType(text_line)
            if line_type.is_extra_code_end:
                break
            else:
                code_block_content.append(text_line)
        return code_block_content

    def pop_code_block(self, code_block_name):
        code_block_name = code_block_name.strip()
        for code_block_definition in self.code_blocks:
            if code_block_definition["code_block_name"] == code_block_name:
                code_block_content = code_block_definition["code_block_content"]
                self.code_blocks.remove(code_block_definition)
                return code_block_content
        else:
            return None

#--------------------------------------------------------------------------

class CodeBlockReplacer:

    def __init__(self, output, code_blocks):
        self.output = output
        self.code_blocks = code_blocks
        self.skip_current_block = False

    def append(self, line_of_text):
        line_type = WholeLineType(line_of_text)
        if line_type.is_extra_code_begin:
            self.output.append(line_of_text)
            code_block_name = line_type.code_block_name
            code_block_content = self.code_blocks.pop_code_block(code_block_name)
            if code_block_content is not None:
                for line_of_code in code_block_content:
                    self.output.append(line_of_code)
                self.skip_current_block = True
        elif line_type.is_extra_code_end:
            self.output.append(line_of_text)
            self.skip_current_block = False
        elif not self.skip_current_block:
            self.output.append(line_of_text)

#--------------------------------------------------------------------------

class ParameterExtractor:

    def __init__(self, text):
        self.tail = text.strip()

    def pop_word(self):
        if self.tail == "":
            return ""
        separator_found = re.search( "\s", self.tail )
        if separator_found:
            word = self.tail[:separator_found.start()]
            self.tail = self.tail[separator_found.start():].strip()
        else:
            word = self.tail
            self.tail = ""
        return word

#--------------------------------------------------------------------------

class DummyOutput:

    def append(self, line_of_text):
        pass

#--------------------------------------------------------------------------

class OutputText:

    def __init__(self):
        self.file_elements = []

    def get_content(self):
        return "".join(self.file_elements)

    def append(self, line_of_text):
        self.file_elements.append(line_of_text)

#--------------------------------------------------------------------------

class OutputAllExceptLast:

    def __init__(self, decorated_output, first_line_prefix):
        self.output = decorated_output
        self.buffered_last_output = None
        self.line_prefix = first_line_prefix

    def append(self, line_of_text):
        if self.buffered_last_output is None:
            self.buffered_last_output = self.line_prefix + line_of_text
            self.line_prefix = re.subn("\S", " ", self.line_prefix)[0]
        else:
            self.output.append(self.buffered_last_output)
            self.buffered_last_output = self.line_prefix + line_of_text

#--------------------------------------------------------------------------

class OutputFile:

    def __init__(self, file_name):
        self.file_name = file_name
    
    def save(self, file_content):
        with open(self.file_name, "w") as text_file:
            text_file.write(file_content)

#--------------------------------------------------------------------------

class GeneratedFile:

    def __init__(self, file_name):
        self.output_file = OutputFile(file_name);
        self.existing_content = FileContent(file_name)
        self.text_storage = OutputText()
        self.existing_code_blocks = ExistingCodeBlocks(self.existing_content)
        self.code_block_replacer = CodeBlockReplacer(self.text_storage, self.existing_code_blocks)

    def append(self, line_of_text):
        self.code_block_replacer.append(line_of_text)

    def save(self):
        output_file_content = self.text_storage.get_content()
        if self.existing_content.text != output_file_content:
            self.output_file.save(output_file_content)

#--------------------------------------------------------------------------

