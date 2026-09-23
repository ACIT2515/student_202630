"""Recursion demo for combining a list of nested groups.

This example shows how a recursive function can walk a list of groups that may
contain sub-groups, then combine them into a single flat list while preserving
full hierarchical names such as Engineering.Backend.API Team.
"""


def flatten_groups(groups: list[dict], parent_name: str = "") -> list[dict]:
    """Combine a list of nested group dictionaries into one flat list.

    Each group may contain a "sub-groups" key with more groups inside it. This
    function walks the structure recursively, removes the nested container, and
    returns a single list of group entries whose names include their full path.

    Example:
        flatten_groups([
            {"name": "A", "sub-groups": [{"name": "A1"}]}
        ])
        -> [{"name": "A"}, {"name": "A.A1"}]
    """
    flat_list: list[dict] = []

    for group in groups:
        clean_group = {}
        group_name = str(group.get("name", ""))
        full_name = f"{parent_name}.{group_name}" if parent_name else group_name

        for key, value in group.items():
            if key == "name":
                clean_group[key] = full_name
            elif key != "sub-groups":
                clean_group[key] = value

        flat_list.append(clean_group)

        child_groups = group.get("sub-groups", [])
        if child_groups:
            flat_list.extend(flatten_groups(child_groups, full_name))

    return flat_list


def main() -> None:
    """Combine a nested list of groups and print the flattened result."""
    nested_groups = [
        {
            "name": "Engineering",
            "location": "Building A",
            "sub-groups": [
                {
                    "name": "Backend",
                    "location": "Floor 2",
                    "sub-groups": [
                        {"name": "API Team", "location": "Room 201", "sub-groups": []},
                        {
                            "name": "Database Team",
                            "location": "Room 202",
                            "sub-groups": [],
                        },
                    ],
                },
                {"name": "Frontend", "location": "Floor 3", "sub-groups": []},
            ],
        }
    ]

    print("Nested groups:")
    print(nested_groups)
    print()

    flat_list = flatten_groups(nested_groups)

    print("Flattened groups:")
    for group in flat_list:
        print(group)


if __name__ == "__main__":
    main()
