from pathlib import Path

from pythonforandroid.recipes.pygame import Pygame2Recipe


class Pygame261Recipe(Pygame2Recipe):
    version = "2.6.1"
    url = "https://github.com/pygame/pygame/archive/{version}.tar.gz"
    hostpython_prerequisites = ["setuptools", "cython>=3.1"]

    def get_recipe_env(self, arch):
        env = super().get_recipe_env(arch)
        for key in ("CFLAGS", "CXXFLAGS", "CC", "CXX"):
            if key in env:
                env[key] += " -O2"
        return env

    def prebuild_arch(self, arch):
        super().prebuild_arch(arch)
        build_dir = Path(self.get_build_dir(arch.arch))

        setup = build_dir / "Setup"
        lines = []
        for line in setup.read_text().splitlines():
            if line.startswith("_sprite "):
                continue
            if line.startswith("surface "):
                line = line.replace(
                    "src_c/surface.c",
                    "src_c/simd_blitters_sse2.c src_c/simd_blitters_avx2.c src_c/surface.c",
                    1,
                )
            lines.append(line)
        setup.write_text("\n".join(lines) + "\n")

        (build_dir / "src_c" / "cython" / "pygame" / "_sprite.pyx").unlink(missing_ok=True)


recipe = Pygame261Recipe()
