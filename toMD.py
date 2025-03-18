import os
import subprocess

def convert_html_to_markdown(input_dir, output_dir):
    """Converts HTML files in the input directory to Markdown using Pandoc."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.endswith(".html"):
            input_filepath = os.path.join(input_dir, filename)
            output_filename = filename.replace(".html", ".md")
            output_filepath = os.path.join(output_dir, output_filename)

            try:
                # Run Pandoc to convert HTML to Markdown
                subprocess.run(
                    ["pandoc", input_filepath, "-f", "html", "-t", "markdown", "-o", output_filepath],
                    check=True
                )
                print(f"Converted: {input_filepath} -> {output_filepath}")
            except subprocess.CalledProcessError as e:
                print(f"Error converting {input_filepath}: {e}")
def append_md_files_to_single_file(md_directory, combined_output_file):
    """Appends all Markdown files in a directory to a single Markdown file."""
    with open(combined_output_file, 'w', encoding='utf-8') as combined_file:
        for filename in os.listdir(md_directory):
            if filename.endswith(".md"):
                input_filepath = os.path.join(md_directory, filename)
                with open(input_filepath, 'r', encoding='utf-8') as file:
                    combined_file.write(file.read() + "\n\n")

if __name__ == "__main__":
    input_directory = input("Enter the directory containing HTML files: ").strip()
    output_directory = input("Enter the directory to save Markdown files: ").strip()
    combined_output_file = input("Enter the name of the combined Markdown file: ").strip()

    convert_html_to_markdown(input_directory, output_directory)
    append_md_files_to_single_file(output_directory, combined_output_file)
    print("Conversion and appending complete.")