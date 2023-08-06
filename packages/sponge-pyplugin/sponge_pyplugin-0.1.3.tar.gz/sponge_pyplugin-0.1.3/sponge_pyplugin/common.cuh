#ifndef COMMON_CUH
#define COMMON_CUH
#include "cuda_runtime.h"
#include "device_launch_parameters.h"
#include "string"
#include "curand_kernel.h"
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
//存储各种常数
//圆周率
#define CONSTANT_Pi 3.1415926535897932f
//自然对数的底
#define CONSTANT_e 2.7182818284590452f
//玻尔兹曼常量（kcal.mol^-1.K^ -1）
//使用kcal为能量单位，因此kB=8.31441(J.mol^-1.K^-1)/4.18407(J/cal)/1000
#define CONSTANT_kB 0.00198716f
//程序中使用的单位时间与物理时间的换算1/20.455*dt=1 ps
#define CONSTANT_TIME_CONVERTION 20.455f
//程序中使用的单位压强与物理压强的换算
// 压强单位: bar -> kcal/mol/A^3 
// (1 kcal/mol) * (4.184074e3 J/kcal) / (6.023e23 mol^-1) * (1e30 m^3/A^3) * (1e-5 bar/pa)
// 程序的压强/(kcal/mol/A^3 ) * CONSTANT_PRES_CONVERTION = 物理压强/bar
#define CONSTANT_PRES_CONVERTION 6.946827162543585e4f
// 物理压强/bar * CONSTANT_PRES_CONVERTION_INVERSE = 程序的压强/(kcal/mol/A^3 )
#define CONSTANT_PRES_CONVERTION_INVERSE 0.00001439506089041446f
//周期性盒子映射所使用的信息，最大的unsigned int
#define CONSTANT_UINT_MAX UINT_MAX
//周期性盒子映射所使用的信息，最大的unsigned int对应的float
#define CONSTANT_UINT_MAX_FLOAT 4294967296.0f
//周期性盒子映射所使用的信息，最大的unsigned int对应的倒数
#define CONSTANT_UINT_MAX_INVERSED 2.3283064365387e-10f

#define CHAR_LENGTH_MAX 256

//用于计算边界循环所定义的结构体
struct UNSIGNED_INT_VECTOR
{
    unsigned int uint_x;
    unsigned int uint_y;
    unsigned int uint_z;
};

//用于计算边界循环或者一些三维数组大小所定义的结构体
struct INT_VECTOR
{
    int int_x;
    int int_y;
    int int_z;
};

struct CONSTANT
{
    //数学常数
    const float pi = 3.1415926535897932f;
    const float e = 2.7182818284590452f;
    //物理常量
    const float kB = 0.00198716f;//玻尔兹曼常量（kcal.mol^-1.K^ -1）
                                //使用kcal为能量单位，因此kB=8.31441(J.mol^-1.K^-1)/4.18407(J/cal)/1000
    const float time_convertion=20.455f;//程序中使用的单位时间与物理时间的换算1/20.455*dt=1 ps
    //周期性盒子映射所使用的信息
    const unsigned int uint_max = UINT_MAX;
    const float uint_max_float = 4294967296.0f;
    const float uint_max_inversed = (float)1. / 4294967296.;
};

//用于存储各种三维float矢量而定义的结构体
struct VECTOR
{
    float x;
    float y;
    float z;

    friend __device__ __host__ __forceinline__ VECTOR operator+ (const VECTOR& veca, const VECTOR& vecb)
    {
        VECTOR vec;
        vec.x = veca.x + vecb.x;
        vec.y = veca.y + vecb.y;
        vec.z = veca.z + vecb.z;
        return vec;
    }

    friend __device__ __host__ __forceinline__ VECTOR operator+ (const VECTOR& veca, const float& b)
    {
        VECTOR vec;
        vec.x = veca.x + b;
        vec.y = veca.y + b;
        vec.z = veca.z + b;
        return vec;
    }

