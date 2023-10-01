from cx_Freeze import setup, Executable
setup(
    name = "DonutDB Velocity Developer Preview",
    version = "24.0.0.128",
    description = "A simple and faster serverless Relational Database Management System written in Python by Gautham Nair",
    executables = [Executable("donutdb.py", icon="donutdb.ico")] # Add the icon argument here
)
