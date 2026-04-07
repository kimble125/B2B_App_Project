import time
import random
import requests
import urllib3
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

# SSL 인증서 강제 우회 (중소기업청 사이트 문제 대응)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def run_sminfo_crawler(username, password, target_url):
    print("[*] Init SME Info Crawler...")
    session = requests.Session()
    ua = UserAgent(os='macos')
    
    # 봇 감지 우회용 헤더 로테이션
    headers = {
        'User-Agent': ua.random,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    
    login_url = "https://sminfo.mss.go.kr/cm/sv/CSV001R0.do"
    
    try:
        print("[*] Fetching Login Page to acquire CSRF token...")
        # 1. 로그인 폼을 먼저 요청해 세션 쿠키와 토큰을 발급받음
        login_page = session.get(login_url, headers=headers, verify=False, timeout=10)
        time.sleep(random.uniform(1.0, 2.0))
        
        soup = BeautifulSoup(login_page.text, "html.parser")
        csrf_input = soup.find("input", {"name": "csrf_token"})
        
        login_data = {
            "username": username,
            "password": password
        }
        
        if csrf_input:
            login_data["csrf_token"] = csrf_input.get("value", "")
            print(f"[*] Found CSRF Token.")
        
        # 2. 로그인 포스트 진행 (SSL 검증 비활성화 적용)
        print("[*] Executing Login POST...")
        headers['Referer'] = login_url
        response = session.post(login_url, data=login_data, headers=headers, verify=False)
        
        if response.status_code == 200:
            print("[*] Login sequence responded securely.")
        
        # 3. 데이터 타겟 페이지 직접 요청
        print("[*] Scraping target page...")
        time.sleep(random.uniform(2.0, 4.0)) # 차단 방지 지연
        target_res = session.get(target_url, headers=headers, verify=False)
        
        target_soup = BeautifulSoup(target_res.text, "html.parser")
        
        # DOM 요소 추출(실제 구조에 맞춰 유연하게 파싱)
        company_elem = target_soup.select_one("td[headers='row01']")
        rep_elem = target_soup.select_one("td[headers='row02']")
        
        company_info_name = company_elem.text.strip() if company_elem else "N/A"
        rep_name = rep_elem.text.strip() if rep_elem else "N/A"
        
        print("-------------------------------")
        print(f"✅ [Target Captured] 기업명: {company_info_name}")
        print(f"✅ [Target Captured] 대표명: {rep_name}")
        print("-------------------------------")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ [Network Error] 접속 실패 또는 타임아웃: {e}")
    except Exception as e:
        print(f"❌ [Error] 크롤링 도중 오류 발생: {e}")
    finally:
        session.close()
        print("[*] Crawler Session Closed.")

if __name__ == "__main__":
    run_sminfo_crawler(
        username="kimble125",
        password="Getajob8282##",
        target_url="https://sminfo.mss.go.kr/si/ei/IEI001R0.do?cmd=com&kcd=0000078229"
    )
