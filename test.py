import argparse
import os
import re


START = 1
END = 114
PREFIX_PATTERN = re.compile(r"^(\d{3})")


def format_missing_numbers(numbers):
	return [f"{number:03d}" for number in numbers]


def check_prefixes(directory):
	entries = os.listdir(directory)
	files = [name for name in entries if os.path.isfile(os.path.join(directory, name))]

	found_prefixes = set()
	out_of_range = []
	no_prefix = []

	for file_name in files:
		match = PREFIX_PATTERN.match(file_name)
		if not match:
			no_prefix.append(file_name)
			continue

		number = int(match.group(1))
		if START <= number <= END:
			found_prefixes.add(number)
		else:
			out_of_range.append((file_name, number))

	expected = set(range(START, END + 1))
	missing = sorted(expected - found_prefixes)

	return {
		"directory": directory,
		"total_files": len(files),
		"matched_in_range": len(found_prefixes),
		"missing": format_missing_numbers(missing),
		"out_of_range": sorted(out_of_range, key=lambda item: item[1]),
		"no_prefix": sorted(no_prefix),
	}


def main():
	parser = argparse.ArgumentParser(
		description="Check file name prefixes (first 3 digits) in range 001-114."
	)
	parser.add_argument(
		"directory",
		nargs="?",
		default=".",
		help="Directory to scan (default: current directory)",
	)
	args = parser.parse_args()

	result = check_prefixes(args.directory)

	print(f"Directory: {result['directory']}")
	print(f"Total files scanned: {result['total_files']}")
	print(f"Valid prefixes found (001-114): {result['matched_in_range']}/114")

	print("\nMissing prefixes:")
	if result["missing"]:
		print(", ".join(result["missing"]))
	else:
		print("None")

	print("\nOut-of-range files:")
	if result["out_of_range"]:
		for file_name, number in result["out_of_range"]:
			print(f"- {file_name} (prefix: {number:03d})")
	else:
		print("None")

	print("\nFiles without a 3-digit prefix:")
	if result["no_prefix"]:
		for file_name in result["no_prefix"]:
			print(f"- {file_name}")
	else:
		print("None")


if __name__ == "__main__":
	main()