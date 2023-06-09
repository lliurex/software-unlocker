profile /usr/share/lliurex-up/lliurex-up.py flags=(attach_disconnected) {
  capability setgid,
  capability chown,
  capability fowner,
  capability dac_read_search,
  capability dac_override,
  capability kill,
  capability setuid,
  capability setpcap,
  capability fsetid,
  capability sys_nice,
  capability sys_admin,
  capability net_admin,
  capability sys_ptrace,
  audit ptrace (trace) peer=@{profile_name},
  audit ptrace peer=@{profile_name},
  include <abstractions/base>
  network,
  dbus,
  / r,
  /dev/pts/{,**/}* wr,
  /dev/ptmx wr,
  /dev/tty wr,
  /etc/{,**/}* mwr,
  /proc/@{pid}/{,**}/* mr,
  /proc/{,**/}* mr,
  /run/{,**/}* mrwlk,
  /run/nscd/socket rkw,
  /run/user/*/{,**/}* rkw,
  /{,usr/}bin/{,**/}* cixrmw,
  /usr/bin/apt-cache px -> unsecuredpkg,
  /usr/bin/apt-config px -> unsecuredpkg,
  /usr/bin/apt-get px -> unsecuredpkg,
  /usr/bin/dpkg px -> unsecuredpkg,
  /usr/{,local/}lib/python3*/dist-packages/{,**/}* mrwcx,
  /usr/{,local/}lib/python3*/distutils/{,**/}* mrwcx,
  /usr/{,local/}share/{,**/}* cixmwr,
  /usr/sbin/dpkg-unlocker-cli cixmwr,
  /usr/sbin/lliurex-up ix,
  /var/cache/{,**/}* rw,
  /var/lib/dpkg/lock lrwk,
  /var/lib/apt/{,**/}* lrwk,
  /var/log/{,**/}* lrwk,
  /var/run/{,**/}* lrwk,
  @{HOME}/{,**/}* rwkix,
  @{HOME}/.Xauthority r,
}

