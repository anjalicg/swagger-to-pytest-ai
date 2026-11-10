import os
import argparse
from src.parser import get_endpoint_schema
from src.llm_client import generate_test_with_gemini, generate_test_with_openai
from src.delta_reporter import calculate_and_report_delta

def main():
    # 1. Setup arguments so it can be run easily from a CI/CD pipeline
    parser = argparse.ArgumentParser(description="AI-Driven Test Case Generator")
    parser.add_argument("--spec", type=str, default="swagger.json", help="Path to the OpenAPI JSON spec")
    parser.add_argument("--endpoint", type=str, default="/pet", help="The API endpoint to test")
    parser.add_argument("--method", type=str, default="post", help="The HTTP method to test")
    parser.add_argument("--llm", type=str, choices=["gemini", "openai"], default="gemini", help="LLM provider")
    args = parser.parse_args()

    # Define paths for our output files
    test_data_path = os.path.join("generated_tests", "pet_post_data.json")
    report_path = "test_delta_report.md"

    print(f"🚀 Starting AI Test Generation Pipeline for {args.method.upper()} {args.endpoint}...")

    # 2. Parse the Schema
    print(f"📄 Parsing schema from {args.spec}...")
    try:
        schema = get_endpoint_schema(args.spec, args.endpoint, args.method)
    except Exception as e:
        print(f"❌ Failed to parse schema: {e}")
        return

    # 3. Generate Boundary Tests via LLM
    print(f"🧠 Prompting {args.llm.capitalize()} to generate boundary conditions...")
    try:
        if args.llm == "gemini":
            llm_json_output = generate_test_with_gemini(schema)
        else:
            llm_json_output = generate_test_with_openai(schema)
        
        # Clean the output just in case the LLM wrapped it in markdown code blocks
        llm_json_output = llm_json_output.replace("```json", "").replace("```", "").strip()
    except Exception as e:
        print(f"❌ LLM generation failed: {e}")
        return

    # 4. Calculate Delta and Generate CI Report
    print("📊 Calculating delta and generating report...")
    calculate_and_report_delta(test_data_path, llm_json_output, report_path)

    print("\n✅ Pipeline complete!")
    print(f"   - Test Data: {test_data_path}")
    print(f"   - CI Report: {report_path}")
    print("\nTo execute the tests, run: pytest generated_tests/test_petstore_runner.py -v")

if __name__ == "__main__":
    main()