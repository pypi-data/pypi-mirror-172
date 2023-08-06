import os


__version__ = '0.1.1'


class Env:

    @staticmethod
    def get(env_key:str, *args) -> str:
        try:
            return os.environ[env_key].strip()
        except KeyError as e:
            if args:
                return args[0]
            error_msg = f"Could not read: '{env_key}' from environment variables. Did you forget to set it or provide a default?"
            raise KeyError(error_msg) from e

    @staticmethod
    def bool(env_key:str, *args) -> bool:
        """
        False if the key is not found and no default is provided.
        """
        try:
            return os.environ[env_key].lower().strip() == "true"
        except KeyError:
            if args:
                return args[0]
            return False

    @staticmethod
    def int(env_key:str, *args) -> int:
        try:
            return int(Env.get(env_key, *args))
        except (ValueError, TypeError) as e:
            raise ValueError(f"{env_key} must be an integer.") from e

    @staticmethod
    def float(env_key:str, *args) -> float:
        try:
            return float(Env.get(env_key, *args))
        except (ValueError, TypeError) as e:
            raise ValueError(f"{env_key} must be a float.") from e

    @staticmethod
    def list(env_key:str, *args) -> list:
        value = Env.get(env_key, *args)
        if isinstance(value, str):
            return value.split(",")
        return value

    @staticmethod
    def has(env_key:str) -> bool:
        return env_key in os.environ
