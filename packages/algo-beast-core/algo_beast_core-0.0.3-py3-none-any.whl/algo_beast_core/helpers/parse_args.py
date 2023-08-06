def parse_args(key, value):
  filtered_key = f"--{key}="
  items = [item.replace(filtered_key, "") for item in value if filtered_key in item]
  return items[0] if len(items) > 0 else None