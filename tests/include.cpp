#include <vector>
#include <undefined>
#include "some/fairy/land"
  #include "../and/its/parent"

/*
#include <don't parse me>
*/

// #include "don't parse me either"

#include <vector> // Duplicated include

const char * s = "#include <no I am not parsable either>.";

int main() {
  return 0;
}
