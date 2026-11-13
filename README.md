# Mewo Clicker

A small clicker game inspired by Cookie Clicker, starring Mewo the cat.
Click Mewo, buy upgrades, unlock achievements and hunt the golden Mewo.

![Mewo](Assets/mewo.png)

## Gameplay

- **Click Mewo** to earn money. Each click also plays a pop sound.
- **Store** — buy items (hand, sword, fish, pig, butterfly, slave Mewo) that
  generate money per second (CPS). Prices increase as you buy more.
- **Achievements** — milestones slide in from the top and pay a reward.
- **Golden Mewo** — a spinning cat appears somewhere on screen for 5–15 seconds
  every 3–10 minutes. Tap it for a big money bonus or a 3× CPS boost.
- Progress is saved to `save.toml` next to the game. Delete that file to reset.

Desktop controls: mouse, `F11` toggles fullscreen.

## Run from source

Requires **Python 3.11+** (`tomllib` is in the standard library).

```bash
git clone https://github.com/Arnav-unix/Mewo-clicker.git
cd Mewo-clicker

python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python main.py
```

The desktop window is resizable; it does not force fullscreen.

## Standalone executable

Prebuilt Linux binaries are attached to [Releases](https://github.com/Arnav-unix/Mewo-clicker/releases).
Download the one matching your architecture, then:

```bash
chmod +x main-linux-x86_64
./main-linux-x86_64
```

To build your own, use the checked-in spec (it bundles `Assets/` and produces a
single-file executable):

```bash
pip install pyinstaller
python3 -m PyInstaller --noconfirm --clean "Mewo Clicker.spec"
```

```bash
./dist/"Mewo Clicker"          # Linux/macOS
.\dist\Mewo Clicker.exe        # Windows
```

`save.toml` is written next to the executable, so the game folder needs to be
writable.

## Android

Prebuilt APKs are attached to [Releases](https://github.com/Arnav-unix/Mewo-clicker/releases).
The Android build targets **arm64-v8a** only. Alternatively, the Linux binary
runs under [Termux](https://termux.dev/).

To build it yourself:

- JDK **17 or 21** (Gradle does not work with newer JDKs)
- Linux host (buildozer/python-for-android)
- Roughly 10 GB free disk space; the SDK/NDK is downloaded on the first build

```bash
./build-debug.sh      # debug APK
./build-release.sh    # release APK
```

The APK is written to `bin/`. Debug builds are signed with the debug key.

Release builds read their signing config from `.env` (sourced by the script, so
it works with fish too):

```bash
cp .env.example .env
$EDITOR .env
```

```bash
P4A_RELEASE_KEYSTORE="/path/to/mewo.keystore"
P4A_RELEASE_KEYALIAS="mewo-clicker"
P4A_RELEASE_KEYSTORE_PASSWD="..."
P4A_RELEASE_KEYALIAS_PASSWD="..."
```

Quote values that contain spaces or shell characters such as `( ) $ !`. `.env`
is gitignored; `.env.example` is the committed template. Back the keystore up
somewhere safe — without it you can't ship an update that installs over an
existing release.

### Build notes

- `p4a-recipes/` contains local python-for-android recipes:
  - `pygame` pins pygame 2.6.1, drops the broken `_sprite` extension, enables the
    SIMD blitters and forces `-O2`. Without `-O2` pygame compiles at `-O0` and
    the game runs at ~13 FPS on a phone.
  - `hostpython3` adds `OPENSSL_NO_*` defines so the host Python builds against
    OpenSSL 4.
- `p4a` is pinned to a commit in `buildozer.spec`. Bump it deliberately, and
  re-test the recipes when you do.
- Buildozer caches the distribution. After changing a recipe, delete
  `.buildozer/android/platform/build-arm64-v8a/dists/mewoclicker` to force a
  rebuild — otherwise it silently reuses the old build.
- Android assets are loaded through absolute paths in `main.py`. SDL2 on Android
  resolves relative paths against the app's internal storage, not the game
  directory.

## Project layout

```
main.py                 game loop, UI, store, achievements, save handling
button.py               small reusable button widget
Assets/                 images, sounds (.ogg), font
p4a-recipes/            local python-for-android recipes
buildozer.spec          Android build configuration
build-debug.sh          buildozer android debug wrapper
build-release.sh        buildozer android release wrapper
requirements.txt        desktop Python dependencies
```

## Windows / macOS / 32-bit

The author only has Linux and Android, so those builds are untested. The source
run and PyInstaller steps above should work, but no promises.
