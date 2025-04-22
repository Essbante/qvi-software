import subprocess

def clear_keri():
    path = "/usr/local/var/keri/"
    confirm = input("🚨 This will clear your keystore. Are you sure? (y/n): ")
    if confirm.lower() == "y":
        print("Proceeding...")
        try:
            subprocess.run(["rm", "-rf", path], check=True)
            print(f"✅ Successfully removed: {path}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error removing {path}: {e}")
    else:
        print("Operation cancelled.")

def exec(command_string: str, return_all_lines: bool = False):
    ipython = get_ipython()
    if ipython is None:
        print("Warning: Not running in IPython/Jupyter.")
        return [] if return_all_lines else None

    # This is the equivalent of output_lines = !{command_string}
    output_lines = ipython.getoutput(command_string, split=True)

    if not output_lines:
        # Handle no output
        return [] if return_all_lines else None

    # Process output if it exists
    stripped_lines = [line.strip() for line in output_lines]

    if return_all_lines:
        return stripped_lines
    else:
        # We already checked output_lines is not empty
        return stripped_lines[0]