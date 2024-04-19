import subprocess

def update_packages(requirements_path='requirements.txt'):
    # Read packages from requirements.txt
    try:
        with open(requirements_path, 'r') as file:
            packages = [line.strip().split('==')[0] for line in file.readlines()]
    except FileNotFoundError:
        print(f"Error: {requirements_path} not found.")
        return
    
    # Update each package
    for package in packages:
        subprocess.call(f'pip install --upgrade {package}', shell=True)
    
    # Output the new versions to a new requirements file
    with open('updated_requirements.txt', 'w') as file:
        subprocess.call(['pip', 'freeze'], stdout=file)

    print("Packages updated and new requirements.txt generated as updated_requirements.txt.")

if __name__ == "__main__":
    update_packages()
