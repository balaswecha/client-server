DAEMON := "/etc/init.d/bsyncd"

pymodule:
	cp modules/balaswecha_sync.py /usr/lib/python3/dist-packages/

crontab: install-bin
	echo "#!/bin/bash\n/usr/sbin/bsync" >/etc/cron.daily/bsync
	
install-bin: install-utils
	echo "#!/bin/bash\npython3 /usr/lib/balaswecha/balaswecha-sync/utils/updater.py" >/usr/sbin/bsync

install-utils: install-config pymodule
	cp -r utils /usr/lib/balaswecha/balaswecha-sync/
	chmod u+x /usr/lib/balaswecha/balaswecha-sync/utils/*

install-api: install-config pymodule
	cp -r api /usr/lib/balaswecha/balaswecha-sync/

install-config: mkdir
	cp -r config /usr/lib/balaswecha/balaswecha-sync/

install-daemon: install-api
	cp balaswecha_sync.daemon $(DAEMON)
	ln -s $(DAEMON) /etc/rc0.d/K99bsyncd
	ln -s $(DAEMON) /etc/rc2.d/S99bsyncd
	ln -s $(DAEMON) /etc/rc3.d/S99bsyncd
	ln -s $(DAEMON) /etc/rc4.d/S99bsyncd
	ln -s $(DAEMON) /etc/rc5.d/S99bsyncd
	ln -s $(DAEMON) /etc/rc6.d/K99bsyncd

uninstall-daemon:
	rm -f $(DAEMON)
	rm -f /etc/rc0.d/K99bsyncd
	rm -f /etc/rc2.d/S99bsyncd
	rm -f /etc/rc3.d/S99bsyncd
	rm -f /etc/rc4.d/S99bsyncd
	rm -f /etc/rc5.d/S99bsyncd
	rm -f /etc/rc6.d/K99bsyncd

mkdir:
	mkdir -p /usr/lib/balaswecha/balaswecha-sync

install: crontab install-daemon

clean:
	rm -f */*.json
