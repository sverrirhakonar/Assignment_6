import json
import os

class Config:
    """
    Singleton class for managing configuration settings using __new__.
    Loads settings from JSON files and ensures only one instance exists.
    """
    _instance = None # Class variable to store the single instance

    def __new__(cls, *args, **kwargs):
        # Called BEFORE __init__. Controls object CREATION.
        if cls._instance is None:
            # Create the actual instance using the object base class __new__
            cls._instance = super().__new__(cls)
        return cls._instance # Always return the single instance

    def __init__(self, config_filepath=None, params_filepath=None):
        """
        Initialize the Singleton instance's attributes ONCE. Loads settings.
        Accepts filepaths only if not already initialized.
        """
        print("Initializing Config settings...") # For demonstration
        if config_filepath is None or params_filepath is None:
            # We must get the paths the first time.
            raise ValueError("Config filepaths must be provided during the first initialization.")

        self.settings = {}
        self._load_settings(config_filepath, params_filepath)


    def _load_settings(self, config_filepath, params_filepath):
        """Loads settings from the JSON files into self.settings dictionary."""
        print(f"Attempting to load settings...")
        # Load main config
        try:
            with open(config_filepath, 'r') as f:
                self.settings.update(json.load(f)) # Merge directly into settings
            print(f" -> Successfully loaded: {config_filepath}")
        except FileNotFoundError:
            print(f" -> ERROR: Config file not found at {config_filepath}")
        except json.JSONDecodeError:
            print(f" -> ERROR: Could not decode JSON from {config_filepath}")
        except Exception as e:
            print(f" -> ERROR: An unexpected error occurred loading {config_filepath}: {e}")

        # Load strategy parameters, storing them under a specific key
        try:
            with open(params_filepath, 'r') as f:
                self.settings['strategy_params'] = json.load(f)
            print(f" -> Successfully loaded: {params_filepath}")
        except FileNotFoundError:
            print(f" -> ERROR: Params file not found at {params_filepath}")
        except json.JSONDecodeError:
            print(f" -> ERROR: Could not decode JSON from {params_filepath}")
        except Exception as e:
            print(f" -> ERROR: An unexpected error occurred loading {params_filepath}: {e}")

    def get_setting(self, key, default=None):
        """
        Safely gets a setting value by key using a loop (supports dot notation for nested dicts).
        Returns the default value if the key path is not found or invalid.
        """
        try:
            keys = key.split('.')
            value = self.settings # Start at the top-level dictionary
            for k in keys:
                if isinstance(value, dict):
                    value = value[k] # Go one level deeper
                else:
                    raise KeyError(f"Invalid path component: '{k}' in key '{key}' leads to a non-dictionary.")
            return value # Return the final value found
        except (KeyError, TypeError):
            return default
