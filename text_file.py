import os

class TextFile:
    def __init__(self, path: str):
        """
        Initializes the TextFile object with a given file path.
        """
        self.path = path

    def check_path(self) -> bool:
        """
        Checks if the file at the given path exists.
        """
        return os.path.exists(self.path)

    def _ensure_dir(self, dir_path: str):
        """
        Ensures that the directory and its parent directories exist.
        """
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)

    def create_file(self, text: str = ""):
        """
        Creates a file at the given path.
        If the file already exists, it will be recreated (overwritten).
        Parent directories will be created if they don't exist.
        """
        parent_dir = os.path.dirname(self.path)
        self._ensure_dir(parent_dir)
        with open(self.path, 'w') as f:
            f.write(text)

    def append_file(self, text: str = ""):
        """
        Appends text to the file. If the file does not exist,
        it will be created along with any necessary parent directories.
        """
        if not self.check_path():
            self.create_file(text) # Create file with initial text
        else:
            with open(self.path, 'a') as f:
                f.write(text)

    def write_file(self, text: str = ""):
        """
        Overwrites the file with the given text.
        Essentially a synonym for create_file in Python's 'w' mode.
        """
        self.create_file(text)

    def get_string(self) -> str:
        """
        Reads and returns the entire content of the file as a string.
        Returns an empty string if the file does not exist.
        """
        if self.check_path():
            with open(self.path, 'r') as f:
                return f.read()
        return ""

    def get_int(self) -> int:
        """
        Reads the file content and attempts to convert it to an integer.
        Returns 0 if the file doesn't exist or conversion fails.
        """
        if self.check_path():
            try:
                return int(self.get_string().strip())
            except ValueError:
                pass # Return 0 by default
        return 0

    def get_float(self) -> float:
        """
        Reads the file content and attempts to convert it to a float.
        Returns 0.0 if the file doesn't exist or conversion fails.
        """
        if self.check_path():
            try:
                return float(self.get_string().strip())
            except ValueError:
                pass # Return 0.0 by default
        return 0.0

    def get_array(self, split_char: str = "|") -> list:
        """
        Reads the file content, splits it by the given character,
        and returns a list of strings.
        Each line ending is also stripped before splitting.
        """
        if not self.check_path():
            return []
        try:
            content = self.get_string()
            # Split by newline first, then by the split_char for each non-empty line
            lines = [line.strip() for line in content.splitlines() if line.strip()]
            result = []
            for line in lines:
                result.extend(line.split(split_char))
            return result
        except Exception:
            return []

    def get_map(self, split_char: str = "=") -> dict:
        """
        Reads the file content, expecting a single key-value pair
        separated by the split_char (e.g., "key=value").
        Returns a dictionary with this single pair, or an empty dict if not found/error.
        """
        if not self.check_path():
            return {}
        output = {}
        content = self.get_string().strip()
        if content:
            parts = content.split(split_char, 1)
            if len(parts) == 2:
                output[parts[0].strip()] = parts[1].strip()
        return output

    def get_list_map(self, split_char: str = "=") -> dict:
        """
        Reads the file content, expecting multiple key-value pairs
        each on a new line (e.g., "key1=value1\nkey2=value2").
        Returns a dictionary where keys are strings and values are
        attempted to be converted to integers, otherwise kept as strings.
        """
        if not self.check_path():
            return {}

        output = {}
        lines = self.get_string().splitlines()
        for line in lines:
            line = line.strip()
            if not line:
                continue
            parts = line.split(split_char, 1)
            if len(parts) == 2:
                key = parts[0].strip()
                value_str = parts[1].strip()
                try:
                    output[key] = int(value_str)
                except ValueError:
                    output[key] = value_str
        return output   