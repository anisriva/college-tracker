# Course-tracker

## Setup

### Install git

1. Download executable

   ```bash
   curl -o git.exe https://github.com/git-for-windows/git/releases/download/v2.33.0.windows.2/Git-2.33.0.2-64-bit.exe
   ```

2. Run the executable and install git

### Install dependencies

```bash
pip install xlsxwriter tk ttkthemes pyinstaller
```

### Clone repository

```bash
git clone https://github.com/anisriva/college-tracker.git
```

### Build the executable (Only for distribution)

```bash
cd college-tracker
pyinstaller  student_manager.py \
--distpath resources/make/dist \
--workpath resources/make/build \
--log-level ERROR \
--clean \
--windowed \
--onefile 
```

### Run and distribute the executable (Only for distribution)

```bash
cd college-tracker/dist
./student_manager.exe
```

## Running the source code

```bash
cd college-tracker
python student_manager.py
```
