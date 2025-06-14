#--------------------------------------------------------------------------

import meth
import math
import generatortools
import inspect

#--------------------------------------------------------------------------

class PlainOldDataTypes:

    def __init__(self, soluton_path, tools_target_path = None):
        if not tools_target_path:
            tools_target_path = soluton_path
        self.environment = generatortools.Environment()
        self.soluton_path = generatortools.AbsolutePath(soluton_path)
        self.output_path = soluton_path
        self.tools_output_path = generatortools.AbsolutePath(tools_target_path)
        self.generator = meth.Metamorph(self.environment.patterns_path.get_as_directory())

    def set_output_path(self, output_path):
        self.output_path = generatortools.AbsolutePath(output_path)

    def generate_bitflags(self, properties):
        extended_properties = self._extend_property_list(properties)
        extended_properties["ordered"] = False
        if len(extended_properties["values"]) <= 8:
            extended_properties["base_class"] = "uint8_t"
            extended_properties["base_class_size"] = 1
        elif len(extended_properties["values"]) <= 16:
            extended_properties["base_class"] = "uint16_t"
            extended_properties["base_class_size"] = 2
        elif len(extended_properties["values"]) <= 32:
            extended_properties["base_class"] = "uint32_t"
            extended_properties["base_class_size"] = 4
        hex_format = "0x{:0" + str(math.ceil(len(properties["values"]) / 4)) + "x}"
        extended_properties["first_value"] = hex_format.format(1)
        extended_properties["last_value"] = hex_format.format(pow(2, len(extended_properties["values"]) - 1))
        extended_properties["code_converting_from_string"] = generatortools.EnumCodeGenerator(extended_properties["values"]).generate_code()
        extended_properties["includes"] = [ self.tools_output_path.create_changed_by("serialization_binary_serialization.h") ]
        self._generate("bitflags.h.pattern", "header_file_name", extended_properties)
        extended_properties["includes"] = [ self.tools_output_path.create_changed_by("common_conversion_error.h") ]
        self._generate("bitflags.cpp.pattern", "source_file_name", extended_properties)

    def generate_enum(self, properties):
        extended_properties = self._extend_property_list(properties)
        if len(extended_properties["values"]) <= 255:
            extended_properties["base_class"] = "uint8_t"
            extended_properties["base_class_size"] = 1
        elif len(extended_properties["values"]) <= 65535:
            extended_properties["base_class"] = "uint16_t"
            extended_properties["base_class_size"] = 2
        else:
            extended_properties["base_class"] = "uint32_t"
            extended_properties["base_class_size"] = 4
        extended_properties["first_value"] = extended_properties["values"][0].UPPERCASE_NAME()
        extended_properties["last_value"] = extended_properties["values"][-1].UPPERCASE_NAME()
        extended_properties["code_converting_from_string"] = generatortools.EnumCodeGenerator(extended_properties["values"]).generate_code()
        extended_properties["includes"] = [ self.tools_output_path.create_changed_by("serialization_binary_serialization.h") ]
        self._set_default_value(extended_properties, "default", None)
        if extended_properties["default"]:
            extended_properties["default"] = generatortools.Name(properties["default"])
        self._generate("enum.h.pattern", "header_file_name", extended_properties)
        extended_properties["includes"] = [ self.tools_output_path.create_changed_by("common_conversion_error.h") ]
        self._generate("enum.cpp.pattern", "source_file_name", extended_properties)

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def _generate(self, pattern_file_name, output_type, properties):
        pattern_file_path = self.environment.patterns_path.create_changed_by(pattern_file_name)
        properties["pattern_file_path"] = pattern_file_path
        output_file_name = properties[output_type]
        properties["output_file_name"] = output_file_name
        self.generator.generate(pattern_file_name, str(output_file_name), properties)

    def _set_default_value(self, properties, name, default_value):
        if name not in properties.keys():
            properties[name] = default_value

    def _extend_property_list(self, properties):
        name = generatortools.Name(properties["name"])
        frame = inspect.currentframe().f_back.f_back
        generator_code_line = frame.f_lineno
        generator_code_file = generatortools.AbsolutePath(inspect.getmodule(frame).__file__)
        extended_properties = { **properties, 
                 "format": generatortools.ListFormatter(),
                 "name": name, 
                 "class_name": name.UppercaseCamelName(),
                 "object_name": name.lowercase_name(),
                 "header_file_name": self.output_path.create_changed_by(name.lowercase_namespace_and_name() + ".h"),
                 "source_file_name": self.output_path.create_changed_by(name.lowercase_namespace_and_name() + ".cpp"),
                 "namespaces": name.UppercaseCamelsNamespaces(),
                 "generator_path": generator_code_file,
                 "generator_line_number": generator_code_line,
                 "solution_path": self.soluton_path }
        if "values" in extended_properties.keys():
            extended_properties["values"] = [generatortools.Name(value) for value in extended_properties["values"] ]
        self._set_default_value(extended_properties, "compareable", True)
        self._set_default_value(extended_properties, "ordered", False)
        if extended_properties["ordered"]:
            extended_properties["compareable"] = True
        return extended_properties

#--------------------------------------------------------------------------


