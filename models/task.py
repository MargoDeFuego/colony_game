class Task:
    """Задача игрового процесса."""

    def __init__(self, type, priority=1, status="new", progress=0):
        self.type = type
        self.priority = priority
        self.status = status
        self.progress = progress

    def __repr__(self):
        return (
            f"Task(type={self.type!r}, priority={self.priority}, "
            f"status={self.status!r}, progress={self.progress})"
        )
