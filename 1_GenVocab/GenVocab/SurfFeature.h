#ifndef __SURF_FEATURE_H
#define __SURF_FEATURE_H

#include <opencv2/opencv.hpp>

class SurfFeature
{
public:
	SurfFeature();
	~SurfFeature();
	float** GetFeature(const cv::Mat& image);
	void FreeFeature(float **Array);
	int GetRows() const;
	int GetCols() const;
private:
	static const int cwlDiameter = 17;  //提取surf特征时的窗口参数
	static const int cwlStep = 8;   
	cv::Mat SurfMat;
	float** SurfArray;
	int rows;
	int cols;
	void GetDenseSurf(const cv::Mat& image);    //提取surf特征
	void Mat2Array();
	float **newArray();

};
#endif