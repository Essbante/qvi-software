import subprocess
import os

def clear_keri(prompt_confirmation=False):

    path = "/usr/local/var/keri/"
    proceed_with_deletion = False

    if prompt_confirmation:
        confirm = input(f"🚨 This will clear your keystore at '{path}'. Are you sure? (y/n): ")
        if confirm.lower() == "y":
            print("Proceeding with deletion...")
            proceed_with_deletion = True
        else:
            print("Operation cancelled by user.")
    else:
        proceed_with_deletion = True
        print(f"Proceeding with deletion of '{path}' without confirmation.")

    if proceed_with_deletion:
        try:
            if not os.path.exists(path):
                print(f"⚠️ Path not found: {path}. Nothing to remove.")
                return
            subprocess.run(["rm", "-rf", path], check=True)
            print(f"✅ Successfully removed: {path}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error removing {path}: {e}")
        except FileNotFoundError: # Should not happen with rm -rf, but good for other commands
            print(f"❌ Path not found during removal attempt (should have been caught earlier): {path}")
        except Exception as e: # Catch any other potential errors
            print(f"❌ An unexpected error occurred: {e}")

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