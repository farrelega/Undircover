import requests
import time
from concurrent.futures import ThreadPoolExecutor
import argparse
import os

def banner():
    print("""
                                                    
██╗   ██╗███╗   ██╗██████╗ ██╗██████╗  ██████╗ ██████╗ ██╗   ██╗███████╗██████╗ 
██║   ██║████╗  ██║██╔══██╗██║██╔══██╗██╔════╝██╔═══██╗██║   ██║██╔════╝██╔══██╗
██║   ██║██╔██╗ ██║██║  ██║██║██████╔╝██║     ██║   ██║██║   ██║█████╗  ██████╔╝
██║   ██║██║╚██╗██║██║  ██║██║██╔══██╗██║     ██║   ██║╚██╗ ██╔╝██╔══╝  ██╔══██╗
╚██████╔╝██║ ╚████║██████╔╝██║██║  ██║╚██████╗╚██████╔╝ ╚████╔╝ ███████╗██║  ██║
 ╚═════╝ ╚═╝  ╚═══╝╚═════╝ ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝   ╚═══╝  ╚══════╝╚═╝  ╚═╝
                                                                                    
Undircover - Stealthy Subdomain Discovery Tool
Version 1.0 | Python Subdomain Enumerator
Created by Farrel Ega N R
""")

def load_wordlist(wordlist_path):
    try:
        with open(wordlist_path, 'r') as file:
            return [line.strip() for line in file if line.strip()]
    except Exception as e:
        print(f"[-] Error loading wordlist: {e}")
        exit(1)

def scan_target(target, protocol, timeout, wordlist=None, scan_type="subdomain"):
    results = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
    }

    def check_url(url):
        try:
            response = requests.get(
                url,
                headers=headers,
                timeout=timeout,
                allow_redirects=True,
                verify=False
            )
            
            # Special handling for JuiceShop
            if "OWASP Juice Shop" in response.text:
                return url, f"JuiceShop Detected (Status: {response.status_code})"
            
            if response.status_code < 400:
                return url, f"Active (Status: {response.status_code})"
                
        except requests.exceptions.SSLError:
            return url, "SSL Error - Try with http"
        except requests.exceptions.RequestException as e:
            return url, f"Error: {type(e).__name__}"
        except Exception as e:
            return url, f"Unexpected Error: {str(e)}"
        return None

    start_time = time.time()
    
    if scan_type == "subdomain":
        print(f"\n[+] Scanning subdomains for: {target}")
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            for word in wordlist:
                url = f"{protocol}://{word}.{target}"
                futures.append(executor.submit(check_url, url))
            
            for future in futures:
                result = future.result()
                if result:
                    url, message = result
                    print(f"[+] Found: {url} - {message}")
                    results.append(url)
    
    elif scan_type == "path":
        print(f"\n[+] Scanning paths for: {protocol}://{target}")
        paths = [
            "/", "/#/", "/#/login", "/#/search", 
            "/api", "/admin", "/rest", "/graphql"
        ]
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = []
            for path in paths:
                url = f"{protocol}://{target}{path}"
                futures.append(executor.submit(check_url, url))
            
            for future in futures:
                result = future.result()
                if result:
                    url, message = result
                    print(f"[+] Found: {url} - {message}")
                    results.append(url)
    
    elapsed_time = time.time() - start_time
    print(f"\n[+] Scan completed in {elapsed_time:.2f} seconds")
    return results

def main():
    parser = argparse.ArgumentParser(description="Undircover - Advanced Web Scanner")
    parser.add_argument("-t", "--target", help="Target domain or URL (e.g., example.com or juice-shop.herokuapp.com)")
    parser.add_argument("-w", "--wordlist", help="Path to wordlist file (for subdomain scanning)")
    parser.add_argument("-p", "--protocol", choices=["http", "https"], default="https", help="Protocol to use")
    parser.add_argument("-to", "--timeout", type=int, default=15, help="Timeout in seconds")
    parser.add_argument("-m", "--mode", choices=["subdomain", "path"], default="subdomain", help="Scanning mode")
    
    args = parser.parse_args()
    
    banner()
    
    if not args.target:
        parser.print_help()
        print("\nExamples:")
        print("  Subdomain scan: python undircover.py -t example.com -w wordlist.txt")
        print("  Path scan: python undircover.py -t juice-shop.herokuapp.com -m path")
        exit(1)

    try:
        if args.mode == "subdomain" and not args.wordlist:
            print("[-] Wordlist required for subdomain scanning")
            exit(1)
        
        wordlist = load_wordlist(args.wordlist) if args.wordlist else None
        results = scan_target(
            target=args.target,
            protocol=args.protocol,
            timeout=args.timeout,
            wordlist=wordlist,
            scan_type=args.mode
        )
        
        if not results:
            print("[-] No active targets found")
        
    except KeyboardInterrupt:
        print("\n[-] Scan interrupted by user")
    except Exception as e:
        print(f"[-] Critical error: {e}")

if __name__ == "__main__":
    main()