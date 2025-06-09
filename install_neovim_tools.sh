#!/usr/bin/env bash

set -e

# Define destination directory
INSTALL_DIR="$HOME/.local/bin"
mkdir -p "$INSTALL_DIR"

echo "Installing tools to $INSTALL_DIR"

# Add INSTALL_DIR to PATH if not already present
PROFILE_FILE="$HOME/.bashrc"
if [[ "$SHELL" == */zsh ]]; then
  PROFILE_FILE="$HOME/.zshrc"
fi

if ! grep -q 'export PATH="$HOME/.local/bin:$PATH"' "$PROFILE_FILE"; then
  echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$PROFILE_FILE"
  echo "Added ~/.local/bin to PATH in $PROFILE_FILE"
fi

# --- fzf ---
FZF_VERSION="0.62.0"
FZF_TARBALL="fzf-${FZF_VERSION}-linux_amd64.tar.gz"
FZF_URL="https://github.com/junegunn/fzf/releases/download/v${FZF_VERSION}/${FZF_TARBALL}"

echo "Downloading fzf..."
curl -L "$FZF_URL" -o "$FZF_TARBALL"
tar -xzf "$FZF_TARBALL" -C "$INSTALL_DIR"
rm "$FZF_TARBALL"

# --- fd ---
FD_VERSION="v10.2.0"
FD_TARBALL="fd-${FD_VERSION}-x86_64-unknown-linux-gnu.tar.gz"
FD_URL="https://github.com/sharkdp/fd/releases/download/${FD_VERSION}/${FD_TARBALL}"

echo "Downloading fd..."
curl -L "$FD_URL" -o "$FD_TARBALL"
tar -xzf "$FD_TARBALL"
cp "fd-${FD_VERSION}-x86_64-unknown-linux-gnu/fd" "$INSTALL_DIR"
rm -rf "fd-${FD_VERSION}-x86_64-unknown-linux-gnu" "$FD_TARBALL"

# --- uv ---
echo "Installing uv..."
curl -LsSf https://astral.sh/uv/install.sh | sh

# --- ripgrep ---
echo "Downloading ripgrep..."
RG_VERSION="14.1.1"
RG_TARBALL="ripgrep-${RG_VERSION}-x86_64-unknown-linux-musl.tar.gz"
RG_URL="https://github.com/BurntSushi/ripgrep/releases/download/${RG_VERSION}/${RG_TARBALL}"

echo $RG_URL

curl -L "$RG_URL" -o "$RG_TARBALL"
tar -xzf "$RG_TARBALL"
RG_DIR=$(tar -tf "$RG_TARBALL" | head -1 | cut -d/ -f1)
cp "$RG_DIR/rg" "$INSTALL_DIR"
rm -rf "$RG_TARBALL" "$RG_DIR"


echo $RG_DIR

echo "All tools installed successfully. Please restart your shell or source $PROFILE_FILE to update your PATH."
