DAEMON := "/etc/init.d/vp-server"

pymodule:
	cp modules/bsversionspublisher.py /usr/lib/python3/dist-packages/

crontab: install-bin
	echo "#!/bin/bash\n/usr/sbin/bsupdater" >/etc/cron.daily/updater
	
install-bin: install-utils
	echo "#!/bin/bash\npython3 /usr/lib/balaswecha/client-server/utils/updater.py" >/usr/sbin/bsupdater

install-utils: install-config pymodule
	cp -r utils /usr/lib/balaswecha/client-server/

install-api: install-config pymodule
	cp -r api /usr/lib/balaswecha/client-server/

install-config: mkdir
	cp -r config /usr/lib/balaswecha/client-server/

install-daemon: install-api
	cp vp-server.daemon $(DAEMON)
	ln -s $(DAEMON) /etc/rc0.d/K99vp-server
	ln -s $(DAEMON) /etc/rc2.d/S99vp-server
	ln -s $(DAEMON) /etc/rc3.d/S99vp-server
	ln -s $(DAEMON) /etc/rc4.d/S99vp-server
	ln -s $(DAEMON) /etc/rc5.d/S99vp-server
	ln -s $(DAEMON) /etc/rc6.d/K99vp-server

uninstall-daemon:
	rm -f $(DAEMON)
	rm -f /etc/rc0.d/K99vp-server
	rm -f /etc/rc2.d/S99vp-server
	rm -f /etc/rc3.d/S99vp-server
	rm -f /etc/rc4.d/S99vp-server
	rm -f /etc/rc5.d/S99vp-server
	rm -f /etc/rc6.d/K99vp-server

mkdir:
	mkdir -p /usr/lib/balaswecha/client-server

install: crontab install-daemon

