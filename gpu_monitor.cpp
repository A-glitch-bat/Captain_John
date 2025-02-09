#include <iostream>
#include <windows.h>
#include <dxgi1_6.h>
#include <pdh.h>
#include <pdhmsg.h>
#pragma comment(lib, "pdh.lib")

void GetGPUUsage()
{
    PDH_HQUERY query;
    PDH_HCOUNTER counter;
    PDH_FMT_COUNTERVALUE counterVal;

    // Query GPU usage from Performance Counters
    if (PdhOpenQuery(NULL, 0, &query) != ERROR_SUCCESS)
    {
        std::cerr << "Failed to open PDH Query!" << std::endl;
        return;
    }

    // Add GPU counter for total utilization
    if (PdhAddCounter(query, L"\\GPU Engine(*)\\Utilization Percentage", 0, &counter) != ERROR_SUCCESS)
    {
        std::cerr << "Failed to add counter!" << std::endl;
        return;
    }

    PdhCollectQueryData(query); // Initial collection

    while (true) // Infinite loop for real-time monitoring
    {
        Sleep(1000); // Refresh every second
        PdhCollectQueryData(query); // Collect new data

        if (PdhGetFormattedCounterValue(counter, PDH_FMT_DOUBLE, NULL, &counterVal) == ERROR_SUCCESS)
        {
            std::cout << "GPU Usage: " << counterVal.doubleValue << "%" << std::endl;
        }
    }
}

void ListGPUs()
{
    IDXGIFactory6* pFactory = nullptr;
    if (FAILED(CreateDXGIFactory1(__uuidof(IDXGIFactory6), (void**)&pFactory)))
    {
        std::cerr << "Failed to create DXGI Factory!" << std::endl;
        return;
    }

    IDXGIAdapter1* pAdapter = nullptr;
    for (UINT i = 0; pFactory->EnumAdapters1(i, &pAdapter) != DXGI_ERROR_NOT_FOUND; ++i)
    {
        DXGI_ADAPTER_DESC1 desc;
        pAdapter->GetDesc1(&desc);

        std::wcout << L"GPU " << i << L": " << desc.Description << std::endl;
    }

    pFactory->Release();
}

int main()
{
    std::cout << "Listing GPUs...\n";
    ListGPUs();  // Print available GPUs

    std::cout << "Monitoring GPU Usage in Real Time...\n";
    GetGPUUsage(); // Start monitoring

    return 0;
}
