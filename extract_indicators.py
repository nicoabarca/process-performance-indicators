#!/usr/bin/env python3
"""
Script to extract all function names from the process_performance_indicators/indicators directory
and organize them into a JSON structure.
"""

import ast
import json
from pathlib import Path


def extract_function_info(file_path):
    """Extract function names and their arguments from a Python file using AST."""
    function_info = {}
    try:
        content = file_path.read_text(encoding="utf-8")

        # Parse the Python file into an AST
        tree = ast.parse(content)

        # Walk through all nodes in the AST
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                func_name = node.name
                # Skip private functions (starting with _)
                if not func_name.startswith("_"):
                    # Extract argument names
                    args_list = [arg.arg for arg in node.args.args]
                    function_info[func_name] = args_list

    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return function_info


def main():
    # Base directory for indicators
    indicators_dir = Path("process_performance_indicators/indicators")

    # Initialize the result dictionary
    indicators_dict = {}

    # Get all subdirectories in indicators
    for category_dir in indicators_dir.iterdir():
        if category_dir.is_dir() and category_dir.name != "__pycache__":
            category_name = category_dir.name
            indicators_dict[category_name] = {}

            # Get all Python files in each category directory
            for py_file in category_dir.iterdir():
                if py_file.is_file() and py_file.name.endswith(".py") and py_file.name != "__init__.py":
                    file_name = py_file.stem  # Get filename without extension
                    function_info = extract_function_info(py_file)
                    if function_info:  # Only add if there are functions
                        indicators_dict[category_name][file_name] = function_info

    # Write to JSON file
    output_file = Path("indicators_list.json")
    output_file.write_text(json.dumps(indicators_dict, indent=2, sort_keys=True), encoding="utf-8")

    print(f"Successfully extracted indicators to {output_file}")

    # Print summary
    total_functions = 0
    for category, files in indicators_dict.items():
        category_functions = sum(len(functions) for functions in files.values())
        total_functions += category_functions
        print(f"{category}: {category_functions} functions across {len(files)} files")

    print(f"Total: {total_functions} functions")


if __name__ == "__main__":
    main()
