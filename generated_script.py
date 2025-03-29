
from automation_functions import open_notepad

def main():
    try:
        result = open_notepad()
        if result:
            print(result)
        else:
            print("open_notepad executed successfully.")
    except Exception as e:
        print(f"Error executing function: {e}")

if __name__ == "__main__":
    main()
