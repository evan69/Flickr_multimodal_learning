#pragma once

#include "DataSet.h"

#include <algorithm>
#include <string>
#include <vector>
#include <map>
#include <set>

using namespace std;

class   Model 
{
public:
    int             D; // #docs
    int             W; // #terms
    int             K; // #toipics
    int				outputLimit;
    
	double          LABEL_WEIGHT;
    double          BETA_SELF;
    double          BETA_FIG;

    double**        gamma;
    double          tau;
    double**        pzd;
    double**        pwz;



    double**        s_pzd;
    double**        s_pwz;

    
    double*         sum_pwz;

    int**           ndz;
    int*            nd_z;
    int**           nzw;
    int*            nz_w;


    int**           Z;


    Corpus*         corpus;
    
    Model(int topicNum, Corpus* corpus);

    int  SampleTopic(int d, int w);
    int             Train(int maxIter, int BURN_IN, int SAMPLE_LAG);
    int             InitEstimation();
	

    int             SaveTopic(const char* fileDir, int top);
    int             SavePzd(const char* fileDir);
   

};
