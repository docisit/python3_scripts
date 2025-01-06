import dns.resolver
import itertools
##must run:pip install dnspython - to use this
def get_subdomains(domain, subdomain_list):
    found_subdomains = []
    for sub in subdomain_list:
        full_domain = f"{sub}.{domain}"
        try:
            dns.resolver.resolve(full_domain)
            found_subdomains.append(full_domain)
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
            continue
    return found_subdomains

def main():
    domain = input("Enter the domain (e.g. example.com): ")
    # A simple list of subdomain prefixes
    subdomain_list = ['www', 'mail', 'ftp', 'test', 'dev', 'api', 'blog']

    print(f"Checking for subdomains of {domain}...")
    found_subdomains = get_subdomains(domain, subdomain_list)

    if found_subdomains:
        print("Found subdomains:")
        for subdomain in found_subdomains:
            print(subdomain)
    else:
        print("No subdomains found.")

if __name__ == "__main__":
    main()
