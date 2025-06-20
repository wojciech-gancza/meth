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

    def generate_integer(self, properties):
        # required properties:
        # - name - fully qualified type name defined as single string where words are name elements ( example: "common : severity"),
        # - int_class - name of type used to store the value internally (example: "uint16_t")
        # optional properties:
        # - compareable - adds "==", "=!" , ... operators. When not defined True is assumed
        # - ordered - adds "<", ">" , ... operators. When set to true also sets compareable. When not defined False is assumed
        # - default - default value. When not defined - 0 is assumed
        extended_properties = self._extend_property_list(properties)
        self._set_int_class_size(extended_properties)
        self._set_default_value(extended_properties, "default", 0)
        extended_properties["std_includes"] = ["cstdint"]
        self._generate_files("integer.h.body.pattern", "integer.cpp.body.pattern", extended_properties)

    def generate_string(self, properties):
        # required properties:
        # - name - fully qualified type name defined as single string where words are name elements ( example: "common : severity"),
        # - max_size - maximum size of string. Used to deduct size type used also in serialization
        # optional properties:
        # - compareable - adds "==", "=!" , ... operators. When not defined True is assumed
        # - ordered - adds "<", ">" , ... operators. When set to true also sets compareable. When not defined False is assumed
        # - default - default value. When not defined - empty string us used as default
        # - compare_type - how the strings are compared. Default is "strcmp"
        extended_properties = self._extend_property_list(properties)
        self._set_int_type_by_count_of_values(extended_properties, extended_properties["max_size"])
        self._set_default_value(extended_properties, "default", "")
        self._set_default_value(extended_properties, "compare_type", "strcmp")
        extended_properties["std_includes"] = ["cstdint"]
        self._generate_files("string.h.body.pattern", "string.cpp.body.pattern", extended_properties)

    def generate_floating_point(self, properties):
        # required properties:
        # - name - fully qualified type name defined as single string where words are name elements ( example: "common : severity"),
        # - float_class - name of type used to store the value internally (example: "uint16_t")
        # optional properties:
        # - compareable - adds "==", "=!" , ... operators. When not defined True is assumed
        # - ordered - adds "<", ">" , ... operators. When set to true also sets compareable. When not defined False is assumed
        # - default - default value. When not defined - 0.0
        # - accuracy - value used to compare - when difference is less the accuracy assume equal. Default = 0.0001
        # - format - format of string the value is converted to
        extended_properties = self._extend_property_list(properties)
        self._set_default_value(extended_properties, "default", "0.0")
        self._set_default_value(extended_properties, "accuracy", "0.0001")
        self._set_default_value(extended_properties, "format", ".4f")
        extended_properties["std_includes"] = ["format"]
        self._generate_files("float.h.body.pattern", "float.cpp.body.pattern", extended_properties)

    def generate_enum(self, properties):
        # required properties:
        # - name - fully qualified type name defined as single string where words are name elements ( example: "common : severity"),
        # - values - list of values (example: [ "data", "memo", "notice", "info", "trace", "debug"])
        # optional properties:
        # - default - default value. When not defined - first value is default
        # - compareable - adds "==", "=!" , ... operators. When not defined True is assumed
        # - ordered - adds "<", ">" , ... operators. When set to true also sets compareable. When not defined False is assumed
        extended_properties = self._extend_property_list(properties)
        self._set_int_type_by_count_of_values(extended_properties, len(extended_properties["values"]))
        extended_properties["first_value"] = extended_properties["values"][0].UPPERCASE_NAME()
        extended_properties["last_value"] = extended_properties["values"][-1].UPPERCASE_NAME()
        extended_properties["code_converting_from_string"] = generatortools.EnumCodeGenerator(extended_properties["values"]).generate_code()
        self._set_default_value(extended_properties, "default", None)
        if extended_properties["default"]:
            extended_properties["default"] = generatortools.Name(properties["default"])
        extended_properties["std_includes"] = ["cstdint"]
        self._generate_files("enum.h.body.pattern", "enum.cpp.body.pattern", extended_properties)

    def generate_bitflags(self, properties):
        # required properties:
        # - name - fully qualified type name defined as single string where words are name elements ( example: "common : severity"),
        # - values - list of values (example: ["audio input l", "audio input r", "radio transmit", "driver handphone" ])
        # optional properties:
        # - compareable - adds "==", "=!" , ... operators. When not defined True is assumed
        # remarks: In this version the default is always no bit set. Bitsets cannot be ordered
        extended_properties = self._extend_property_list(properties)
        extended_properties["ordered"] = False
        self._set_int_type_by_count_of_bits(extended_properties, len(extended_properties["values"]))
        hex_format = "0x{:0" + str(math.ceil(len(properties["values"]) / 4)) + "x}"
        extended_properties["first_value"] = hex_format.format(1)
        extended_properties["last_value"] = hex_format.format(pow(2, len(extended_properties["values"]) - 1))
        extended_properties["code_converting_from_string"] = generatortools.EnumCodeGenerator(extended_properties["values"]).generate_code()
        extended_properties["std_includes"] = ["cstdint"]
        self._generate_files("bitflags.h.body.pattern", "bitflags.cpp.body.pattern", extended_properties)

    def generate_record(self, properties):
        # required properties:
        # - name - fully qualified type name defined as single string where words are name elements ( example: "common : severity"),
        # - values - list of types of record elements ["common : severity", "acoustic : selected output ids", "common : network : port number"]
        # optional properties:
        # - compareable - adds "==", "=!" , ... operators. When not defined True is assumed
        # - ordered - adds "<", ">" , ... operators. When set to true also sets compareable. When not defined False is assumed
        extended_properties = self._extend_property_list(properties)
        extended_properties["values"] = [ generatortools.Name(value) for value in properties["values"] ]
        extended_properties["includes"] = [ self.output_path.create_changed_by(name.lowercase_namespace_and_name() + ".h") for name in extended_properties["values"] ]
        extended_properties["cpp_includes"] =  [ self.tools_output_path.create_changed_by("common_record_fields_comparision.h") ]
        self._generate_files("record.h.body.pattern", "record.cpp.body.pattern", extended_properties)

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def _generate_files(self, header_pattern, cpp_pattern, properties):
        self._set_default_value(properties, "includes", [] )
        properties["includes"] = properties["includes"] + [ self.tools_output_path.create_changed_by("serialization_binary_serialization.h") ]
        properties["code_body_pattern"] = header_pattern
        properties["std_includes"] = properties["std_includes"] + ["string", "iostream"]
        properties["once"] = True
        self._generate("source.main.pattern", "header_file_name", properties)
        properties["includes"] = [ self.output_path.create_changed_by( properties["name"].lowercase_namespace_and_name() + ".h" ), \
                                   self.tools_output_path.create_changed_by("common_conversion_error.h") \
                                  ] + properties["cpp_includes"]
        properties["code_body_pattern"] = cpp_pattern
        properties["std_includes"] = ["sstream"]
        properties["once"] = False
        self._generate("source.main.pattern", "source_file_name", properties)

    def _generate(self, pattern_file_name, output_type, properties):
        pattern_file_path = self.environment.patterns_path.create_changed_by(pattern_file_name)
        properties["pattern_file_path"] = self.environment.patterns_path.create_changed_by(properties["code_body_pattern"])
        properties["pattern_wrapper_file_path"] = pattern_file_path
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
                 "solution_path": self.soluton_path,
                 "cpp_includes": [],
                 "std_includes": [] }
        if "values" in extended_properties.keys():
            extended_properties["values"] = [generatortools.Name(value) for value in extended_properties["values"] ]
        self._set_default_value(extended_properties, "compareable", True)
        self._set_default_value(extended_properties, "ordered", False)
        if extended_properties["ordered"]:
            extended_properties["compareable"] = True
        return extended_properties

    def _set_int_class_size(self, properties):
        if properties["int_class"] in ["int8_t", "uint8_t"]:
            properties["int_class_size"] = 1
        elif properties["int_class"] in ["int16_t", "uint16_t"]:
            properties["int_class_size"] = 2
        elif properties["int_class"] in ["int32_t", "uint32_t"]:
            properties["int_class_size"] = 4
        elif properties["int_class"] in ["int64_t", "uint64_t"]:
            properties["int_class_size"] = 8

    def _set_int_type_by_count_of_values(self, properties, cout_values):
        if cout_values <= 255:
            properties["int_class"] = "uint8_t"
            properties["int_class_size"] = 1
        elif cout_values <= 65535:
            properties["int_class"] = "uint16_t"
            properties["int_class_size"] = 2
        else:
            properties["int_class"] = "uint32_t"
            properties["int_class_size"] = 4

    def _set_int_type_by_count_of_bits(self, properties, count_of_bits):
        if count_of_bits <= 8:
            properties["int_class"] = "uint8_t"
            properties["int_class_size"] = 1
        elif count_of_bits <= 16:
            properties["int_class"] = "uint16_t"
            properties["int_class_size"] = 2
        elif count_of_bits <= 32:
            properties["int_class"] = "uint32_t"
            properties["int_class_size"] = 4
        elif count_of_bits <= 64:
            properties["int_class"] = "uint64_t"
            properties["int_class_size"] = 4

#--------------------------------------------------------------------------