    friend __device__ __host__  __forceinline__ float operator* (const VECTOR& veca, const VECTOR& vecb)
    {
        return veca.x * vecb.x + veca.y * vecb.y + veca.z * vecb.z;
    }
    friend __device__ __host__  __forceinline__ VECTOR operator* (const float& a, const VECTOR& vecb)
    {
        VECTOR vec;
        vec.x = a * vecb.x;
        vec.y = a * vecb.y;
        vec.z = a * vecb.z;
        return vec;
    }

    friend __device__ __host__  __forceinline__ VECTOR operator- (const VECTOR& veca, const VECTOR& vecb)
    {
        VECTOR vec;
        vec.x = veca.x - vecb.x;
        vec.y = veca.y - vecb.y;
        vec.z = veca.z - vecb.z;
        return vec;
    }

    friend __device__ __host__ __forceinline__ VECTOR operator- (const VECTOR& veca, const float& b)
    {
        VECTOR vec;
        vec.x = veca.x - b;
        vec.y = veca.y - b;
        vec.z = veca.z - b;
        return vec;
    }

    friend __device__ __host__  __forceinline__ VECTOR operator- (const VECTOR& vecb)
    {
        VECTOR vec;
        vec.x = -vecb.x;
        vec.y = -vecb.y;
        vec.z = -vecb.z;
        return vec;
    }

    friend __device__ __host__  __forceinline__ VECTOR operator/ (const VECTOR& veca, const VECTOR& vecb)
    {
        VECTOR vec;
        vec.x = veca.x / vecb.x;
        vec.y = veca.y / vecb.y;
        vec.z = veca.z / vecb.z;
        return vec;
    }

    friend __device__ __host__  __forceinline__ VECTOR operator/ (const float& a, const VECTOR& vecb)
    {
        VECTOR vec;
        vec.x = a / vecb.x;
        vec.y = a / vecb.y;
        vec.z = a / vecb.z;
        return vec;
    }

    friend __device__ __host__  __forceinline__ VECTOR operator^ (const VECTOR& veca, const VECTOR& vecb)
    {
        VECTOR vec;
        vec.x = veca.y * vecb.z - veca.z * vecb.y;
        vec.y = veca.z * vecb.x - veca.x * vecb.z;
        vec.z = veca.x * vecb.y - veca.y * vecb.x;
        return vec;
    }

    friend __device__ __host__ __forceinline__ VECTOR Get_Periodic_Displacement(const UNSIGNED_INT_VECTOR uvec_a, const UNSIGNED_INT_VECTOR uvec_b, const VECTOR scaler)
    {
        VECTOR dr;
        dr.x = ((int)(uvec_a.uint_x - uvec_b.uint_x)) * scaler.x;
        dr.y = ((int)(uvec_a.uint_y - uvec_b.uint_y)) * scaler.y;
        dr.z = ((int)(uvec_a.uint_z - uvec_b.uint_z)) * scaler.z;
        return dr;
    }


    friend __device__ __host__ __forceinline__ VECTOR Get_Periodic_Displacement(const VECTOR vec_a, const VECTOR vec_b, const VECTOR box_length)
    {
        VECTOR dr;
        dr = vec_a - vec_b;
        dr.x = dr.x - floorf(dr.x / box_length.x + 0.5) * box_length.x;
        dr.y = dr.y - floorf(dr.y / box_length.y + 0.5) * box_length.y;
        dr.z = dr.z - floorf(dr.z / box_length.z + 0.5) * box_length.z;
        return dr;
    }

    friend __device__ __host__ __forceinline__ VECTOR Get_Periodic_Displacement(const VECTOR vec_a, const VECTOR vec_b, const VECTOR box_length, const VECTOR box_length_inverse)
    {
        VECTOR dr;
        dr = vec_a - vec_b;
        dr.x = dr.x - floorf(dr.x * box_length_inverse.x + 0.5) * box_length.x;
        dr.y = dr.y - floorf(dr.y * box_length_inverse.y + 0.5) * box_length.y;
        dr.z = dr.z - floorf(dr.z * box_length_inverse.z + 0.5) * box_length.z;
        return dr;
    }

