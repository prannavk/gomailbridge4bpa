def flatten_idoc_response(original_json: list[dict]) -> list[dict]:
    """Flattens the given raw iDoc response into a list of flat dicts"""
    def flatten_dict(nested_dict: dict, prefix: str = "") -> dict:
        flat = {}
        for key, value in nested_dict.items():
            if isinstance(value, dict):
                for sub_key, sub_val in value.items():
                    flat[f"{key}_{sub_key}"] = sub_val
            else:
                flat[f"{prefix}{key}"] = value
        return flat

    return [flatten_dict(entry) for entry in original_json]