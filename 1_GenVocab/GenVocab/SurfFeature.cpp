#include <string>
#include <opencv2/nonfree/nonfree.hpp>
#include "SurfFeature.h"

SurfFeature::SurfFeature()
{
	
}

SurfFeature::~SurfFeature()
{

}

float** SurfFeature::GetFeature(const cv::Mat& image)
{
	GetDenseSurf(image);
	Mat2Array();
	return SurfArray;
}
int SurfFeature::GetRows() const
{
	return rows;
}
int SurfFeature::GetCols() const
{
	return cols;
}

void SurfFeature::GetDenseSurf(const cv::Mat& image)
{
	int imageRows = image.rows;
	int imageCols = image.cols;
	if( (imageRows < cwlDiameter) || (imageCols < cwlDiameter) )
	{
		return;
	}

	int row_begin = cwlStep;
	int row_end = imageRows - cwlStep + 1;
	int col_begin = cwlStep;
	int col_end = imageCols - cwlStep + 1;
	
	std::vector<cv::KeyPoint> denseKeyPoints;
	
	for(int r = row_begin; r <= row_end; r += cwlStep)
	{
		for(int c = col_begin; c <= col_end; c += cwlStep)
		{
			denseKeyPoints.push_back(cv::KeyPoint(c, r, cwlDiameter, 0));
		}
	}

	//int minHessian = 400;
	//cv::SurfFeatureDetector detector( minHessian );
	//detector.detect(image, denseKeyPoints);
	cv::SurfDescriptorExtractor extractor;
	extractor.compute(image,denseKeyPoints,SurfMat);
}

void SurfFeature::Mat2Array()
{
	//统计非零行
	std::vector<int> nonZeroRow;
	int countNonZero= 0;
	for(int r = 0; r < SurfMat.rows; r++)
	{
		int num_zero = cv::countNonZero(SurfMat.row(r));
		if(num_zero != 0)
		{
			countNonZero++;
			nonZeroRow.push_back(r);
		}
	}

	//决定feature的维数
	rows = countNonZero;
	cols = SurfMat.cols;

	//将矩阵转换为数组
	SurfArray = newArray();
	for(size_t i = 0; i < nonZeroRow.size(); i++)
	{
		memcpy(SurfArray[i], SurfMat.ptr<float>(nonZeroRow[i]), cols*sizeof(float));

	}
}

//给二维数组分配内存
float** SurfFeature::newArray()
{
	float **Array = new float *[rows];
	for(int r = 0; r < rows; r++)
	{
		Array[r] = new float[cols];
		memset(Array[r], 0, cols*sizeof(float));
	}
	return Array;
}

//销毁二维数组
void SurfFeature::FreeFeature(float **Array)
{
	for(int r = 0; r < rows; r++)
	{
		delete [cols]Array[r];
		Array[r] = NULL;
	}
	delete [rows]Array;
	Array = NULL;
}
