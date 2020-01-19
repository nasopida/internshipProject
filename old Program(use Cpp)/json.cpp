#include "json.h"
#include <iostream>

void opdata(int n)
{
	std::ifstream in("record.json");
	std::string s;
	int size = 0;
	if(in.is_open())
	{
		std::ifstream num("strlen.json");
		if(num.is_open())
		{
			int sum = 0;
			for(int num = 0; num < n; num++)
			{
				num >> size;
				sum += size;
			}
			in.seekg(sum, std::ios::beg);
			num >> size;
			s.resize(size);
			std::cout << size << std::endl;
			in.read(&s[0], size);
		}
		else
		{
			in.seekg(0,std::ios::end);
			size = in.tellg();
			s.resize(size);
			in.seekg(0, std::ios::beg);
			in.read(&s[0], size);
		}
		std::cout << s << std::endl;
	}
	else
	{
		std::cout << "cannot open file." << std::endl;	
	}
}

void ipdata(data& d)
{
	std::ofstream out("record.json", std::ios::app);

	int size = 0;
	if(out.is_open())
	{
		out << "(";
		out << "name: " << d.name << std::endl;
		out << "time: " << d.time << std::endl;
		out << "content: " << d.content;
		out << ")" << std::endl;
		std::ifstream in("record.json");
		if(in.is_open())
		{
			std::ifstream inum("strlen.json");
			if(inum.is_open())
			{
				int temp;
				int sum = 0;
				while(inum >> temp)
				{
					size = temp;
					sum +=size;
				}
				in.seekg(sum, std::ios::beg);
				temp = in.tellg();
				in.seekg(0, std::ios::end);
				size = in.tellg();
				size = size-temp-4;
				std::cout << "temp" << temp << " size" << size << std::endl;
			}
			else
			{
				in.seekg(0, std::ios::beg);
				int temp = in.tellg();
				in.seekg(0, std::ios::end);
				size = in.tellg();
				size = size - temp - 4;
			}
			std::ofstream onum("strlen.json", std::ios::app);

			if(onum.is_open())
			{
				onum << size << std::endl;
			}
		}
	}
	else
	{
		std::cout << "cannot open file." << std::endl;
	}
}
