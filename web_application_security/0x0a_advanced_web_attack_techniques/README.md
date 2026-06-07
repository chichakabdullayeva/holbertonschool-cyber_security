Advanced XSS Challenge - Photo Gallery Exploitation
Explore and exploit an XSS vulnerability in the provided photo gallery web application to capture the administrator’s cookie. This task simulates a real-world web attack scenario, focusing on advanced techniques in web application security.

Holberton School has created a photo gallery app for users to share their favorite pictures. While regular users can view and suggest photos, only the admin has the authority to approve and add them. Your mission is to exploit a vulnerability in the Suggestion Page to capture the admin’s cookie using a malicious payload. Successfully retrieving the admin’s cookie will allow you to obtain the flag, which is the main objective of this task.

Instructions:

Review the provided index.html file for potential vulnerabilities. Look for parameters in the JavaScript code that can be manipulated (e.g., holberton parameter in the eval function). Use the identified vulnerability to craft a malicious URL that executes your payload when accessed by the admin. Ensure the payload sends the admin’s cookies to your external webhook. Tips:

Inspect the JavaScript carefully to identify how inputs are processed. Utilize tools such as the browser’s developer console and Webhook.site to assist in payload testing and capturing cookies. Pay close attention to eval() and how the parameter holberton is being used in the provided HTML code. Review any browser behaviors (e.g., cross-origin requests) that may affect your payload delivery. Initial Endpoint: http://web0x0a.task0.hbtn Suggestion Endpoint: Suggestion Monitor Webhook for Cookies: Webhook Code base: Index.html

Holberton Notes App - SSTI Exploitation Challenge
The Holberton Notes App contains a critical Server-Side Template Injection (SSTI) vulnerability that allows attackers to execute arbitrary code through unsanitized user input. Although a blacklist is in place to block certain characters and keywords, it’s not enough to prevent exploitation.

In this challenge, your objective is to bypass the blacklist, exploit the SSTI vulnerability, and retrieve the hidden flag. This will test your understanding of templating engines, payload crafting, and blacklist bypassing techniques.

Instructions:

Visit the target application http://web0x0a.task1.hbtn and test basic payloads like {{7*7}} to check if the app evaluates expressions. Review the base code for the blacklist and try to bypass it using obfuscation techniques (e.g., Unicode encoding or splitting keywords). Once you’ve bypassed the blacklist, use the exploit to access sensitive data or environment variables containing the flag. Tools & Techniques:

Burp Suite for intercepting requests and modifying them. Python scripts for automating the testing of payloads. Familiarity with Jinja2 templating engine and obfuscation techniques to evade the blacklist. Hints :

The app uses Jinja2 as its templating engine, which processes user inputs without proper sanitization. Input sanitization is incomplete, allowing malicious template injection. A blacklist exists to block certain characters or keywords, and its details are accessible in the provided base code. App:

By reviewing the code, we can see that there is a blacklist:

Initial Endpoint: http://web0x0a.task1.hbtn Code Base: App.py

XSS vulnerability
Following a cyberattack, administrators discovered that the attacker exploited a vulnerability in a web application to access sensitive information. Your task is to understand how the attacker performed the exploit and retrieve the flag by gaining admin access.

This web application allows users to view files archived in a directory. However, there is a significant security flaw that allows an attacker to bypass certain access restrictions.

The challenge involves:

Access the web application at http://web0x0a.task2.hbtn/report. Upload a malicious XSS file containing JavaScript designed to exfiltrate the admin’s credentials to a webhook URL. Wait for the admin to review the report and execute the malicious script. Retrieve the admin credentials from your webhook. Log in to the web application as the admin using the stolen credentials. Navigate to the appropriate section of the admin panel and retrieving the flag. Endpoint: http://web0x0a.task2.hbtn/ Report Endpoint: http://web0x0a.task2.hbtn/report Good luck, and be cautious when handling security vulnerabilities!

Bypass Registration and Purchase a Course
You are tasked with testing a vulnerable e-learning platform where critical security flaws exist. The registration process has been intentionally disabled, but users are still given a free coupon that can be redeemed to purchase a course. However, this coupon can only be used once. Your mission is to bypass the registration phase, escalate your privileges to gain purchase permissions, and exploit the vulnerability in order to redeem the coupon multiple times to successfully purchase a course. The task will require you to utilize your knowledge of session hijacking, session manipulation, and other advanced web application vulnerabilities such as PHP deserialization and insecure direct object reference (IDOR).

Objective:

Bypass the Registration: The registration functionality has been disabled to prevent unauthorized sign-ups. Investigate the application’s behavior and find a way to bypass this restriction to create an account. Gain Purchase Permissions: Once you have bypassed the registration, modify your session to enable course purchases. The platform restricts users from purchasing courses unless certain conditions (such as permissions) are met. By modifying your session data, you should be able to unlock the purchase functionality. Redeem the Coupon: Although the coupon can only be redeemed once, the application may have a flaw that allows you to reuse it. Attempt to exploit this vulnerability by sending multiple synchronous requests to redeem the coupon several times, ultimately enabling you to purchase a course. Hints:

Session Hijacking: Use tools like flask-unsign to inspect and modify the session cookie. Session Modification: Change the can_buy permission in the session to allow purchasing the course. Coupon Redeem Limitation: The coupon can only be used once, but try sending multiple synchronous requests to exploit this. Tools and Resources:

Flask-Unsign: Flask-Unsign. Postman: You can use Postman to send HTTP requests, modify headers, inspect and manipulate cookies, and test for vulnerabilities like session hijacking. Burp Suite: You can use Burp Suite to inspect requests, modify parameters, and test for potential security flaws. Initial Endpoint: http://web0x0a.task3.hbtn/ Good luck!

PHP Deserialization Vulnerability - Upload Exploit
Hey hacker, we are adding the “add book” functionality to the admin section, and we want to make sure everything is secure. After our previous penetration testing, we need you to test the newly added code. We have implemented a new book object using PHP serialization to manage the book details.

Challenge Idea: The goal is to perform fuzzing to locate the upload endpoint. Once found, you will exploit this endpoint to carry out a PHP deserialization attack and retrieve the flag. You must craft a specific request using different HTTP methods, content types, and encoding techniques to bypass security measures.

Writeup:

Begin by performing fuzzing with a tool like Gobuster (or another of your choice) to locate the upload endpoint. Understand that the upload process involves unserializing the uploaded data, which may be vulnerable to attacks. Craft an exploit by modifying the file content and altering the file path to point to a sensitive file. This will trigger the deserialization vulnerability. Use Burp Suite to intercept and manipulate the request. Experiment with different HTTP methods and content-type encodings using Burp’s “Change request method” feature to effectively test different approaches. Upload the malicious object with the exploit and retrieve the flag, demonstrating the PHP deserialization vulnerability. Initial Endpoint: http://web0x0a.task4.hbtn/ File to use: exploit.txt

