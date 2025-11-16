from scanner import Scanner
from token import Token
import os


def main():
    input_file = input("input file name: ")
    output_file = input("output file name: ")

    # ensure Tokens folder exists
    folder_path = "E:\\Facultate\\IMP\\Tokens"
    os.makedirs(folder_path, exist_ok=True)
    
    # create output file path with proper separator
    out_file_path = os.path.join(folder_path, output_file)

    if os.path.exists(out_file_path):
        os.remove(out_file_path)

    with open(out_file_path, "a") as f1:
        sc = Scanner(input_file)
        t = Token()

        while True:
            try:
                t = sc.next_token()
            except ValueError as e:
                print(f"An error occurred: {e}")
            else:
                t.print_token()
                t.print_token(f1)

                if t.get_type() == "END_OF_PROGRAM":
                    break


if __name__ == "__main__":
    main()
