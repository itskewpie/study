PASSWD="test2"

if [ 1 -eq 2 ]
then
echo "Installing MySQL 5.0.."
sudo apt-get install -qqy debconf-utils
apt-get -y --purge remove mysql-server mysql-server-5.1
cat << EOF | debconf-set-selections
mysql-server mysql-server/root_password password ${PASSWD}
mysql-server mysql-server/root_password_again password ${PASSWD}
mysql-server mysql-server/root_password seen true
mysql-server mysql-server/root_password_again seen true
EOF
/usr/bin/apt-get -y install mysql-server python-mysqldb



apt-get -y --purge remove slapd ldap-utils python-ldap
cat << EOF | debconf-set-selections
slapd slapd/password1 password ${PASSWD}
slapd slapd/password2 password ${PASSWD}
EOF
/usr/bin/apt-get -y install ldap-utils python-ldap slapd


fi

cat << EOF | debconf-set-selections
dhcp3-server dhcp3-server/new_auth_behavior note true
EOF
dpkg -i dhcp3-server_3.1.1-7_amd64.deb 
