#include <fmt/format.h>
#include <fmt/core.h>
#include <string>
#include <iostream>

int main(){
	fmt::print("Hello {}", std::string("Hello"));
	return 0;
}
