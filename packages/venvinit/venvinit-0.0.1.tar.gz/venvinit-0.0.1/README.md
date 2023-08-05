# venvinit

venvinit is a simple script to create a virtual environment and install packages from a requirements file.

## Usage

```bash
venvinit [COMMAND] [ATTR] [OPTIONS]
```

### Commands

| Command | Description |
| ------- | ----------- |
| `create` | Create a virtual environment. |
| `remove` | Remove a virtual environment. |
| `help` | Show help. |


### Attributes

| Attribute | Description |
| --------- | ----------- |
| `[VENV_NAME]` | The name of the virtual environment. |
| `[DEPS_FILE]` | The name of the dependencies file. |

**Note:** The default dependencies file is `requirements.txt`.

### Options

| Option | Description |
| ------ | ----------- |
| `-deps`, `-dependencies` | `-deps [DEPS_FILE]` |
| `-y` | Set all arguments to default values. |
| `-h`, `--help` | Show help. |
| `-v`, `--version` | Show version. |


## Installation

```bash
pip install venvinit
```

## USAGE EXAMPLES

### Create a virtual environment with default values

```bash
venvinit create -y
```

### Create a virtual environment step by step

```bash
venvinit create
```

### Create a virtual environment with custom name set

```bash
venvinit create [VENV_NAME]
```

### Create a virtual environment with dependencies installation

```bash
venvinit create [VENV_NAME] -deps
```

### Create a virtual environment with dependencies installation and custom dependencies file

```bash
venvinit create [VENV_NAME] -deps [DEPS_FILE]
```


### Activate a virtual environment

```bash
venvinit activate [VENV_NAME]
```
### Deactivate a virtual environment

```bash
venvinit deactivate [VENV_NAME]
```

### Remove a virtual environment

```bash
venvinit remove [VENV_NAME]
```
or

```bash
venvinit remove
```


## License
MIT License © 2022 [Lux Luth](https://github.com/luxluth)
