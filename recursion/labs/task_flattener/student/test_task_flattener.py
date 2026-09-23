from task_flattener import flatten_tasks


def test_flatten_empty_list():
    """Test flattening an empty list."""
    assert flatten_tasks([]) == []


def test_flatten_single_task_no_subtasks():
    """Test flattening a single task with no subtasks."""
    input_tasks = [{"details": "Task 1", "status": "Pending", "sub_tasks": []}]

    result = flatten_tasks(input_tasks)
    assert len(result) == 1
    assert result[0]["details"] == "Task 1"
    assert result[0]["status"] == "Pending"


def test_flatten_nested_tasks():
    """Test flattening a task with one level of subtasks."""
    input_tasks = [
        {
            "details": "Parent",
            "status": "In Progress",
            "sub_tasks": [
                {"details": "Child 1", "status": "Done", "sub_tasks": []},
                {"details": "Child 2", "status": "Pending", "sub_tasks": []},
            ],
        }
    ]

    result = flatten_tasks(input_tasks)

    assert len(result) == 3
    assert result[0]["details"] == "Parent"
    assert result[1]["details"] == "Child 1"
    assert result[2]["details"] == "Child 2"


def test_flatten_deeply_nested_tasks():
    """Test flattening deeply nested tasks."""
    input_tasks = [
        {
            "details": "Level 1",
            "sub_tasks": [
                {
                    "details": "Level 2",
                    "sub_tasks": [{"details": "Level 3", "sub_tasks": []}],
                }
            ],
        }
    ]

    result = flatten_tasks(input_tasks)

    assert len(result) == 3
    assert result[0]["details"] == "Level 1"
    assert result[1]["details"] == "Level 2"
    assert result[2]["details"] == "Level 3"


def test_flatten_multiple_top_level_tasks():
    """Test flattening multiple top-level tasks."""
    input_tasks = [
        {"details": "Task 1", "sub_tasks": [{"details": "Sub 1"}]},
        {"details": "Task 2", "sub_tasks": []},
    ]

    result = flatten_tasks(input_tasks)

    assert len(result) == 3
    assert result[0]["details"] == "Task 1"
    assert result[1]["details"] == "Sub 1"
    assert result[2]["details"] == "Task 2"
    assert result[1]["details"] == "Sub 1"
    assert result[2]["details"] == "Task 2"
