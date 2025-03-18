import os
from downloadSite import crawl_readthedocs
from toMD import convert_html_to_markdown, append_md_files_to_single_file

def main():
    readthedocs_url = input("Enter the base URL of your Read the Docs webpage (e.g., https://your-project.readthedocs.io/en/latest/): ").strip()
    combined_output_file = input("Enter the name of the combined Markdown file: ").strip()

    if not readthedocs_url.endswith('/'):
        readthedocs_url += '/'

    working_directory = "working"
    crawl_readthedocs(readthedocs_url, working_directory)
    convert_html_to_markdown(working_directory, working_directory + "_md")
    append_md_files_to_single_file(working_directory + "_md", combined_output_file)

    # Delete all files except the combined Markdown file
    for root, dirs, files in os.walk(working_directory):
        for file in files:
            os.remove(os.path.join(root, file))
    for root, dirs, files in os.walk(working_directory + "_md"):
        for file in files:
            if file != combined_output_file:
                os.remove(os.path.join(root, file))
    os.rmdir(working_directory)
    os.rmdir(working_directory + "_md")

if __name__ == "__main__":
    main()


