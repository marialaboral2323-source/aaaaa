#include <openssl/sha.h>

#include <atomic>
#include <cctype>
#include <cstdint>
#include <cstdlib>
#include <iomanip>
#include <iostream>
#include <sstream>
#include <string>
#include <thread>
#include <vector>

static int hexval(char c) {
  if ('0' <= c && c <= '9') return c - '0';
  if ('a' <= c && c <= 'f') return c - 'a' + 10;
  if ('A' <= c && c <= 'F') return c - 'A' + 10;
  return -1;
}

static bool hex_to_bytes(const std::string& hex, std::vector<unsigned char>* out) {
  if ((hex.size() % 2) != 0) return false;
  out->clear();
  out->reserve(hex.size() / 2);
  for (size_t i = 0; i < hex.size(); i += 2) {
    int hi = hexval(hex[i]);
    int lo = hexval(hex[i + 1]);
    if (hi < 0 || lo < 0) return false;
    out->push_back(static_cast<unsigned char>((hi << 4) | lo));
  }
  return true;
}

// Interpret "ends with 30 zero bits" as:
// last 3 bytes == 0 and low 6 bits of the 4th-last byte == 0.
static inline bool has_30_trailing_zero_bits(const unsigned char digest[SHA256_DIGEST_LENGTH]) {
  return digest[31] == 0 && digest[30] == 0 && digest[29] == 0 && (digest[28] & 0x3F) == 0;
}

static std::string bytes_to_hex(const unsigned char* bytes, size_t n) {
  std::ostringstream oss;
  oss << std::hex << std::setfill('0');
  for (size_t i = 0; i < n; i++) {
    oss << std::setw(2) << static_cast<unsigned>(bytes[i]);
  }
  return oss.str();
}

int main(int argc, char** argv) {
  if (argc != 2) {
    std::cerr << "usage: " << argv[0] << " <prefix_hex>\n";
    return 2;
  }

  std::string prefix_hex = argv[1];
  std::vector<unsigned char> prefix;
  if (!hex_to_bytes(prefix_hex, &prefix)) {
    std::cerr << "invalid hex prefix\n";
    return 2;
  }

  SHA256_CTX base;
  SHA256_Init(&base);
  SHA256_Update(&base, prefix.data(), prefix.size());

  const unsigned nthreads = std::max(1u, std::thread::hardware_concurrency());
  std::atomic<bool> found{false};
  std::atomic<uint64_t> winner{0};

  auto worker = [&](uint64_t start) {
    unsigned char suffix[8];
    unsigned char digest[SHA256_DIGEST_LENGTH];

    for (uint64_t x = start; !found.load(std::memory_order_relaxed); x += nthreads) {
      // Use big-endian for stable hex output.
      for (int i = 0; i < 8; i++) suffix[i] = static_cast<unsigned char>((x >> (8 * (7 - i))) & 0xFF);

      SHA256_CTX ctx = base;
      SHA256_Update(&ctx, suffix, sizeof(suffix));
      SHA256_Final(digest, &ctx);

      if (has_30_trailing_zero_bits(digest)) {
        if (!found.exchange(true)) {
          winner.store(x);
        }
        return;
      }
    }
  };

  std::vector<std::thread> threads;
  threads.reserve(nthreads);
  for (unsigned t = 0; t < nthreads; t++) threads.emplace_back(worker, t);
  for (auto& th : threads) th.join();

  uint64_t x = winner.load();
  unsigned char suffix[8];
  for (int i = 0; i < 8; i++) suffix[i] = static_cast<unsigned char>((x >> (8 * (7 - i))) & 0xFF);
  std::cout << bytes_to_hex(suffix, sizeof(suffix)) << "\n";
  return 0;
}