    friend __device__ __forceinline__ VECTOR Make_Vector_Not_Exceed_Value(VECTOR vector, const float value)
    {
        return fminf(1.0, value * rnorm3df(vector.x, vector.y, vector.z)) * vector;
    }

    friend __device__ __forceinline__ VECTOR __ldg(VECTOR* address)
    {
        return { __ldg((float*)address), __ldg(((float*)address) + 1), __ldg(((float*)address) + 2) };
    }
};

//用于记录原子组
struct ATOM_GROUP
{
    int atom_numbers;
    int *atom_serial;
};


//用来重置一个已经分配过显存的列表：list。使用CUDA一维block和thread启用
void Reset_List(int *list, const int replace_element, const int element_numbers, const int threads = 1024);
__global__ void Reset_List(const int element_numbers, int *list, const int replace_element);
void Reset_List(float *list, const float replace_element, const int element_numbers, const int threads = 1024);
__global__ void Reset_List(const int element_numbers, float *list, const float replace_element);
//对一个列表的数值进行缩放
void Scale_List(float *list, const float scaler, const int element_numbers, const int threads = 1024);
__global__ void Scale_List(const int element_numbers, float *list, float scaler);
//用来复制一个列表
__global__ void Copy_List(const int element_numbers, const int *origin_list, int *list);
__global__ void Copy_List(const int element_numbers, const float *origin_list, float *list);
//用来将一个列表中的每个元素取其倒数
__global__ void Inverse_List_Element(const int element_numbers, const float *origin_list, float *list);
//对一个列表求和，并将和记录在sum中
void Sum_Of_List(const int *list, int *sum, const int end, int threads = 1024);
void Sum_Of_List(const float *list, float *sum, const int end, const int start = 0, int threads = 1024);
__global__ void Sum_Of_List(const int element_numbers, const int* list, int *sum);
__global__ void Sum_Of_List(const int start, const int end, const float* list, float *sum);
__global__ void Sum_Of_List(const int element_numbers, const float* list, float *sum);
__global__ void Sum_Of_List(const int element_numbers, const VECTOR* list, VECTOR *sum);

//用来将原子的真实坐标转换为unsigned int坐标,注意factor需要乘以0.5（保证越界坐标自然映回box）
__global__ void Crd_To_Uint_Crd(const int atom_numbers, const VECTOR scale_factor, const VECTOR *crd, UNSIGNED_INT_VECTOR *uint_crd);
//用来将坐标从真实坐标变为int坐标，factor不用乘以0.5，因为假设这类真实坐标总是比周期边界小得多。目前主要用于格林函数离散点的坐标映射
__global__ void Crd_To_Int_Crd(const int atom_numbers, const VECTOR scale_factor, const VECTOR *crd, INT_VECTOR *int_crd);
//用来对原子真实坐标进行周期性映射
__global__ void Crd_Periodic_Map(const int atom_numbers, VECTOR *crd, const VECTOR box_length);


//用来平移一组向量(CPU包装)
void Vector_Translation(const int vector_numbers, VECTOR *vec_list, const VECTOR translation_vec, int threads_per_block);
//用来平移gpu上的一个平移向量（并非一组）（CPU包装）
void Vector_Translation(const int vector_numbers, VECTOR *vec_list, const VECTOR *translation_vec, int threads_per_block);

//用来平移一组向量
__global__ void Vector_Translation(const int vector_numbers, VECTOR *vec_list, const VECTOR translation_vec);
//gpu上的一个平移向量（并非一组）
__global__ void Vector_Translation(const int vector_numbers, VECTOR *vec_list, const VECTOR *translation_vec);

//用于安全的显存和内存分配，以及打开文件
bool Malloc_Safely(void **address, size_t size);
bool Cuda_Malloc_Safely(void **address, size_t size);
bool Open_File_Safely(FILE **file, const char *file_name, const char *open_type);
bool Cuda_Malloc_And_Copy_Safely(void** d_address, void *h_address, size_t size, const char *var_name = NULL);

