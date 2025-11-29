static int forge_buffer[3];

__attribute__((noinline, used))
int *SWORD_OF_THE_HERO(int first, int second, int third) {
  forge_buffer[0] = first;
  forge_buffer[1] = second;
  forge_buffer[2] = third;
  return forge_buffer;
}

int main(void) {
  int *forged = SWORD_OF_THE_HERO(1, 2, 3);
  return forged[0] + forged[1] + forged[2];
}
