import sys
import importlib


def check_dependencies() -> bool:
    print("Checking dependencies:")
    dependencies: list[tuple[str, str]] = [
        ('pandas', ' Data manipulation ready'),
        ('numpy', 'Numerical computation ready'),
        ('matplotlib', 'Visualization ready')
    ]
    count: int = 0
    for name, descr in dependencies:
        try:
            module = importlib.import_module(name)
            version = module.__version__
            print(f"[OK] {name} ({version}) - {descr}")
        except ImportError:
            print(f"[X] Missing dependency: {name}")
            count += 1
    return count == 0


def installation_instructions() -> None:
    print("\nPlease install the missing dependencies.")
    print("Using pip:")
    print("\tpython3 -m venv venv")
    print("\tvenv/bin/pip install -r requirements.txt")
    print("\nUsing poetry:")
    print("\tPOETRY_VIRTUALENVS_IN_PROJECT=True poetry install\n")
    print("\nUsages:")
    print("\t- venv/bin/python3 loading.py")
    print("\t\tor")
    print("\t- poetry run python3 loading.py")


def main() -> None:
    print("\nLOADING STATUS: Loading programs...\n")
    if not check_dependencies():
        installation_instructions()
        sys.exit(1)
    import numpy as np  # type: ignore
    print("\nAnalyzing Matrix data...")
    np.random.seed(42)
    data: np.ndarray = np.random.randint(0, 100, size=1000)
    import pandas as pd  # type: ignore
    print("Processing 1000 data points...")
    df: pd.DataFrame = pd.DataFrame({
        'index': np.arange(len(data)),
        'value': data
    })
    import matplotlib.pyplot as plt  # type: ignore
    print("Generating visualization...")
    plt.figure(figsize=(10, 4))
    plt.plot(df['index'], df['value'])
    plt.title("Visualization of 1000 data points")
    plt.xlabel('Index')
    plt.ylabel('Value')
    print("\nAnalysis complete!")
    save_file: str = 'matrix_analysis.png'
    plt.savefig(save_file)
    print(f"Results saved to: {save_file}")


if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        print(f"Unexpected error: {err}")
