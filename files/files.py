"""Task3."""
# ruff: noqa: PTH123
from __future__ import annotations

from typing import NamedTuple


class FileWrapper(NamedTuple):
    """Wrapper for file content."""

    file_name: str
    length: int
    content: list[str]


def get_file_contents(file_paths: list[str]) -> list[FileWrapper]:
    """Get file contexts wrapped in FileWrapper class."""
    files_content = []
    for file_path in file_paths:
        with open(file_path) as file:
            content = file.readlines()
            files_content.append(FileWrapper(file_path, len(content), content))
    return files_content


def sort_files_content(wrapper_contents: list[FileWrapper]) -> None:
    """Sort file contexts by length."""
    wrapper_contents.sort(key=lambda file_wrapper: file_wrapper.length)


def write_into_one_files(wrapper_contents: list[FileWrapper]) -> None:
    """Generate result file based on all files."""
    with open("result.txt", "w") as result_file:
        for wrapper_content in wrapper_contents:
            result_file.write(
                f"{wrapper_content.file_name}\n{wrapper_content.length}\n",
            )
            result_file.writelines(wrapper_content.content)


if __name__ == "__main__":
    file_names = ["1.txt", "2.txt"]
    content_wrappers = get_file_contents(file_names)
    sort_files_content(content_wrappers)
    write_into_one_files(content_wrappers)
