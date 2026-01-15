def get_blueprints():
    from .timetable import timetable_bp
    from .todo import todo_bp
    from .subject import subject_bp
    return [timetable_bp, todo_bp, subject_bp]
