/usr/share/rebost/rebostCli.py {
  include <abstractions/base>
  /usr/bin/env cx,
  /usr/{,local/}lib/python3*/dist-packages/** mr,
  /usr/share/rebost/rebostCli.py cxrm,
  /run/dbus/system_bus_socket rw,
  /usr/bin/python3* cixrmw,
  dbus,
  network,
  }
