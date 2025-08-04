#!/usr/bin/env python3

import os
import shutil
import subprocess
import tarfile
from pathlib import Path


def run(cmd, check=True):
    print(f"Running: {cmd}")
    subprocess.run(cmd, shell=True, check=check)


def curl_download(url, dest):
    run(f'curl -L "{url}" -o "{dest}"')


def extract_tar_gz(tar_path, extract_to="."):
    with tarfile.open(tar_path, "r:gz") as tar:
        tar.extractall(path=extract_to)


def ensure_path_in_profile(install_dir):
    shell = os.environ.get("SHELL", "")
    home = Path.home()
    profile_file = home / ".bashrc"
    if shell.endswith("zsh"):
        profile_file = home / ".zshrc"

    export_line = f'export PATH="{install_dir}:$PATH"\n'
    with open(profile_file, "a+" if profile_file.exists() else "w") as f:
        f.seek(0)
        content = f.read()
        if export_line.strip() not in content:
            f.write(export_line)
            print(f"Added {install_dir} to PATH in {profile_file}")
        else:
            print(f"{install_dir} already in PATH in {profile_file}")


def main():
    home = Path.home()
    install_dir = home / ".local" / "bin"
    install_dir.mkdir(parents=True, exist_ok=True)
    print(f"Installing tools to {install_dir}")

    ensure_path_in_profile(str(install_dir))

    # Install fzf
    fzf_version = "0.62.0"
    fzf_tarball = f"fzf-{fzf_version}-linux_amd64.tar.gz"
    fzf_url = f"https://github.com/junegunn/fzf/releases/download/v{fzf_version}/{fzf_tarball}"
    curl_download(fzf_url, fzf_tarball)
    extract_tar_gz(fzf_tarball, str(install_dir))
    os.remove(fzf_tarball)

    # Install fd
    fd_version = "v10.2.0"
    fd_tarball = f"fd-{fd_version}-x86_64-unknown-linux-gnu.tar.gz"
    fd_url = (
        f"https://github.com/sharkdp/fd/releases/download/{fd_version}/{fd_tarball}"
    )
    curl_download(fd_url, fd_tarball)
    extract_tar_gz(fd_tarball)
    fd_dir = Path(f"fd-{fd_version}-x86_64-unknown-linux-gnu")
    shutil.move(str(fd_dir / "fd"), str(install_dir / "fd"))
    shutil.rmtree(fd_dir)
    os.remove(fd_tarball)

    # Installing uv
    print("Installing uv...")
    run("curl -LsSf https://astral.sh/uv/install.sh | sh")

    # Install ruff
    print("Installing Ruff")
    run("curl -LsSf https://astral.sh/ruff/install.sh | sh")

    # --- ripgrep ---
    rg_version = "14.1.1"
    rg_tarball = f"ripgrep-{rg_version}-x86_64-unknown-linux-musl.tar.gz"
    rg_url = f"https://github.com/BurntSushi/ripgrep/releases/download/{rg_version}/{rg_tarball}"
    print(f"Downloading ripgrep from {rg_url}")
    curl_download(rg_url, rg_tarball)
    extract_tar_gz(rg_tarball)
    with tarfile.open(rg_tarball, "r:gz") as tar:
        rg_dir = tar.getnames()[0].split("/")[0]
    shutil.move(f"{rg_dir}/rg", str(install_dir / "rg"))
    shutil.rmtree(rg_dir)
    os.remove(rg_tarball)

    # Neovim
    nvim_version = "v0.11.3"
    nvim_url = f"https://github.com/neovim/neovim-releases/releases/download/{nvim_version}/nvim-linux-x86_64.appimage"
    print(f"Downloading neovim from {rg_url}")
    curl_download(nvim_url, str(install_dir / "nvim"))

    # create python env
    run("uv venv")
    run("uv pip install -r requirements.txt")

    print(
        "All tools installed successfully. Please restart your shell or source the appropriate profile file to update your PATH."
    )


if __name__ == "__main__":
    main()
