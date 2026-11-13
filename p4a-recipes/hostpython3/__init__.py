from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

import pythonforandroid

_builtin_path = (
    Path(pythonforandroid.__file__).parent / "recipes" / "hostpython3" / "__init__.py"
)
_spec = spec_from_file_location("_p4a_hostpython3_builtin", _builtin_path)
_builtin = module_from_spec(_spec)
_spec.loader.exec_module(_builtin)

_OPENSSL_FLAGS = " ".join(
    [
        "-DOPENSSL_NO_SSL3",
        "-DOPENSSL_NO_TLS1_METHOD",
        "-DOPENSSL_NO_TLS1_1_METHOD",
        "-DOPENSSL_NO_TLS1_2_METHOD",
    ]
)


class HostPython3Recipe(_builtin.HostPython3Recipe):
    def get_recipe_env(self, arch=None):
        env = super().get_recipe_env(arch)
        env["CFLAGS"] = f"{env.get('CFLAGS', '')} {_OPENSSL_FLAGS}".strip()
        return env


recipe = HostPython3Recipe()
