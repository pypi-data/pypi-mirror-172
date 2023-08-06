#ifdef _WIN32
#define PLUGIN_API extern "C" __declspec(dllexport)
#elif __linux__
#define PLUGIN_API extern "C"
#endif

#include "control.cuh"
 
PLUGIN_API void Initial()
{

}