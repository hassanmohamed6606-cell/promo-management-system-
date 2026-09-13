from functools import wraps
from rich.console import Console
console = Console()

def require_role(*roles):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if not self.current_user or self.current_user.role not in roles:
                console.print("[bold red]⛔ Access denied.[/bold red] You do not have permission for this action.")
                return None
            return func(self, *args, **kwargs)
        return wrapper
    return decorator

def audit(action):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            try:
                console.log(f"[green]AUDIT[/green] {action}")
            except Exception:
                pass
            return result
        return wrapper
    return decorator
