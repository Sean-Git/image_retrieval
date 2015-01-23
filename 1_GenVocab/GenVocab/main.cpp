#include <iostream>
#include <vector>
#include <fstream>
#include "SurfFeature.h"
#include "CBrowseDir.h"

int main() {
	CBrowseDir dir;
	bool flag = false;
	flag = dir.SetInitDir("./data");
	std::vector<std::string> files;
	if (flag) {
		files = dir.BeginBrowseFilenames("*?");
	}
	dir.SetInitDir("..");

	// write file
	std::ofstream featfile("./surf_feats_pool.txt", ios::out);
	std::ofstream labelfile("./labels.txt", ios::out);
	int id = 0;
	char log[50];
	char value[10];
	for (size_t t = 0; t != files.size(); t++) {
		int p1 = files[t].rfind('\\');
		int p2 = files[t].rfind('_');
		int label = std::atoi(files[t].substr(p1+1, p2-p1+1).c_str());
		labelfile << label << '\n';

		cv::Mat img = cv::imread(files[t]); // read image
		SurfFeature f;
		float** feats = f.GetFeature(img);
		int r = f.GetRows();
		int c = f.GetCols();
		sprintf(log, "Img NO.%d has NO.%d feats\n", (int) t, r);
		std::cout << log;
		for (int i = 0; i < r; i++) {
			for (int j = 0; j < c; j++) {
				sprintf(value, "%.6f ", feats[i][j]);
				featfile << value;
			}
			featfile << '\n';
			id++;
		}
		f.FreeFeature(feats);
	}
	labelfile.close();
	featfile.close();
	std::cout << "totally " << id << " feat_vec written..." << std::endl;
	system("pause");
	return 0;
}