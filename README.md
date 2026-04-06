# TikTok screenshot resizer

Resize phone screenshots and marketing art to **1206×1670** for TikTok-style vertical posts (many feeds handle this aspect better than strict 1080×1920). Images are **scaled to fit** inside the frame (nothing is cropped), **centered**, with **white** letterboxing or pillarboxing as needed. Each run writes a **new file** with a timestamp and random id so previous exports are never overwritten.

## What you get

- **Output size:** 1206×1670
- **Fit mode:** full image visible, centered on a white canvas
- **Default format:** JPEG at **high quality** (default **95**), with **4:4:4 chroma subsampling** for sharper text and UI. Adjust with `--jpeg-quality` (1–100). Use `--format png` for lossless output (larger files)
- **Output folder:** `screenshots/` (created automatically)
- **Names:** `tiktok_YYYYMMDD_HHMMSS_<6-char-hex>.jpg` (prefix configurable)

## Requirements

- **Python 3** (3.9+ recommended)
- **Pillow** (installed via `requirements.txt`)

## Quick start

```bash
git clone <YOUR_REPO_URL>
cd <repository-folder>
python3 -m pip install -r requirements.txt
python3 resize_tiktok.py path/to/screenshot.png
```

Processed files appear under `./screenshots/`.

### Examples

```bash
# One file
python3 resize_tiktok.py ./assets/promo.png

# Several files
python3 resize_tiktok.py ./a.png ./b.png ./c.png

# Custom output directory and PNG (lossless, larger files)
python3 resize_tiktok.py ./shot.png -o ./screenshots --format png

# Higher JPEG quality (up to 100)
python3 resize_tiktok.py ./shot.png --jpeg-quality 98

# Custom filename prefix
python3 resize_tiktok.py ./shot.png --prefix myapp
```

### Direct script path

If you prefer not to use the root launcher:

```bash
python3 .cursor/skills/tiktok-screenshot-resize/scripts/resize_for_tiktok.py path/to/image.png
```

### CLI options

| Option | Description |
|--------|-------------|
| `images` | One or more input image paths (required) |
| `-o`, `--output-dir` | Output directory (default: `screenshots`) |
| `--prefix` | Prefix before timestamp (default: `tiktok`) |
| `--format` | `jpg` or `png` (default: `jpg`) |
| `--jpeg-quality` | JPEG quality 1–100 (default: `95`) |
| `-h`, `--help` | Show help |

---

## Using with AI coding assistants

These tools do not share one single “skills” format. The idea is the same everywhere: **install Python + Pillow**, then **run `resize_tiktok.py`** (or the full script path) with the image paths you care about.

### Cursor

1. Clone the repo and open the folder in Cursor.
2. This project includes a **Cursor skill** at  
   `.cursor/skills/tiktok-screenshot-resize/SKILL.md`  
   Cursor picks up **project** skills from `.cursor/skills/<name>/` when that directory is part of the workspace.
3. You can ask the agent to resize images for TikTok and attach files or paste absolute paths.

If you use skills in other repos, you can copy the whole folder  
`.cursor/skills/tiktok-screenshot-resize/`  
into another project’s `.cursor/skills/` tree.

### Claude (Claude Code, desktop, etc.)

There is no automatic loader for `.cursor/skills/` in every Claude product. Practical options:

- **Run the command yourself** using the Quick start above, or  
- **Ask the assistant to run** the same command in the terminal (e.g. `python3 resize_tiktok.py "/absolute/path/to/file.png"`), or  
- Copy the short **“What to run”** section from  
  `.cursor/skills/tiktok-screenshot-resize/SKILL.md`  
  into a project note such as `CLAUDE.md` so the model always sees the exact steps.

### OpenAI Codex (CLI / IDE)

Codex skills usually live under `$CODEX_HOME/skills/` (not inside this repo). You can:

- **Use the Python workflow only:** `pip install -r requirements.txt` and `python3 resize_tiktok.py …`, or  
- **Install as a Codex skill** by copying the directory  
  `tiktok-screenshot-resize`  
  (the folder that contains `SKILL.md` and `scripts/`) into `$CODEX_HOME/skills/`, so it matches your Codex skill layout.  
  If you use the official skill installer from OpenAI, point it at this folder or your fork.

### Other assistants (GitHub Copilot, etc.)

Same as above: open the repo, install dependencies, run `resize_tiktok.py` with absolute paths when files live outside the project.

---

## Repository layout

```
.
├── README.md
├── requirements.txt
├── resize_tiktok.py          # convenience launcher
├── screenshots/              # default output (may be empty until you run the tool)
└── .cursor/
    └── skills/
        └── tiktok-screenshot-resize/
            ├── SKILL.md      # Cursor / agent instructions
            └── scripts/
                └── resize_for_tiktok.py
```

---

## Tips for GitHub

- **Tracking exports:** By default, outputs go to `screenshots/`. If you do not want JPEGs in git, add something like:

  ```gitignore
  screenshots/*
  !screenshots/.gitkeep
  ```

  and keep a `.gitkeep` in `screenshots/` if you want the folder to exist in the repo.

- **Spaces in folder names:** Cloning into a path **without spaces** avoids a few tools quoting edge cases; the commands above work either way if paths are quoted.

---

## License

Add a `LICENSE` file in this repo if you plan to open-source the project (for example MIT).