//用于生成高斯分布的随机数
//用seed初始化制定长度的随机数生成器，每个生成器一次可以生成按高斯分布的四个独立的数
__global__ void Setup_Rand_Normal_Kernel(const int float4_numbers, curandStatePhilox4_32_10_t *rand_state, const int seed);
//用生成器生成一次随机数，将其存入数组中
__global__ void Rand_Normal(const int float4_numbers, curandStatePhilox4_32_10_t *rand_state, float4 *rand_float4);

//用于GPU上的debug，将GPU上的信息打印出来
__global__ void Cuda_Debug_Print(float *x);
__global__ void Cuda_Debug_Print(VECTOR *x);
__global__ void Cuda_Debug_Print(int *x);


//用于做快速傅里叶变换前选择格点数目
int Get_Fft_Patameter(float length);
int Check_2357_Factor(int number);

/*XYJ备注：SAD=simple auto diff，简单自动微分
实现原理：利用操作符重载，将f(x,y)的关系同时用链式法则链接到df(x,y)上。效率肯定会有影响，暂时未明具体会影响多少
使用方法：1. 确定该部分需要求偏微分的数量，假设有1个，则后面使用的类就为SADfloat<1>或SADvector<1>，2个则为SADfloat<2>或SADvector<1>
2. 将包含微分的变量和过程用上面确定的类声明变量，其中对于想求的变量初始化时需要两个参数：本身的值和第i个变量
3. 正常计算，那么最后结果中的dval[i]即为第i个变量的微分。
使用样例：（均在No_PNC/generalized_Born.cu中）
1. 求有效伯恩半径对距离的导数：不求导数的函数为Effective_Born_Radii_Factor_CUDA，求导数的函数为GB_accumulate_Force_Energy_CUDA
2. 求GB能量对距离和有效伯恩半径的导数：不求导数的函数为GB_inej_Energy_CUDA，求导数的函数为GB_inej_Force_Energy_CUDA
*/
template<int N>
struct SADfloat
{
    float val;
    float dval[N];
    __device__ __host__ __forceinline__ SADfloat<N>()
    {
        this->val = 0;
        for (int i = 0; i < N; i++)
        {
            this->dval[i] = 0;
        }
    }
    __device__ __host__ __forceinline__ SADfloat<N>(int f, int id = -1)
    {
        this->val = (float)f;
        for (int i = 0; i < N; i++)
        {
            if (i != id)
                this->dval[i] = 0;
            else
                this->dval[i] = 1;
        }
    }
    __device__ __host__ __forceinline__ SADfloat<N>(float f, int id = -1)
    {
        this->val = f;
        for (int i = 0; i < N; i++)
        {
            if (i != id)
                this->dval[i] = 0;
            else
                this->dval[i] = 1;
        }
    }
    __device__ __host__ __forceinline__ SADfloat<N>(const SADfloat<N>& f)
    {
        this->val = f.val;
        for (int i = 0; i < N; i++)
        {
            this->dval[i] = f.dval[i];
        }
    }
	__device__ __host__ __forceinline__ SADfloat<N> operator-()
	{
		val = -val;
		for (int i = 0; i < N; i++)
		{
			dval[i] = -dval[i];
		}
		return *this;
	}
	__device__ __host__ __forceinline__ void operator=(const SADfloat<N>& f1)
	{
		val = f1.val;
		for (int i = 0; i < N; i++)
		{
			dval[i] = f1.dval[i];
		}
	}
	__device__ __host__ __forceinline__ void operator+=(const SADfloat<N>& f1)
	{
		val += f1.val;
		for (int i = 0; i < N; i++)
		{
			dval[i] += f1.dval[i];
		}
	}
	__device__ __host__ __forceinline__ void operator-=(const SADfloat<N>& f1)
	{
		val += f1.val;
		for (int i = 0; i < N; i++)
		{
			dval[i] += f1.dval[i];
		}
	}
	__device__ __host__ __forceinline__ void operator*=(const SADfloat<N>& f1)
	{
		val *= f1.val;
		for (int i = 0; i < N; i++)
		{
			dval[i] = f1.val * dval[i] + val * f1.dval[i];
		}
	}
	__device__ __host__ __forceinline__ void operator/=(const SADfloat<N>& f1)
	{
		val /= f1.val;
		for (int i = 0; i < N; i++)
		{
			dval[i] = dval[i] * f1.val - f1.dval[i] * val;
			dval[i] /= f1.val * f1.val;
		}
	}
    friend __device__ __host__ __forceinline__ SADfloat<N> operator+ (const SADfloat<N>& f1, const SADfloat<N>& f2)
    {
        SADfloat<N> f;
        f.val = f1.val + f2.val;
        for (int i = 0; i < N; i++)
        {
            f.dval[i] = f1.dval[i] + f2.dval[i];
        }
        return f;
    }
    friend __device__ __host__ __forceinline__ SADfloat<N> operator- (const SADfloat<N>& f1, const SADfloat<N>& f2)
    {
        SADfloat<N> f;
        f.val = f1.val - f2.val;
        for (int i = 0; i < N; i++)
        {
            f.dval[i] = f1.dval[i] - f2.dval[i];
        }
        return f;
    }
    friend __device__ __host__ __forceinline__ SADfloat<N> operator* (const SADfloat<N>& f1, const SADfloat<N>& f2)
    {
        SADfloat<N> f;
        f.val = f1.val * f2.val;
        for (int i = 0; i < N; i++)
        {
            f.dval[i] = f2.val * f1.dval[i] + f1.val * f2.dval[i];
        }
        return f;
    }
    friend __device__ __host__ __forceinline__ SADfloat<N> operator/ (const SADfloat<N>& f1, const SADfloat<N>& f2)
    {
        SADfloat<N> f;
        f.val = f1.val / f2.val;
        for (int i = 0; i < N; i++)
        {
            f.dval[i] = f1.dval[i] * f2.val - f2.dval[i] * f1.val;
            f.dval[i] /= f2.val * f2.val;
        }
        return f;
    }
    friend __device__ __host__ __forceinline__ SADfloat<N> logf (const SADfloat<N>& f)
    {
        SADfloat<N> fa;
        fa.val = logf(f.val);
        for (int i = 0; i < N; i++)
        {
            fa.dval[i] = f.dval[i] / f.val;
        }

        return fa;
    }
    friend __device__ __host__ __forceinline__ SADfloat<N> sqrtf(const SADfloat<N>& f)
    {
        SADfloat<N> fa;
        fa.val = sqrtf(f.val);
        for (int i = 0; i < N; i++)
        {
            fa.dval[i] = 0.5 / fa.val * f.dval[i];
        }
        return fa;
    }
    friend __device__ __host__ __forceinline__ SADfloat<N> expf(const SADfloat<N>& f)
    {
        SADfloat<N> fa;
        fa.val = expf(f.val);
        for (int i = 0; i < N; i++)
        {
            fa.dval[i] = fa.val * f.dval[i];
        }
        return fa;
    }
	friend __device__ __host__ __forceinline__ SADfloat<N> acosf(const SADfloat<N>& f)
	{
		SADfloat<N> fa;
		fa.val = acosf(f.val);
		for (int i = 0; i < N; i++)
		{
			fa.dval[i] = -1.0 / sqrtf(1 - f.val * f.val) * f.dval[i];
		}
		return fa;
	}
};

