import os

PACKAGE_DIRS = [
    "src",
    "src/data",
    "src/features",
    "src/models",
    "src/visualization"
]

for directory in PACKAGE_DIRS:
    init_path = os.path.join(directory, "__init__.py")
    if not os.path.exists(init_path):
        with open(init_path, "w") as f:
            f.write("# Auto-generated to ensure package recognition\n")
        print(f"✅ Created: {init_path}")
    else:
        print(f"✔ Already exists: {init_path}")
