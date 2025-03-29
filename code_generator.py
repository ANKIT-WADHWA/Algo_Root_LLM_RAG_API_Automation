def generate_code(function_name):
    """Generates Python code to execute a function."""
    return f'''
from automation import {function_name}

def main():
    try:
        result = {function_name}()
        if result:
            print(result)
        else:
            print("{function_name} executed successfully.")
    except Exception as e:
        print(f"Error executing function: {{e}}")

if __name__ == "__main__":
    main()
    '''
