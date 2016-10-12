#!/usr/bin/env ruby
require 'fileutils'

$root_dir = Dir.pwd() + '/../'

def generate_tar(version)
  appWithVersion = "balaswecha-sync-#{version}"
  Dir.mkdir(appWithVersion)
  Dir.chdir(appWithVersion) do
    copy_source()
    generate_bin()
    generate_cron()
  end
  tar_filename = "balaswecha-sync_#{version}.orig.tar.gz"
  `tar czf #{tar_filename} #{appWithVersion}`
  FileUtils.rm_rf(appWithVersion)
  tar_filename
end

def extract_tar(filename)
  `tar xzf #{filename}`
end

def copy_source()
  Dir.mkdir("lib")
  Dir.chdir("lib") do
    FileUtils.cp_r([$root_dir + 'api', $root_dir + 'config', $root_dir + 'utils'], '.')
  end
  FileUtils.cp_r( $root_dir + 'modules', '.')
  FileUtils.cp( $root_dir + 'balaswecha_sync.daemon','bsyncd')
end

def generate_bin()
  Dir.mkdir("bin")
  Dir.chdir("bin") do
    contents = <<-FILE.gsub(/^ {4}/, '')
      #!/bin/bash
      python3 /usr/lib/balaswecha/balaswecha-sync/utils/updater.py
    FILE
    File.write('bsync', contents)
  end
end

def generate_cron()
  Dir.mkdir("cron")
  Dir.chdir("cron") do
    contents = <<-FILE.gsub(/^ {4}/, '')
      #!/bin/bash
      if [ -f /usr/sbin/bsync ]; then
        /usr/sbin/bsync
      fi
    FILE
    File.write('bsync', contents)
  end
end

def generate_meta_files()
  puts "Generating Deb files ..."
  Dir.mkdir('debian')
  Dir.chdir('debian') do
    generate_changelog()
    generate_control()
    generate_compat()
    generate_copyright()
    generate_rules()
    generate_install()
    generate_format()
    generate_postinst()
    generate_prerm()
    #generate_postrm()
  end
end

def generate_copyright()
  contents = <<-FILE.gsub(/^ {4}/, '')
    GPL V3
  FILE
  File.write('copyright', contents)
end

def generate_rules()
  contents = <<-FILE.gsub(/^ {4}/, '')
    #!/usr/bin/make -f
    %:
    	dh $@
    override_dh_usrlocal:
  FILE
  File.write("rules", contents)
end

def generate_format()
  Dir.mkdir('source')
  Dir.chdir('source') do
    contents = <<-FILE.gsub(/^ {6}/, '')
      3.0 (quilt)
    FILE
    File.write('format', contents)
  end
end

def generate_install()
  contents = <<-FILE.gsub(/^ {4}/, '')
    lib/config usr/lib/balaswecha/balaswecha-sync
    lib/api usr/lib/balaswecha/balaswecha-sync
    lib/utils usr/lib/balaswecha/balaswecha-sync
    modules/balaswecha_sync.py usr/lib/python3/dist-packages
    bsyncd etc/init.d
    bin/bsync usr/sbin
    cron/bsync /etc/cron.daily
  FILE
  File.write("balaswecha-sync.install", contents)
end

def generate_control()
  contents = <<-FILE.gsub(/^ {4}/, '')
    Source: balaswecha-sync
    Maintainer: Balaswecha Team<balaswecha-dev-team@thoughtworks.com>
    Section: misc
    Priority: optional
    Standards-Version: 3.9.2
    Build-Depends: debhelper (>= 9)

    Package: balaswecha-sync
    Architecture: all
    Depends: ${shlibs:Depends}, ${misc:Depends}, python3-bottle, python3-requests
    Description: Client-Server software for balaswecha systems
  FILE
  File.write('control', contents)
end

