import os

def archive_file(name, arc_dir='old'):
    # ...
    os.rename(os.path.join(arc_dir, name))
