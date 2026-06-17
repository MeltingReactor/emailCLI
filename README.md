# EmailCLI

An CLI utility built for **Arch Linux** running **Wayland with KDE Plasma 6**. It extracts configured email strings from a local configuration data file and copies them directly into the system clipboard via native Wayland protocols.

## Installation
> [!IMPORTANT]
> [**curlFolder**](https://github.com/MeltingReactor/curlFolder), **uv** and **python3**, **wl-clipboard** required to install this program.

Run this command in your terminal to set up the project folder structure, download the files, initialize an isolated virtual environment using `uv`, and grant executable rights automatically:

```bash
mkdir -p ~/Documents/emailCLI && cd ~/Documents/emailCLI && curlFolder --quiet --override-path . "https://github.com/MeltingReactor/emailCLI/raw/refs/heads/main/email.py" && uv venv && source .venv/bin/activate && uv pip install pyperclipfix && chmod +x email.py && sudo bash -c 'cat << "EOF" > /usr/local/bin/email-cli
#!/bin/bash
USER_HOME=$(eval echo "~${SUDO_USER:-$USER}")
export WAYLAND_DISPLAY="wayland-0"
export XDG_RUNTIME_DIR="/run/user/$(id -u)"
"$USER_HOME/Documents/emailCLI/.venv/bin/python" "$USER_HOME/Documents/emailCLI/email.py" "$@"
EOF' && sudo chmod +x /usr/local/bin/email-cli
```

## Post-Installation Configuration

### 1. Create your Config File
Create your configuration file inside your local folder path:

```bash
nano ~/Documents/emailCLI/config.scs
```

> [!TIP]
> Default mode controls what email will paste
> if you just run the command without options.
> `1` is *new email* and `0` is *old email*.
Paste and modify the options inside it:
```scs
[Config:SCS]
  SCS{
      version=1.0.0
    }

[Config:SCS-Python]
  SCS-Python{
      email="new@scs.org"
      old_email="old@scs.org"
      default_mode=1
    }
```

### 2. Append Tool Path to your Shell Profile
Open your `~/.zshrc` or `~/.bashrc` file and ensure the bin directory is added to your environment path lookup:

```bash
export PATH=HOME/Documents/emailCLI:PATH
```

### 3. Setup Global KDE Plasma 6 Hotkeys
To configure the keyboard shortcuts:

> [!NOTE]
> On other *desktop enviroments*, just use the command listed
> in the steps below for setting up shortcuts in your own way.

1. Open **KDE System Settings** ➔ **Keyboard** ➔ **Shortcuts**.
2. Click **Add New** ➔ **Command**.
3. In the **Command** text field, paste this path:
Here `-n` is for the new email and `-o` is for the old.
   ```bash
   zsh -ic "email.py -n"
   ```
5. Map your chosen key combination (e.g., `Meta + E`).
6. Click **Apply**.

## Uninstallation
To uninstall run this command:
```bash
rm -rf ~/Documents/emailCLI && sudo rm -f /usr/local/bin/email-cli && for rc in ~/.zshrc ~/.bashrc; do [ -f "$rc" ] && sed -i '/\/Documents\/emailCLI/d' "$rc"; done
```
