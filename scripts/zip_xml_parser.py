import argparse
import zipfile
import xml.etree.ElementTree as ET

from typing import List, Optional


class ZipXMLParser:
    """
    A class to parse and process XML files within a zip archive.

    This class provides functionality to count the number of products, show the list of available products, and show
    the list of spare parts for the products in an XML file contained within a zip archive. The user is prompted to
    choose an operation, and then the appropriate action is taken on the selected XML file.

    Args:
    zip_file_path (str): The path to the zip archive containing XML files.

    Methods:
    open_zip_file(): Prompts the user to select an XML file from the archive, and reads the contents of the selected file.
    count_products(root: ET.Element): Counts the number of products in the XML file.
    show_products(root: ET.Element): Displays a list of available products in the XML file.
    show_spare_parts(root: ET.Element): Displays a list of spare parts available for the products in the XML file.
    process_choice(): Prompts the user to select an operation and processes the selected operation on the XML file.
    """
    def __init__(self, zip_file_path: str):
        self.zip_file_path: str = zip_file_path
        self.file_list: Optional[List[str]] = None
        self.xml_contents: Optional[bytes] = None

    def open_zip_file(self) -> None:
        try:
            with zipfile.ZipFile(self.zip_file_path, "r") as zip_file:
                self.file_list = zip_file.namelist()

                print("Please choose an XML file:")
                for i, file_name in enumerate(self.file_list):
                    print(f"{i + 1}. {file_name}")

                file_choice = int(input("Enter a number: ")) - 1

                with zip_file.open(self.file_list[file_choice], "r") as xml_file:
                    self.xml_contents = xml_file.read()

        except FileNotFoundError:
            print(f"File {self.zip_file_path} not found.")
            exit()
        except zipfile.BadZipFile:
            print(f"{self.zip_file_path} is not a valid zip file.")
            exit()
        except (zipfile.LargeZipFile, MemoryError):
            print("Zip file is too large to read.")
            exit()
        except:
            print("Unexpected error occurred while reading zip file.")
            exit()

    @staticmethod
    def count_products(root: ET.Element) -> None:
        count: int = len(root.findall(".//item"))
        print(f"Total products in the XML file: {count}")

    @staticmethod
    def show_products(root: ET.Element) -> None:
        items: list = root.findall(".//item")
        for item in items:
            print(f'{item.get("name")}')

    @staticmethod
    def show_spare_parts(root: ET.Element) -> None:
        parts: list = root.findall(".//item/parts/part/item")
        for item in parts:
            print(f'{item.get("name")}')

    def process_choice(self) -> None:
        option_1: str = "Count products"
        option_2: str = "Show products"
        option_3: str = "Show available product spare parts"

        user_choice = input(
            f"Please choose an operation:\n"
            f"1. {option_1}\n"
            f"2. {option_2}\n"
            f"3. {option_3}\n"
            f"Enter a number: "
        )

        root: Optional[ET.Element] = None

        try:
            root = ET.fromstring(self.xml_contents)
        except ET.ParseError as e:
            print(f"Failed to parse XML: {str(e)}")
            exit()

        if user_choice == "1":
            self.count_products(root)

        elif user_choice == "2":
            self.show_products(root)

        elif user_choice == "3":
            self.show_spare_parts(root)

        else:
            print("Invalid choice")


if __name__ == "__main__":
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Process a zip archive containing XML files."
    )
    parser.add_argument("zip_file_path", type=str, help="path to the zip archive")
    args: argparse.Namespace = parser.parse_args()

    xml_parser: ZipXMLParser = ZipXMLParser(args.zip_file_path)
    xml_parser.open_zip_file()
    xml_parser.process_choice()
