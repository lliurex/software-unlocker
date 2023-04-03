/usr/sharepzero-center/zero-center.py flags=(attach_disconnected) {
  include <abstractions/base>
  capability setgid,
  capability audit_write,
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
  ptrace (trace) peer=@{profile_name},
  ptrace (trace) peer=unconfined,
  dbus,
  network,
  /dev/pts/{,**/}* wr,
  /dev/ptmx wr,
  /dev/tty wr,
  /etc/{,**/}* r,
  /etc/apparmor.d/{,**/}* rwlkm,
  /etc/epi.token rwlk,
  audit /etc/polkit/{,**/}* rwlkm,
  /opt/{,**/}* r,
  /proc/{,**/}* rm,
  /run/{,**/}* rk,
  /run/dbus/system_bus_socket rw,
  /run/nscd/socket rw,
  /run/nslcd/socket rw,
  /sys/kernel/security/apparmor/profiles r,
  /tmp/{,**/}* rwcixlk,
  /usr/{,**/}* r,
  /{,usr/}bin/{,**/}* cixmrw,
  /{,usr/}sbin/{,**/}* cixmrw,
  /{,usr/}sbin/epi-gtk px,
  /usr/share/{,**/}* ixmrwlk,
  /usr/share/zero-center/zero-center.py ixmrw,
  /usr/share/zero-center/{,**/}* rwlkm,
  /usr/share/zero-center/zmds/* ixmrklw,
  /usr/{,local/}lib/python3*/dist-packages/{,**/}* mr,
  /var/{,**/}* r,
  @{HOME}/{,**/}* mrwkixl,
  }

