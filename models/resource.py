class ResourceState:
    """Состояние одного ресурса колонии."""

    def __init__(self, type, amount=0):
        self.type = type
        self.amount = amount

    def add(self, value):
        self.amount += value
        return True

    def spend(self, value):
        if self.amount >= value:
            self.amount -= value
            return True
        return False

    def __repr__(self):
        return f"ResourceState(type={self.type!r}, amount={self.amount})"


# Старое имя оставлено для совместимости с уже написанным кодом.
Resource = ResourceState
