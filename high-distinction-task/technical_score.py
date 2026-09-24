import argparse
import csv
import sys
from datetime import datetime, timezone


def log(message):
    timestamp = datetime.now(timezone.utc).isoformat()
    print(f"[{timestamp}] {message}", flush=True)


def calculate_score(input_file, output_file):
    log("Starting Figure Skating Technical Score Calculator")
    log(f"Reading program data from: {input_file}")

    try:
        elements = []

        with open(input_file, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                element = row["element"]
                base_value = float(row["base_value"])
                goe_points = float(row["goe_points"])
                element_score = base_value + goe_points

                elements.append({
                    "element": element,
                    "base_value": base_value,
                    "goe_points": goe_points,
                    "element_score": element_score
                })

        if not elements:
            raise ValueError("The program contains no technical elements.")

        log(f"Loaded {len(elements)} technical elements")

        total_base_value = sum(
            element["base_value"] for element in elements
        )

        total_goe = sum(
            element["goe_points"] for element in elements
        )

        technical_element_score = sum(
            element["element_score"] for element in elements
        )

        highest_scoring_element = max(
            elements,
            key=lambda element: element["element_score"]
        )

        report_lines = [
            "FIGURE SKATING TECHNICAL SCORE REPORT",
            "=====================================",
            ""
        ]

        for element in elements:
            report_lines.append(
                f'{element["element"]:<10} '
                f'BV: {element["base_value"]:>5.2f}   '
                f'GOE: {element["goe_points"]:>+5.2f}   '
                f'Score: {element["element_score"]:>5.2f}'
            )

        report_lines.extend([
            "",
            "-------------------------------------",
            f"Total Base Value:          {total_base_value:.2f}",
            f"Total GOE Points:          {total_goe:+.2f}",
            f"Technical Element Score:   {technical_element_score:.2f}",
            "",
            "Highest Scoring Element:",
            f'{highest_scoring_element["element"]} '
            f'({highest_scoring_element["element_score"]:.2f} points)',
            ""
        ])

        report = "\n".join(report_lines)

        with open(output_file, "w", encoding="utf-8") as file:
            file.write(report)

        log(f"Calculated TES: {technical_element_score:.2f}")
        log(f"Technical report written to: {output_file}")
        log("Score calculation completed successfully")

    except Exception as error:
        log(f"ERROR: {error}")
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Calculate a figure skating program Technical Element Score."
    )

    parser.add_argument(
        "--input",
        default="/app/data/program.csv",
        help="Path to skating program CSV file"
    )

    parser.add_argument(
        "--output",
        default="/app/data/technical_report.txt",
        help="Path to generated score report"
    )

    args = parser.parse_args()

    calculate_score(args.input, args.output)