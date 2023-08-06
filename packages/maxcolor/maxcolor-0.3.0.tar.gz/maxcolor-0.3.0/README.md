# MaxColor

## Based of Rich by Textualize

## Installation
Easy to install right from PyPi.


### Pipx

```bash
pipx install maxcolor
```

### Pip

```bash
pip install maxcolor
```

### Poetry

```bash
poetry add maxcolor
```

## Usage

```python
from maxcolor import console, rainbow, gradient_panel, progress

console.print(
    rainbow("Fugiat veniam labore aliquip nostrud incididunt elit cupidatat occaecat quis deserunt do eu sit consectetur dolore. Aute excepteur laboris sunt. Laborum culpa incididunt pariatur ut adipisicing proident in ex adipisicing cupidatat consequat exercitation reprehenderit. Veniam sint esse velit in. Fugiat veniam labore aliquip nostrud incididunt elit cupidatat occaecat quis deserunt do eu sit consectetur dolore. Aute excepteur laboris sunt. Laborum culpa incididunt pariatur ut adipisicing proident in ex adipisicing cupidatat consequat exercitation reprehenderit. Veniam sint esse velit in. Fugiat veniam labore aliquip nostrud incididunt elit cupidatat occaecat quis deserunt do eu sit consectetur dolore. Aute excepteur laboris sunt. Laborum culpa incididunt pariatur ut adipisicing proident in ex adipisicing cupidatat consequat exercitation reprehenderit. Veniam sint esse velit in. Fugiat veniam labore aliquip nostrud incididunt elit cupidatat occaecat quis deserunt do eu sit consectetur dolore. Aute excepteur laboris sunt. Laborum culpa incididunt pariatur ut adipisicing proident in ex adipisicing cupidatat consequat exercitation reprehenderit. Veniam sint esse velit in."
    )
)

console.print(
    gradient_panel(
        "Fugiat veniam labore aliquip nostrud incididunt elit cupidatat occaecat quis deserunt do eu sit consectetur dolore. Aute excepteur laboris sunt. Laborum culpa incididunt pariatur ut adipisicing proident in ex adipisicing cupidatat consequat exercitation reprehenderit. Veniam sint esse velit in. Fugiat veniam labore aliquip nostrud incididunt elit cupidatat occaecat quis deserunt do eu sit consectetur dolore. Aute excepteur laboris sunt. Laborum culpa incididunt pariatur ut adipisicing proident in ex adipisicing cupidatat consequat exercitation reprehenderit. Veniam sint esse velit in. Fugiat veniam labore aliquip nostrud incididunt elit cupidatat occaecat quis deserunt do eu sit consectetur dolore. Aute excepteur laboris sunt. Laborum culpa incididunt pariatur ut adipisicing proident in ex adipisicing cupidatat consequat exercitation reprehenderit. Veniam sint esse velit in. Fugiat veniam labore aliquip nostrud incididunt elit cupidatat occaecat quis deserunt do eu sit consectetur dolore. Aute excepteur laboris sunt. Laborum culpa incididunt pariatur ut adipisicing proident in ex adipisicing cupidatat consequat exercitation reprehenderit. Veniam sint esse velit in.",
        "Max Color's Gradient Panel"
    )
)
