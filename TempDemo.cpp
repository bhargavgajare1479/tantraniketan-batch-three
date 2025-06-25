#include <iostream>
#include <string>
#if defined(_WIN32)
#include <windows.h>
#include <comdef.h>
#include <Wbemidl.h>
#pragma comment(lib, "wbemuuid.lib")
#elif defined(__APPLE__)
#include <sys/utsname.h>
#include <cstdlib>
#include <cstdio>
#elif defined(__linux__)
#include <sys/utsname.h>
#include <fstream>
#endif

void printOSAndModel() {
#if defined(_WIN32)
    std::cout << "Operating System: Windows\n";
    // Get device model using WMI
    HRESULT hres;
    hres = CoInitializeEx(0, COINIT_MULTITHREADED);
    if (FAILED(hres)) return;
    hres = CoInitializeSecurity(NULL, -1, NULL, NULL, RPC_C_AUTHN_LEVEL_DEFAULT, RPC_C_IMP_LEVEL_IMPERSONATE, NULL, EOAC_NONE, NULL);
    if (FAILED(hres)) { CoUninitialize(); return; }
    IWbemLocator *pLoc = NULL;
    hres = CoCreateInstance(CLSID_WbemLocator, 0, CLSCTX_INPROC_SERVER, IID_IWbemLocator, (LPVOID *)&pLoc);
    if (FAILED(hres)) { CoUninitialize(); return; }
    IWbemServices *pSvc = NULL;
    hres = pLoc->ConnectServer(_bstr_t(L"ROOT\\CIMV2"), NULL, NULL, 0, NULL, 0, 0, &pSvc);
    if (FAILED(hres)) { pLoc->Release(); CoUninitialize(); return; }
    hres = CoSetProxyBlanket(pSvc, RPC_C_AUTHN_WINNT, RPC_C_AUTHZ_NONE, NULL, RPC_C_AUTHN_LEVEL_CALL, RPC_C_IMP_LEVEL_IMPERSONATE, NULL, EOAC_NONE);
    if (FAILED(hres)) { pSvc->Release(); pLoc->Release(); CoUninitialize(); return; }
    IEnumWbemClassObject* pEnumerator = NULL;
    hres = pSvc->ExecQuery(bstr_t("WQL"), bstr_t("SELECT * FROM Win32_ComputerSystem"), WBEM_FLAG_FORWARD_ONLY | WBEM_FLAG_RETURN_IMMEDIATELY, NULL, &pEnumerator);
    if (SUCCEEDED(hres)) {
        IWbemClassObject *pclsObj = NULL;
        ULONG uReturn = 0;
        while (pEnumerator) {
            HRESULT hr = pEnumerator->Next(WBEM_INFINITE, 1, &pclsObj, &uReturn);
            if (0 == uReturn) break;
            VARIANT vtProp;
            hr = pclsObj->Get(L"Model", 0, &vtProp, 0, 0);
            std::wcout << L"Device Model: " << vtProp.bstrVal << std::endl;
            VariantClear(&vtProp);
            pclsObj->Release();
        }
        pEnumerator->Release();
    }
    pSvc->Release();
    pLoc->Release();
    CoUninitialize();
#elif defined(__APPLE__)
    std::cout << "Operating System: macOS\n";
    // Get device model
    char buffer[128];
    FILE* pipe = popen("sysctl -n hw.model", "r");
    if (pipe && fgets(buffer, sizeof(buffer), pipe)) {
        std::cout << "Device Model: " << buffer;
    }
    if (pipe) pclose(pipe);
#elif defined(__linux__)
    std::cout << "Operating System: Linux\n";
    // Get device model
    std::ifstream modelFile("/sys/devices/virtual/dmi/id/product_name");
    std::string model;
    if (modelFile.is_open()) {
        std::getline(modelFile, model);
        std::cout << "Device Model: " << model << std::endl;
        modelFile.close();
    }
#endif
}

void printTemperatures() {
#if defined(_WIN32)
    // Use WMI to get temperature
    HRESULT hres;
    hres = CoInitializeEx(0, COINIT_MULTITHREADED);
    if (FAILED(hres)) return;
    hres = CoInitializeSecurity(NULL, -1, NULL, NULL, RPC_C_AUTHN_LEVEL_DEFAULT, RPC_C_IMP_LEVEL_IMPERSONATE, NULL, EOAC_NONE, NULL);
    if (FAILED(hres)) { CoUninitialize(); return; }
    IWbemLocator *pLoc = NULL;
    hres = CoCreateInstance(CLSID_WbemLocator, 0, CLSCTX_INPROC_SERVER, IID_IWbemLocator, (LPVOID *)&pLoc);
    if (FAILED(hres)) { CoUninitialize(); return; }
    IWbemServices *pSvc = NULL;
    hres = pLoc->ConnectServer(_bstr_t(L"ROOT\\WMI"), NULL, NULL, 0, NULL, 0, 0, &pSvc);
    if (FAILED(hres)) { pLoc->Release(); CoUninitialize(); return; }
    hres = CoSetProxyBlanket(pSvc, RPC_C_AUTHN_WINNT, RPC_C_AUTHZ_NONE, NULL, RPC_C_AUTHN_LEVEL_CALL, RPC_C_IMP_LEVEL_IMPERSONATE, NULL, EOAC_NONE);
    if (FAILED(hres)) { pSvc->Release(); pLoc->Release(); CoUninitialize(); return; }
    IEnumWbemClassObject* pEnumerator = NULL;
    hres = pSvc->ExecQuery(bstr_t("WQL"), bstr_t("SELECT * FROM MSAcpi_ThermalZoneTemperature"), WBEM_FLAG_FORWARD_ONLY | WBEM_FLAG_RETURN_IMMEDIATELY, NULL, &pEnumerator);
    if (SUCCEEDED(hres)) {
        IWbemClassObject *pclsObj = NULL;
        ULONG uReturn = 0;
        while (pEnumerator) {
            HRESULT hr = pEnumerator->Next(WBEM_INFINITE, 1, &pclsObj, &uReturn);
            if (0 == uReturn) break;
            VARIANT vtProp;
            hr = pclsObj->Get(L"CurrentTemperature", 0, &vtProp, 0, 0);
            if (vtProp.vt == VT_NULL) {
                std::cout << "Temperature: Not available\n";
            } else {
                double temp = (vtProp.uintVal / 10.0) - 273.15;
                std::cout << "Temperature: " << temp << " C\n";
            }
            VariantClear(&vtProp);
            pclsObj->Release();
        }
        pEnumerator->Release();
    }
    pSvc->Release();
    pLoc->Release();
    CoUninitialize();
#elif defined(__APPLE__)
    std::cout << "Temperature: Not available (requires SMC access, not available from standard C++)\n";
#elif defined(__linux__)
    // Try to read from /sys/class/thermal/thermal_zone*/temp
    for (int i = 0; i < 10; ++i) {
        std::string path = "/sys/class/thermal/thermal_zone" + std::to_string(i) + "/temp";
        std::ifstream tempFile(path);
        if (tempFile.is_open()) {
            int temp;
            tempFile >> temp;
            std::cout << "thermal_zone" << i << ": " << (temp / 1000.0) << " C\n";
            tempFile.close();
        }
    }
#endif
}

int main() {
    printOSAndModel();
    printTemperatures();
    return 0;
}