# FTBX Ext: Alias

The `financetoolbox-alias` namespace extension allows providing an alias to other namespace extensions.

## Installation

TBD

## Usage

Add the following lines of code at the start of a python script or jupyter-notebook:

```python
import financetoolbox.alias

# Option 1: Set a single alias using env.vars or arguments
financetoolbox.alias.set_alias()
# Option 2: Set multiple aliases via the arguments
financetoolbox.alias.set_aliases(
    module_1="alias_1",
    module_2="alias_2"
)

```

For `option 1`, you can provide the `module_original_name` & `module_alias_name` arguments or set the following env.vars:
* `FTBX_MODULE_ORIGINAL_NAME`
* `FTBX_MODULE_ALIAS_NAME`

Alternatively, you can configure the alias in an empty namespace package directly. Place the following code snippet in the `__init__.py` of a new namespace package:

```python
from financetoolbox.alias import set_alias

set_alias()
```

Example:

```text
src/financetoolbox/{{my_long_namespace_package}}/...
src/financetoolbox/{{my_short_alias}}/__init__.py
```

## Known limitations

Consider that ...
