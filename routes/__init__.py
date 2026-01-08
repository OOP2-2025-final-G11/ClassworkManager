def get_blueprints():
    from .timetable import timetable_bp
    from .todo import todo_bp
    return [timetable_bp, todo_bp]
