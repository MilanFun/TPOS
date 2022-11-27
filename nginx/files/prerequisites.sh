#!/usr/bin/env bash

{
  echo 'Server = https://mirror.surf/archlinux/$repo/os/$arch'
  echo 'Server = https://mirror.truenetwork.ru/archlinux/$repo/os/$arch'
  echo 'Server = https://mirror.yal.sl-chat.ru/archlinux/$repo/os/$arch'
  echo 'Server = https://mirror.yandex.ru/archlinux/$repo/os/$arch'
  echo 'Server = https://mirror.kamtv.ru/archlinux/$repo/os/$arch'
} > /etc/pacman.d/mirrorlist

pacman -Syu --noconfirm
pacman -S --noconfirm python3
