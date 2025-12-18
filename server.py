import socket
import fnmatch
from dnslib import DNSRecord, DNSHeader, RR, A

# config
host = '0.0.0.0'
port = 5354
forward_ip = '8.8.8.8'
forward_port = 53

victim = "school.com" # google.com == google.com.school.com

# pls only one frwd
RECORDS = {
    f"*.{victim}.": 'frwd',
}

# self-explanitory
def dns_lookup(domain):
    # credits to https://stackoverflow.com/a/66000439
    return list(
        i
            [4]
            [0]
        for i in 
        socket.getaddrinfo(
            domain,
            80
        )
        if i[0] is socket.AddressFamily.AF_INET and i[1] is socket.SocketKind.SOCK_RAW  
    )[0]

def resolve_local(qname):
    if qname in RECORDS:
        return RECORDS[qname]
    for pattern, ip in RECORDS.items():
        if '*' in pattern and fnmatch.fnmatch(qname, pattern):
            return ip
    return None

# dns forward
def forward_query(data):
    print("  -> Forwarding to upstream...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(2.0)
    try:
        sock.sendto(data, (forward_ip, forward_port))
        response, _ = sock.recvfrom(512)
        return response
    except socket.timeout:
        print("  !! Upstream timeout")
        return None
    finally:
        sock.close()

# actual dns response handler
def dns_response(data):
    request = DNSRecord.parse(data)
    qname = str(request.q.qname)
    qtype = request.q.qtype
    # Local resolution
    if qtype == 1:
        local_ip = resolve_local(qname)
        if local_ip:
            if local_ip == 'frwd':
                domain_part = str(qname.replace('.school.com.', ""))
                local_ip = dns_lookup(domain_part)
                if not local_ip:
                    print(f"[not found] {qname}")
                    return data
            print(f"[found] {qname} -> {local_ip}")
            reply = DNSRecord(DNSHeader(id=request.header.id, qr=1, aa=1, ra=1), q=request.q)
            reply.add_answer(RR(qname, rdata=A(local_ip)))
            return reply.pack()
        
    # Forwarding
    upstream_data = forward_query(data)
    if upstream_data:
        upstream_record = DNSRecord.parse(upstream_data)
        upstream_record.header.id = request.header.id
        return upstream_record.pack()

    # failure D:
    return data

def main():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_sock.bind((host, port))
    print(f"Active on {host}:{port}")
    print(f"Forward ip: {forward_ip}")

    while True:
        try:
            data, addr = server_sock.recvfrom(512)
            response = dns_response(data)
            server_sock.sendto(response, addr)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    main()
