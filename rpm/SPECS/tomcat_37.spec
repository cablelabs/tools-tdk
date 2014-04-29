##############################################################
#
# Spec for creating Apache Tomcat RPM
#
###############################################################

# Hack to remove jar changing by brp-java-repack-jars
%define __os_install_post \
    /usr/lib/rpm/brp-compress ; \
    %{!?__debug_package:/usr/lib/rpm/brp-strip %{__strip}} ; \
    /usr/lib/rpm/brp-strip-static-archive %{__strip} ; \
    /usr/lib/rpm/brp-strip-comment-note %{__strip} %{__objdump} ; \
    /usr/lib/rpm/brp-python-bytecompile ; \
%{nil}

# Hack to avoid building debug packages
%define debug_package %{nil}
%define debug_packages %{nil}

%define default_install_prefix /opt/comcast/software/tomcat

# FIXME: This is the same uid/gid as the default RPM package - check if problem
%define tcuid 91


Name:           apache-tomcat
Version:        6.0.37
Release:        18%{?dist}
Summary:        Apache Tomcat 
Group:          CCP
License:        GPL
URL:            http://tomcat.apache.org/

# From the site http://tomcat.apache.org/
Source:         %{name}-%{version}.tar.gz

# For creating the Unix Daemon {start|stop|restart}
Source1:        tomcat6

# Runner file needed for init script to run properly.
#Source2:        tomcatRunner

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}
Prefix: %{default_install_prefix}

BuildArch: i586

# Install Prereqisites
Requires: jdk >= 1.6.0

%description
Apache Tomcat installer spec file.

%prep
%setup -q

%build
LANG=C

%install
rm -rf %{buildroot}
install -m 755 -d %{buildroot}%{prefix}/%{name}-%{version}
cp -r bin %{buildroot}%{prefix}/%{name}-%{version}
cp -r conf %{buildroot}%{prefix}/%{name}-%{version}
cp -r lib %{buildroot}%{prefix}/%{name}-%{version}
cp -r logs %{buildroot}%{prefix}/%{name}-%{version}
cp -r temp %{buildroot}%{prefix}/%{name}-%{version}
cp -r webapps %{buildroot}%{prefix}/%{name}-%{version}
cp -r work %{buildroot}%{prefix}/%{name}-%{version}
cp -r LICENSE %{buildroot}%{prefix}/%{name}-%{version}
cp -r NOTICE %{buildroot}%{prefix}/%{name}-%{version}
cp -r RELEASE-NOTES %{buildroot}%{prefix}/%{name}-%{version}
cp -r RUNNING.txt %{buildroot}%{prefix}/%{name}-%{version}

#copy tomcat start|stop| script.
install -m 755 -d %{buildroot}/etc/init.d/
cp -r %{SOURCE1} %{buildroot}/etc/init.d/
#cp -r %{SOURCE2} %{buildroot}/etc/init.d/

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{prefix}/%{name}-%{version}/bin
%{prefix}/%{name}-%{version}/conf
%{prefix}/%{name}-%{version}/lib
%{prefix}/%{name}-%{version}/logs
%{prefix}/%{name}-%{version}/temp
%{prefix}/%{name}-%{version}/webapps
%{prefix}/%{name}-%{version}/work
%{prefix}/%{name}-%{version}/LICENSE
%{prefix}/%{name}-%{version}/NOTICE
%{prefix}/%{name}-%{version}/RELEASE-NOTES
%{prefix}/%{name}-%{version}/RUNNING.txt

/etc/init.d/tomcat6
#/etc/init.d/tomcatRunner


%pre
# Add the "tomcat" user and group
# we need a shell to be able to use su - later
%{_sbindir}/groupadd -g %{tcuid} -r tomcat 2> /dev/null || :
# FIXME: Fix home directory
%{_sbindir}/useradd -c "Tomcat" -u %{tcuid} -g tomcat \
    -s /bin/sh -r -d /opt/comcast/software tomcat 2> /dev/null || :


%post   
#Creates a tomcat  home link 
rm -rf %{prefix}/current
ln -s %{prefix}/%{name}-%{version} %{prefix}/current
mkdir /var/run/tomcat
chown -R tomcat:tomcat /var/run/tomcat

#chkconfig entries
pushd /etc/init.d/
chmod 755 tomcat6
chkconfig --add tomcat6
chkconfig --level 345 tomcat6 on
popd 

%preun
# Stop the service if running
service tomcat6 stop
# Remove symlinks from service
chkconfig --del tomcat6

%postun
# Remove scripts and link
echo "Uninstalling, Removing "%{default_install_prefix}", link..."
rm -rf %{prefix}/current
rm -rf %{default_install_prefix}
rm -rf /var/run/tomcat
#rm -rf /etc/init.d/tomcatRunner

%changelog
* Wed Jul 17 2013 Praveen K P <praveenkp@tataelxsi.co.in> r1
- initial build, spec file created.

