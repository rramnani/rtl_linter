# rtl_linter/RTL Lint Script

This project provides a Python script to lint RTL (Register Transfer Level) code. The script identifies common issues in RTL code, such as improper bit-range specifications, invalid assign statements, and mismatched labels in `begin-end` blocks. It also provides suggestions for fixing these issues.

## Features

- Detects improper bit-range specifications for `integer`, `time`, and `real` types.
- Flags illegal usage of `integer real` in parameter declarations.
- Identifies incorrect module port declarations with default values.
- Detects invalid assign statements with incorrect numeric literals.
- Checks for mismatched labels in `begin-end` blocks.
- Validates port declarations with misplaced bit-ranges.

## Getting Started

### Prerequisites

- Python 3.x
- Basic understanding of RTL code (e.g., Verilog).

### Installation

Clone the repository:
   git clone https://github.com/rramnani/rtl-lint-script.git
   cd rtl-lint-script
   
### Project Structure
.
├── [integer_no_range.py](http://_vscodecontentref_/0)   # Main linting script
├── README.md             # Project documentation

### Contributing

Contributions are welcome! If you have suggestions for improvements or additional features, feel free to open an issue or submit a pull request.

### Contact

For questions or feedback, please contact ramnani.rohit.k@gmail.com
