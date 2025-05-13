import re

def lint_rtl(rtl_code):
    """
    Lints RTL code to report bit-range specifications for Integer/Time/Real types
    and flags invalid assign statements. Provides suggestions for fixes.
    Args:
        rtl_code (str): The RTL code as a string.
    Returns:
        list: A list of errors, each error is a tuple of (line_number, error_message, suggestion).
    """

    errors = []
    lines = rtl_code.splitlines()

    for line_num, line in enumerate(lines, 0):
        # Regex to detect integer, time, or real declarations without bit-range
        match = re.search(r'\b(integer|time|real)\b(\s*\[.+:.*\])?\s*(\w+)\s*;', line)
        if match:
            type_name = match.group(1)
            var_name = match.group(3)
            if match.group(2):
                error_message = f"Line {line_num}: {type_name} variable '{var_name}' may not have bit-range specification."
                suggestion = f"Remove the bit-range specification for '{var_name}' or use a valid type that supports bit-ranges."
                errors.append((line_num, error_message, suggestion))

        # Regex to detect illegal usage of 'integer real'
        illegal_combination_match = re.search(r'\bparameter\s+integer\s+real\b', line)
        if illegal_combination_match:
            error_message = f"Line {line_num}: Syntax error near 'real' - Illegal use of 'integer real' detected."
            suggestion = "Use either 'integer' or 'real' as the type, but not both together."
            errors.append((line_num, error_message, suggestion))

        # Regex to detect incorrect module port declarations with default values
        incorrect_port_declaration = re.search(r'\bmodule\b.*\((.*\b(input|output|inout)\b\s+\w+\s+\w*\s*=\s*.+)\);', line)
        if incorrect_port_declaration:
            error_message = f"Line {line_num}: You cannot directly assign a default value within the port declaration itself."
            suggestion = "Move the default value assignment to an 'initial' block inside the module."
            errors.append((line_num, error_message, suggestion))

        # Regex to detect invalid assign statements
        invalid_assign_statement = re.search(r'\bassign\b\s+\w+\s*=\s*\(.*\)\d+;', line)
        if invalid_assign_statement:
            error_message = f"Line {line_num}: Syntax error - Invalid numeric literal in assign statement."
            suggestion = "Use a valid numeric literal format, such as '4'b0101' or '8'd55'."
            errors.append((line_num, error_message, suggestion))
        # Regex to detect mismatched labels in begin-end blocks
        mismatched_label = re.search(r'\bbegin\s*:\s*(\w+)', line)
        if mismatched_label:
            begin_label = mismatched_label.group(1) # In this case, it extracts the label following the begin : syntax.
            # Check ahead for corresponding end label
            for future_line_num, future_line in enumerate(lines[line_num:], line_num + 1):
                end_label_match = re.search(r'\bend\s*:\s*(\w+)', future_line)
                if end_label_match:
                    end_label = end_label_match.group(1) # In this case, it extracts the label following the end : syntax.
                    if begin_label != end_label:
                        error_message = f"Line {line_num}: Mismatched labels in begin-end block. 'begin : {begin_label}' does not match 'end : {end_label}'."
                        suggestion = f"Ensure the labels for 'begin' and 'end' blocks match."
                        errors.append((line_num, error_message, suggestion))
                    break
        # Regex to detect port declarations with misplaced bit-ranges
        misplaced_bit_range = re.search(r'\b(input|output|inout)\b\s+\w+\s*\[\d+:\d+\]\s*;', line)
        if misplaced_bit_range:
            error_message = f"Line {line_num}: Port declaration with misplaced bit-range detected. Bit-ranges should be declared before the variable name."
            suggestion = "Declare the bit-range before the variable name, e.g., 'input [2:0] x;'."
            errors.append((line_num, error_message, suggestion))
    return errors

if __name__ == '__main__':
    rtl_code_example = """
    module test_module(input xx = 1'b0);
      integer a;      // Non-missing bit-range
      integer [31:0] b;  // Incorrect
      time c;         // Non-missing bit-range
      real d;         // Non-missing bit-range
      real [63:0] e;  // Incorrect
      integer [7:0] f; // Incorrect
      parameter integer  x = 0; // Illegal usage
      time [31:0] t;  // Incorrect
      input clk;
      output reg valid;
      input x[2:0]; // Incorrect
      assign y = (4)55; // Incorrect
    endmodule
    module a(input wire x = 1'b0); // Incorrect port declaration
    endmodule
    module a;
        initial
        begin : label1
        end: label2
    endmodule
    """
    
    lint_errors = lint_rtl(rtl_code_example)
    
    if lint_errors:
        for line_num, error_msg, suggestion in lint_errors:
            print(f"{error_msg}\nSuggestion: {suggestion}\n")
    else:
        print("No linting errors found.")
