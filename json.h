#pragma once
#include <fstream>
#include <string>
#include <ctime>

typedef struct data
{
	std::string name;
	time_t time;
	std::string content;
} data;

void opdata(int);
void ipdata(data& d);
