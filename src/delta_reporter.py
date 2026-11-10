import json
import os

def calculate_and_report_delta(old_file_path: str, new_llm_json_string: str, report_path: str = "test_delta_report.md"):
    """Compares previous test data with new LLM data and generates a Markdown report."""
    
    # 1. Parse the new LLM output into a Python list of dicts
    try:
        new_data = json.loads(new_llm_json_string)
    except json.JSONDecodeError:
        print("Error: LLM did not return valid JSON.")
        return

    # 2. Load the old data if it exists
    old_data = []
    if os.path.exists(old_file_path):
        with open(old_file_path, 'r', encoding='utf-8') as f:
            old_data = json.load(f)

    # 3. Extract just the test names to use as unique identifiers for our Sets
    old_test_names = {test.get("test_name") for test in old_data if "test_name" in test}
    new_test_names = {test.get("test_name") for test in new_data if "test_name" in test}

    # 4. Calculate the Delta using Python Set operations
    added_tests = new_test_names - old_test_names
    removed_tests = old_test_names - new_test_names

    # 5. Build the Markdown Report
    report_lines = [
        "# AI Test Generation Delta Report",
        "### Summary",
        f"- **Previous Test Count:** {len(old_test_names)}",
        f"- **New Test Count:** {len(new_test_names)}",
        f"- **Net Change:** {len(new_test_names) - len(old_test_names)}",
        "---",
        "### 🟢 Newly Added Boundary Tests"
    ]

    if added_tests:
        for test in sorted(added_tests):
            report_lines.append(f"- `{test}`")
    else:
        report_lines.append("- *No new tests added in this run.*")

    report_lines.append("\n### 🔴 Removed Boundary Tests")
    if removed_tests:
        for test in sorted(removed_tests):
            report_lines.append(f"- `{test}`")
    else:
        report_lines.append("- *No tests were removed.*")

    # 6. Save the new data overwriting the old file for the next run
    with open(old_file_path, 'w', encoding='utf-8') as f:
        json.dump(new_data, f, indent=2)

    # 7. Write the markdown report
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(report_lines))
        
    print(f"✅ State updated. Delta report saved to {report_path}")

# --- Quick Test ---
if __name__ == "__main__":
    # Simulating a scenario where the LLM generated 3 tests, but the old file only had 2.
    dummy_llm_output = """
    [
      {"test_name": "test_empty_name", "payload": {}, "expected_status": 400},
      {"test_name": "test_null_id", "payload": {"id": null}, "expected_status": 400},
      {"test_name": "test_negative_id", "payload": {"id": -1}, "expected_status": 400}
    ]
    """
    
    # Run the function (assuming old data doesn't exist yet, it will treat all 3 as "Added")
    calculate_and_report_delta("generated_tests/pet_post_data.json", dummy_llm_output)