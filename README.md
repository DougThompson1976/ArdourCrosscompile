# Python script for cross compiling Ardour DAW from Arch Linux targeting Windows

WIP, lots of steps to cross compile Ardour.

This script will work best on a Arch Linux distribution, it can work on other based distros like Manjaro, however I offer no support for those.

#### Why Arch?

Out of Ubuntu, Fedora, OpenSUSE and Arch Linux, I was only successful cross compiling on Arch.

If you're on Windows, consider running this on WSL (Windows Subsystem for Linux), but you really should just use Linux, we have many free (as in price and freedom) plugins, such as Calf Studio Gear, ZynFusion, Disthro ports of LV2 / VST, TAL Plugins, and many others honorable mentions.

Compiling Ardour for Windows IS hard, under the penguin it is a lot more simple and straightforward.

# Roadmap

- [ ] Basic shell functions (rmdir, sed a file, mkdir, etc)

- [ ] Download sources, urls simple way

- [ ] Manually patch files (mainly two PKGBUILDS)

- [ ] Pacman wrapper for installing dependencies, needed ones, etc.
 
- [ ] From a finished build, package ardour

And others I might add as development goes on.

# Legal, disclaimer

Only the files that comes with this repo are under the MIT license, downloaded files and sources licenses have their own license, own creators, etc.

If you find something wrong (like me downloading a file the user should do by hand because distribution problems), let me know!!

### Ardour developers offer NO SUPPORT and WARRANTY on DIY builds and third party.

## CONSIDER SUPPORTING ARDOUR DEVELOPMENT, BUY THEIR PRODUCT OR A SUBSCRIPTION.