def generate_postinst()
  contents = <<-FILE.gsub(/^ {4}/, '')
   #!/bin/sh
   if [ ! -f /etc/rc0.d/K99bsyncd ]; then
     ln -s /etc/init.d/bsyncd /etc/rc0.d/K99bsyncd
   fi
   if [ ! -f /etc/rc2.d/S99bsyncd ]; then
     ln -s /etc/init.d/bsyncd /etc/rc2.d/S99bsyncd
   fi
   if [ ! -f /etc/rc3.d/S99bsyncd ]; then
     ln -s /etc/init.d/bsyncd /etc/rc3.d/S99bsyncd
   fi
   if [ ! -f /etc/rc4.d/S99bsyncd ]; then
     ln -s /etc/init.d/bsyncd /etc/rc4.d/S99bsyncd
   fi
   if [ ! -f /etc/rc5.d/S99bsyncd ]; then
     ln -s /etc/init.d/bsyncd /etc/rc5.d/S99bsyncd
   fi
   if [ ! -f /etc/rc6.d/K99bsyncd ]; then
     ln -s /etc/init.d/bsyncd /etc/rc6.d/K99bsyncd
   fi

   service bsyncd start

   chmod u+x /usr/lib/balaswecha/balaswecha-sync/utils/*
   chmod a+x /etc/cron.daily/bsync

   if [ ! -f /usr/sbin/bsync-versions ]; then
     ln -s /usr/lib/balaswecha/balaswecha-sync/utils/versions.py /usr/sbin/bsync-versions
   fi
   if [ ! -f /usr/sbin/bsync-bundler ]; then
     ln -s /usr/lib/balaswecha/balaswecha-sync/utils/bundler.py /usr/sbin/bsync-bundler
   fi
   if [ ! -f /usr/sbin/bsync-offline-updater ]; then
     ln -s /usr/lib/balaswecha/balaswecha-sync/utils/offline-updater.py /usr/sbin/bsync-offline-updater
   fi
   if [ ! -f /usr/lib/balaswecha/balaswecha-sync/config/configuration.json ]; then
     cp /usr/lib/balaswecha/balaswecha-sync/config/configuration.json.defaults /usr/lib/balaswecha/balaswecha-sync/config/configuration.json
   fi
   exit 0
  FILE
  File.write("postinst", contents)
end

def generate_prerm()
  contents = <<-FILE.gsub(/^ {4}/, '')
   #!/bin/sh
   service bsyncd stop

   if [ -f /etc/rc0.d/K99bsyncd ]; then
     unlink /etc/rc0.d/K99bsyncd
   fi
   if [ -f /etc/rc2.d/S99bsyncd ]; then
     unlink /etc/rc2.d/S99bsyncd
   fi
   if [ -f /etc/rc3.d/S99bsyncd ]; then
     unlink /etc/rc3.d/S99bsyncd
   fi
   if [ -f /etc/rc4.d/S99bsyncd ]; then
     unlink /etc/rc4.d/S99bsyncd
   fi
   if [ -f /etc/rc5.d/S99bsyncd ]; then
     unlink /etc/rc5.d/S99bsyncd
   fi
   if [ -f /etc/rc6.d/K99bsyncd ]; then
     unlink /etc/rc6.d/K99bsyncd
   fi
   if [ -f /usr/sbin/bsync-versions ]; then
     unlink /usr/sbin/bsync-versions
   fi
   if [ -f /usr/sbin/bsync-bundler ]; then
     unlink /usr/sbin/bsync-bundler
   fi
   if [ -f /usr/sbin/bsync-offline-updater ]; then
     unlink /usr/sbin/bsync-offline-updater
   fi

   exit 0
  FILE
  File.write("prerm", contents)
end

def generate_postrm()
  contents = <<-FILE.gsub(/^ {4}/, '')
   #!/bin/sh
   exit 0
  FILE
  File.write("postrm", contents)
end


def generate_changelog()
  contents = <<-FILE.gsub(/^ {4}/, '')
    balaswecha-sync (1.0-1) UNRELEASED; urgency=low

      * Initial release. (Closes: #XXXXX)

     -- Balaswecha Team <balaswecha-dev-team@thoughtworks.com>  #{Time.now.strftime '%a, %-d %b %Y %H:%M:%S %z'}
  FILE
  File.write('changelog', contents)
end

def generate_compat()
  File.write('compat', "9\n")
end

def generate_deb
  `debuild -i -us -uc -b`
  puts ".. Done!"
end

FileUtils.rm_rf 'dist'
Dir.mkdir('dist')
Dir.chdir('dist') do
      version = "1.0"
      tar_filename = generate_tar(version)
      extract_tar(tar_filename)
      Dir.chdir("balaswecha-sync-#{version}") do
        generate_meta_files()
        generate_deb
      end
end
