# Building CavrixOS

## Prerequisites

You need a standard Linux system (or a container/VM) to build CavrixOS.

Install the build dependencies:

```bash
sudo pacman -S --needed archiso base-devel git squashfs-tools
```

## Build Process

The build process is orchestrated by a `Makefile` at the root of the project.

### 1. Build Custom Packages

```bash
make packages
```
This will compile all `PKGBUILD` files in the `packages/` directory and place the resulting `.pkg.tar.zst` files in `repositories/pkgs/`.

### 2. Build the Local Repository

```bash
make repo
```
This will run `repo-add` to create the `cavrixos.db` database in `repositories/pkgs/`.

### 3. Build the ISO

```bash
sudo make iso
```
This uses `mkarchiso` to build the live environment. The final `.iso` file will be placed in the `build/` directory.

### All in One

You can run the entire pipeline with:

```bash
sudo make all
```