template<int N>
struct SADvector
{
	SADfloat<N> x, y, z;
	__device__ __host__ __forceinline__ SADvector<N>()
	{
		this->x = SADfloat<N>(0);
		this->y = SADfloat<N>(0);
		this->z = SADfloat<N>(0);
	}
	__device__ __host__ __forceinline__ SADvector<N>(VECTOR v, int idx = -1, int idy = -1, int idz = -1)
	{
		this->x = SADfloat<N>(v.x, idx);
		this->y = SADfloat<N>(v.y, idy);
		this->z = SADfloat<N>(v.z, idz);
	}
	friend __device__ __host__ __forceinline__ SADvector<N> operator+ (const SADvector<N> &veca, const SADvector<N> &vecb)
	{
		SADvector<N> vec;
		vec.x = veca.x + vecb.x;
		vec.y = veca.y + vecb.y;
		vec.z = veca.z + vecb.z;
		return vec;
	}

	friend __device__ __host__ __forceinline__ SADvector<N> operator+ (const SADvector<N> &veca, const SADfloat<N> &b)
	{
		SADvector<N> vec;
		vec.x = veca.x + b;
		vec.y = veca.y + b;
		vec.z = veca.z + b;
		return vec;
	}
	friend __device__ __host__  __forceinline__ SADvector<N> operator* (const SADfloat<N> &a, const SADvector<N> &vecb)
	{
		SADvector<N> vec;
		vec.x = a*vecb.x;
		vec.y = a*vecb.y;
		vec.z = a*vecb.z;
		return vec;
	}
	friend __device__ __host__  __forceinline__ SADfloat<N> operator* (const SADvector<N> &veca, const SADvector<N> &vecb)
	{
		return veca.x*vecb.x + veca.y*vecb.y + veca.z*vecb.z;
	}
	friend __device__ __host__  __forceinline__ SADvector<N> operator- (const SADvector<N> &veca, const SADvector<N> &vecb)
	{
		SADvector<N> vec;
		vec.x = veca.x - vecb.x;
		vec.y = veca.y - vecb.y;
		vec.z = veca.z - vecb.z;
		return vec;
	}
	friend __device__ __host__ __forceinline__ SADvector<N> operator- (const SADvector<N> &veca, const SADfloat<N> &b)
	{
		SADvector<N> vec;
		vec.x = veca.x - b;
		vec.y = veca.y - b;
		vec.z = veca.z - b;
		return vec;
	}
	friend __device__ __host__  __forceinline__ SADvector<N> operator/ (const SADvector<N> &veca, const SADvector<N> &vecb)
	{
		SADvector<N> vec;
		vec.x = veca.x / vecb.x;
		vec.y = veca.y / vecb.y;
		vec.z = veca.z / vecb.z;
		return vec;
	}
	friend __device__ __host__  __forceinline__ SADvector<N> operator/ (const float &a, const SADvector<N> &vecb)
	{
		SADvector<N> vec;
		vec.x = a / vecb.x;
		vec.y = a / vecb.y;
		vec.z = a / vecb.z;
		return vec;
	}
	friend __device__ __host__  __forceinline__ SADvector<N> operator^ (const SADvector<N> &veca, const SADvector<N> &vecb)
	{
		SADvector<N> vec;
		vec.x = veca.y * vecb.z - veca.z * vecb.y;
		vec.y = veca.z * vecb.x - veca.x * vecb.z;
		vec.z = veca.x * vecb.y - veca.y * vecb.x;
		return vec;
	}
	friend __device__ __host__ __forceinline__ SADvector<N> Get_Periodic_Displacement(const SADvector<N> vec_a, const SADvector<N> vec_b, const SADvector<N> box_length)
	{
		SADvector<N> dr;
		dr = vec_a - vec_b;
		dr.x.val = dr.x.val - floorf(dr.x.val / box_length.x.val + 0.5) * box_length.x.val;
		dr.y.val = dr.y.val - floorf(dr.y.val / box_length.y.val + 0.5) * box_length.y.val;
		dr.z.val = dr.z.val - floorf(dr.z.val / box_length.z.val + 0.5) * box_length.z.val;
		for (int i = 0; i < N; i++)
		{
			dr.x.dval[i] = dr.x.val / box_length.x.val * box_length.x.dval[i] + dr.x.dval[i];
			dr.y.dval[i] = dr.y.val / box_length.y.val * box_length.y.dval[i] + dr.y.dval[i];
			dr.z.dval[i] = dr.z.val / box_length.z.val * box_length.z.dval[i] + dr.z.dval[i];
		}
		return dr;
	}
};

#endif //COMMON_CUH(common.cuh)
