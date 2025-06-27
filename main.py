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
            words = file.read().splitlines()
        return words
    except FileNotFoundError:
        print(f"[-] Error: File '{wordlist_path}' not found.")
        exit(1)
    except Exception as e:
        print(f"[-] Error reading wordlist: {e}")
        exit(1)

def check_subdomain(subdomain, domain, protocol, timeout, results):
    url = f"{protocol}://{subdomain}.{domain}"
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code < 400:
            print(f"[+] Found: {url} (Status: {response.status_code})")
            results.append(url)
    except requests.ConnectionError:
        pass
    except requests.RequestException as e:
        pass
    except Exception as e:
        print(f"[-] Error checking {url}: {e}")

def enumerate_subdomains(domain, wordlist_path, protocol="http", threads=10, timeout=5):
    start_time = time.time()
    wordlist = load_wordlist(wordlist_path)
    
    print(f"\n[+] Starting subdomain enumeration for: {domain}")
    print(f"[+] Using wordlist: {wordlist_path}")
    print(f"[+] Protocol: {protocol}")
    print(f"[+] Threads: {threads}")
    print(f"[+] Timeout: {timeout} seconds\n")
    
    results = []
    
    with ThreadPoolExecutor(max_workers=threads) as executor:
        for word in wordlist:
            executor.submit(check_subdomain, word, domain, protocol, timeout, results)
    
    return results, start_time

def save_results(results, domain):
    if not results:
        return
    
    output_dir = "results"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"{output_dir}/{domain}_subdomains_{timestamp}.txt"
    
    with open(filename, 'w') as file:
        for result in results:
            file.write(result + "\n")
    
    print(f"\n[+] Results saved to: {filename}")

def main():
    parser = argparse.ArgumentParser(description="PySubEnum - Python Subdomain Enumerator")
    parser.add_argument("-d", "--domain", help="Target domain (e.g., example.com)")
    parser.add_argument("-w", "--wordlist", help="Path to wordlist file")
    parser.add_argument("-p", "--protocol", choices=["http", "https"], default="http", 
                       help="Protocol to use (http/https)")
    parser.add_argument("-t", "--threads", type=int, default=10, 
                       help="Number of threads to use (default: 10)")
    parser.add_argument("-to", "--timeout", type=int, default=5, 
                       help="Timeout in seconds for each request (default: 5)")
    
    args = parser.parse_args()
    
    if not args.domain or not args.wordlist:
        banner()
        parser.print_help()
        print("\nExample usage:")
        print("  python pysubenum.py -d example.com -w wordlist.txt")
        print("  python pysubenum.py -d example.com -w wordlist.txt -p https -t 20 -to 3")
        exit(1)
    
    banner()
    
    try:
        results, start_time = enumerate_subdomains(
            args.domain, 
            args.wordlist, 
            args.protocol, 
            args.threads, 
            args.timeout
        )
        
        elapsed_time = time.time() - start_time
        
        print("\n[+] Enumeration completed!")
        print(f"[+] Total subdomains found: {len(results)}")
        print(f"[+] Time elapsed: {elapsed_time:.2f} seconds")
        
        if results:
            print("\n[+] Found subdomains:")
            for result in results:
                print(f"  - {result}")
            
            save_results(results, args.domain)
        else:
            print("[-] No subdomains found.")
            
    except KeyboardInterrupt:
        print("\n[-] Scan interrupted by user.")
        exit(0)
    except Exception as e:
        print(f"[-] An error occurred: {e}")
        exit(1)

if __name__ == "__main__":
    main()