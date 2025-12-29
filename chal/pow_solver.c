#include <errno.h>
#include <inttypes.h>
#include <pthread.h>
#include <stdatomic.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
// OpenSSL headers
#include <openssl/sha.h>

// Finds hex suffix S such that:
//   sha256(unhex(prefix_hex + S_hex)) ends with N zero bits (trailing bits).
//
// We brute-force S as 8 bytes (16 hex chars) using a counter per thread.

typedef struct {
  SHA256_CTX base;
  int tid;
  int nthreads;
  int zero_bits;
  _Atomic int *found;
  _Atomic uint64_t *found_ctr;
} worker_args_t;

static inline void u64_to_be_bytes(uint64_t x, uint8_t out[8]) {
  out[0] = (uint8_t)(x >> 56);
  out[1] = (uint8_t)(x >> 48);
  out[2] = (uint8_t)(x >> 40);
  out[3] = (uint8_t)(x >> 32);
  out[4] = (uint8_t)(x >> 24);
  out[5] = (uint8_t)(x >> 16);
  out[6] = (uint8_t)(x >> 8);
  out[7] = (uint8_t)(x);
}

static inline int has_trailing_zero_bits(const uint8_t digest[32], int zero_bits) {
  int full_bytes = zero_bits / 8;
  int rem_bits = zero_bits % 8;

  // check full bytes from the end
  for (int i = 0; i < full_bytes; i++) {
    if (digest[31 - i] != 0)
      return 0;
  }
  if (rem_bits == 0)
    return 1;

  // Need lowest rem_bits of next byte to be zero.
  uint8_t b = digest[31 - full_bytes];
  uint8_t mask = (uint8_t)((1u << rem_bits) - 1u); // low rem_bits set
  return (b & mask) == 0;
}

static void *worker(void *vp) {
  worker_args_t *a = (worker_args_t *)vp;
  uint8_t suffix[8];
  uint8_t digest[32];
  uint64_t ctr = (uint64_t)a->tid;

  while (!atomic_load(a->found)) {
    // Stride by number of threads to partition the search space.
    u64_to_be_bytes(ctr, suffix);

    SHA256_CTX ctx = a->base; // copy
    SHA256_Update(&ctx, suffix, sizeof(suffix));
    SHA256_Final(digest, &ctx);

    if (has_trailing_zero_bits(digest, a->zero_bits)) {
      atomic_store(a->found_ctr, ctr);
      atomic_store(a->found, 1);
      break;
    }
    ctr += (uint64_t)a->nthreads;
  }
  return NULL;
}

static int hexval(char c) {
  if ('0' <= c && c <= '9')
    return c - '0';
  if ('a' <= c && c <= 'f')
    return 10 + (c - 'a');
  if ('A' <= c && c <= 'F')
    return 10 + (c - 'A');
  return -1;
}

static int unhex(const char *hex, uint8_t *out, size_t out_cap) {
  size_t n = strlen(hex);
  if ((n % 2) != 0)
    return -1;
  size_t out_n = n / 2;
  if (out_n > out_cap)
    return -2;
  for (size_t i = 0; i < out_n; i++) {
    int hi = hexval(hex[2 * i]);
    int lo = hexval(hex[2 * i + 1]);
    if (hi < 0 || lo < 0)
      return -3;
    out[i] = (uint8_t)((hi << 4) | lo);
  }
  return (int)out_n;
}

int main(int argc, char **argv) {
  if (argc != 3) {
    fprintf(stderr, "usage: %s <prefix_hex> <zero_bits>\n", argv[0]);
    return 2;
  }

  const char *prefix_hex = argv[1];
  int zero_bits = atoi(argv[2]);
  if (zero_bits < 1 || zero_bits > 256) {
    fprintf(stderr, "bad zero_bits\n");
    return 2;
  }

  uint8_t prefix[4096];
  int prefix_len = unhex(prefix_hex, prefix, sizeof(prefix));
  if (prefix_len < 0) {
    fprintf(stderr, "bad prefix_hex\n");
    return 2;
  }

  int nthreads = 0;
  long ncpu = sysconf(_SC_NPROCESSORS_ONLN);
  if (ncpu > 0 && ncpu < 256)
    nthreads = (int)ncpu;
  else
    nthreads = 4;

  SHA256_CTX base;
  SHA256_Init(&base);
  SHA256_Update(&base, prefix, (size_t)prefix_len);

  _Atomic int found = 0;
  _Atomic uint64_t found_ctr = 0;

  pthread_t *ths = calloc((size_t)nthreads, sizeof(*ths));
  worker_args_t *args = calloc((size_t)nthreads, sizeof(*args));
  if (!ths || !args) {
    fprintf(stderr, "oom\n");
    return 2;
  }

  for (int i = 0; i < nthreads; i++) {
    args[i].base = base;
    args[i].tid = i;
    args[i].nthreads = nthreads;
    args[i].zero_bits = zero_bits;
    args[i].found = &found;
    args[i].found_ctr = &found_ctr;
    if (pthread_create(&ths[i], NULL, worker, &args[i]) != 0) {
      fprintf(stderr, "pthread_create failed\n");
      return 2;
    }
  }

  for (int i = 0; i < nthreads; i++)
    pthread_join(ths[i], NULL);

  if (!atomic_load(&found)) {
    fprintf(stderr, "not found?\n");
    return 1;
  }

  uint64_t ctr = atomic_load(&found_ctr);
  uint8_t suffix[8];
  u64_to_be_bytes(ctr, suffix);

  static const char hexdigits[] = "0123456789abcdef";
  char s_hex[16 + 1];
  for (int i = 0; i < 8; i++) {
    s_hex[2 * i] = hexdigits[suffix[i] >> 4];
    s_hex[2 * i + 1] = hexdigits[suffix[i] & 0xF];
  }
  s_hex[16] = '\0';

  // Output just S (hex), newline.
  puts(s_hex);
  return 0;
}

