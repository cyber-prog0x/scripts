#!/usr/bin/env bash

set -uex
umask 0077

yum makecache
yum install autoconf -y
yum install automake -y

for i in $(rpm -qa | grep openssh);do rpm -e $i --nodeps;done
ZLIB_VERSION=1.3.1
OPENSSL_VERSION=1.1.1w
OPENSSH_VERSION=8.4p1

cp /etc/pam.d/sshd /etc/pam.d/sshd_bak

prefix="/opt/openssh"
top="$(pwd)"
root="$top/root"
build="$top/build"
dist="$top/dist"

export "CPPFLAGS=-I$root/include -L. -fPIC"
export "CFLAGS=-I$root/include -L. -fPIC"
export "LDFLAGS=-L$root/lib -L$root/lib64"

#COMMENT THIS for debugging the script. Each stage will cache download and build
#rm -rf "$root" "$build" "$dist"
mkdir -p "$root" "$build" "$dist"
rm -rf $root/*
rm -rf $build/*

cp $dist/*.tar.gz $build
cd $build && tar xvf zlib-1.3.1.tar.gz
cd $build && tar xvf openssh-8.9p1.tar.gz
cd $build && tar xvf openssl-1.1.1w.tar.gz

echo "---- Building ZLIB -----"
cd "$build"/zlib-*
./configure --prefix="$root" --static
make
make install
cd "$top"

echo "---- Building OpenSSL -----"
cd "$build"/openssl-1.1.1w
./config --prefix="$root" no-shared no-tests
make
make install

cd "$build"/openssh-*
cp -p "$root"/lib/*.a .
export PATH=$root/bin:$PATH 
autoreconf
./configure LIBS="-pthread" --prefix=/usr "--with-ssl-dir=$root" --sysconfdir=/etc/ssh  --with-md5-passwords  --with-pam --with-tcp-wrappers  --without-hardening
make
make install

cp -a contrib/redhat/sshd.init  /etc/init.d/sshd
cp -a contrib/redhat/sshd.pam /etc/pam.d/sshd.pam
chmod u+x /etc/init.d/sshd
# vim /etc/ssh/sshd_config
chmod 0600 /etc/ssh/ssh_host_ed25519_key
chmod 0600 /etc/ssh/ssh_host_ecdsa_key
chmod 0600 /etc/ssh/ssh_host_rsa_key
cd "$top"

cp /etc/pam.d/sshd_bak /etc/pam.d/sshd

chkconfig --add sshd
chkconfig sshd on

systemctl daemon-reload
systemctl start sshd
systemctl status sshd

# https://www.cnblogs.com/pengpengboshi/p/16034000.html
# https://blog.csdn.net/juxua_xatu/article/details/51823195


