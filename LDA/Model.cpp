#include "Model.h"

#include <algorithm>
#include <sstream>
#include <fstream>
#include <cstdio>
#include <cstring>
#include <string>
#include <vector>
#include <set>
#include <map>
#include <complex>
#include <utility>
#include <fstream>
#include <iostream>
#include <dirent.h>
#include <unistd.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <cmath>

using namespace std;

Model::Model(int topicNum, Corpus* corpus) {
    this -> corpus = corpus;
    D = corpus -> docNum;
    W = corpus -> wordNum;
    K = topicNum;
    gamma = new double*[D]; //�ı���topic�ֲ����� 

    for (int d = 0; d < D; d ++) {
        gamma[d] = new double[K];
    }
    LABEL_WEIGHT = 1;
    tau = 0.01;  //ԭʼlda��������������������tau��gama 
    BETA_SELF = 1;
    BETA_FIG = 1;
    outputLimit = 10000000;
}



//�������Ϊ �ĵ��š��ʱ��
//�����µ�z 
int Model::SampleTopic(int d, int w) {
	//KΪtopic��Ŀ 

    double KGamma = 0.0;
    
	for (int k = 0; k < K; k ++) { //��Ӧpaper�е�gamma 
        KGamma += gamma[d][k];
 	} 

    
	double WTau = W * tau; //��Ӧpaper�е�yita 
    
	double* p = new double[K];
	
   
    for (int k = 0; k < K; k ++) {
        p[k] = (ndz[d][k] + gamma[d][k]) / (nd_z[d] + KGamma); //��������ʽ��Gibbs�����ĸ��� 
        p[k] *= (nzw[k][w] + tau) / (nz_w[k] + WTau);
    }
    
    // cumulate multinomial parameters
    for (int k = 1; k < K; k++) { //���и����ۼ� 
	    p[k] += p[k - 1];
    } 
    
    // scaled sample because of unnormalized p[] soga����Ϊû�й�һ��������p[2*K-1]������1 
    double u = ((double) rand() / RAND_MAX) * p[K - 1];
	
	//�е������ 
    int topic = 0;
    for (topic = 0; topic < K - 1; topic++) { 
	    if (p[topic] > u) { 
	        break;
     	} 
    }
	  
    //printf("%.3lf %.3lf %d\n", p[K - 1], u, topic);
    delete[] p;
    return topic;
}

//int         Model::Train(int maxIter, int BURN_IN, int SAMPLE_LAG, int ALPHA, int GAMMA)
int Model::Train(int maxIter, int BURN_IN, int SAMPLE_LAG) { //ѧ������ԭ���������һ�� 
    printf("Start learning!\n");
    printf("Initialize the parameters! \n");
	
	//���������� 

    for (int d = 0; d < D; d ++) {
        Document* doc = corpus -> docs[d];
        for (int k = 0; k < K; k ++) {
        	gamma[d][k] = 50.0 / double(K);
        }
        

    }
    
    
    InitEstimation(); //һ�������ʼ�� 
    
	//����ѵ������ 
    int sample_cnt = 0;
    for (int iter = 0; iter < maxIter; iter ++) {
        printf("[Iteration %d]...\n", iter + 1);
        
        //�ı�ѵ������ 
		for (int d = 0; d < D; d ++) {
            Document* doc = corpus -> docs[d];
 
            for (unsigned int i = 0; i < doc -> words.size(); i ++) {
                int w = doc -> words[i];
                int old_z = Z[d][i]; //�ô�ԭ����topic 
               
                //����Ϊ���ֻ��� 
				nzw[old_z][w] --; //����topic old_z�Ĵ��д�w����Ŀ��һ 
                nz_w[old_z] --; //����old_z�Ĵʵ���Ŀ��һ 
            
            	ndz[d][old_z] --;
             	nd_z[d] --;
               
                //���˽��������²��� 
                //Gibbs���������µ�topic��c 
                
                //�������Ϊ �ĵ��š��ʱ�š���Ƶ��� 
                int z = SampleTopic(d, w);
                
				//printf("%d : %d %d\n", d, c, z);
                //���²��� 
             
                Z[d][i] = z;
                nzw[z][w] ++;
                nz_w[z] ++;
                
                ndz[d][z] ++;
                nd_z[d] ++;
           
            }
        }
        
      
    

        if (iter < BURN_IN) { //ͷ20�ֵ��������²��� 
        	continue;
        }
        if ((iter - BURN_IN) % SAMPLE_LAG != 0) { //֮��ÿ10�ֵ�������һ�β��� 
        	continue;
        }
        sample_cnt ++;
        // update parameters
        //�ı����ֲ������� 
        for (int d = 0; d < D && d<outputLimit; d ++) { //��for��Ӧsita�ĸ��� 
       
            double sum = 0.0;
            for (int k = 0; k < K; k ++) {
                pzd[k][d] = ndz[d][k] + gamma[d][k];
                sum += pzd[k][d];
            }
            for (int k = 0; k < K; k ++) {
                if (sum > 0) {
                	pzd[k][d] /= sum;
                } else {
                    pzd[k][d] = 1.0 / K;
                }
                s_pzd[k][d] += pzd[k][d];
            }
        }
   
        //��Ȼ���ı��������� 
        for (int k = 0; k < K; k ++) {//��for��Ӧfai�ĸ��� 
            double sum = 0.0;
            for (int w = 0; w < W; w ++) {
                pwz[w][k] = nzw[k][w] + tau;
                sum += pwz[w][k];
            }
            for (int w = 0; w < W; w ++) {
                if (sum > 0) {
                    pwz[w][k] /= sum;
                } else {
                    pwz[w][k] = 1.0 / W;
                }
                s_pwz[w][k] += pwz[w][k];
            }
        }

    }
    //ѵ����� 
    //pzd֮��ģ�������������ÿһ�ֵ�����ֵ
	//ѵ����Ϻ���ƽ��ֵ����s_XXX���ܺͣ���һ�¼�ƽ��ֵ 
    for (int d = 0; d < D && d<outputLimit ; d ++) {
     
        for (int z = 0; z < K; z ++) {
            pzd[z][d] = s_pzd[z][d] / (sample_cnt + 0.0);
        }
    }
    

    
    for (int z = 0; z < K; z ++) {
        for (int w = 0; w < W; w ++) {
            pwz[w][z] = s_pwz[w][z] / (sample_cnt + 0.0);
            if (pwz[w][z] > 1) { 
                printf("%.5lf %d %d\n", pwz[w][z], w, z);
            }
        }
    }
    return 0;
}

//����0��1֮������С�� 
double	Random() {
	return 1.0 * rand() / RAND_MAX;
}

int Model::InitEstimation()
{ //������ʼ��

    s_pzd = new double*[K];

    s_pwz = new double*[W];

    

    pzd = new double*[K];
    pwz = new double*[W];

    
	nzw = new int*[K];
    ndz = new int*[D];
    nd_z = new int[D];
    nzw = new int*[K];
    nz_w = new int[K];
    
	Z = new int*[D];



    for (int d = 0; d < D; d ++)
    {
        ndz[d] = new int[K];
    } 
    for (int k = 0; k < K; k ++)
    {
    
        pzd[k] = new double[D];
      
        s_pzd[k] = new double[D];
   
        for (int d = 0; d < D; d ++)
        {
            s_pzd[k][d] = 0.0;
        } 
        nzw[k] = new int[W];
    }
    for (int w = 0; w < W; w ++)
    {
        pwz[w] = new double[K];
        s_pwz[w] = new double[K];
        for (int k = 0; k < K; k ++)
        {
            s_pwz[w][k] = 0.0;
        } 
    }
    for (int d = 0; d < D; d ++)
    {
        Z[d] = new int[corpus -> docs[d] -> words.size()];
    }
    
    srand(745623); // initialize for random number generation
    for (int d = 0; d < D; d ++)
    {
        nd_z[d] = 0;
        for (int k = 0; k < K; k ++)
        {
            ndz[d][k] = 0;
        } 
    }

    

    
    for (int k = 0; k < K; k ++) {
        nz_w[k] = 0;
        for (int w = 0; w < W; w ++) { 
            nzw[k][w] = 0;
        } 
    }
    //�������ȫ���ʼ������ 
    
    //�ı���ʼ������ 
    for (int d = 0; d < D; d ++) {
    	
        Document* doc = corpus -> docs[d];
        //��ÿһ���� 
        for (unsigned int i = 0; i < doc -> words.size(); i ++) {
            int w = doc -> words[i];
            
			int k = (int) (Random() * K); //���ȡһ��topic 
            if (k == K) { 
                k --;
            } 

            Z[d][i] = k; //��ʾwdi��topic 
            
			ndz[d][k] ++;  //�ĵ�d��topic k ���ִ��� 
   			nd_z[d] ++; // �ĵ�d���������صĴʵ���Ŀ
        
            nzw[k][w] ++; //����topic k�Ĵ��д�w����Ŀ 
            nz_w[k] ++; //����topic k�Ĵʵ���Ŀ 

        }
    }
    return 0;
}


//����Ϊ�洢���ֲ����ֲ� 
int         Model::SaveTopic(const char* fileDir, int top)
{
    printf("Saving topics to %s...\n", fileDir);
    bool done[W];
    FILE* fout = fopen(fileDir, "w");
    int hit[K][top];
    memset(hit, 0, sizeof(hit));
    for (int k = 0; k < K; k ++)
    {
        fprintf(fout, "Topic #%d:\n", k);
        memset(done, false, sizeof(done));
        for (int t = 0; t < top; t ++)
        {
            double max = 0;
            int wid;
            for (int w = 0; w < W; w ++)
            {
                if (pwz[w][k] > max && (! done[w]))
                {
                    max = pwz[w][k];
                    wid = w;
                }
            }
            done[wid] = true;
            //printf("%.5lf\n", max);
            fprintf(fout, "%s %.5lf\n", corpus -> terms[wid].c_str(), max);
        }
        fprintf(fout, "\n");
    }
    fclose(fout);

    return 0;
}





int         Model::SavePzd(const char* fileDir)
{
    printf("Save topic distribution to %s.\n", fileDir);
    FILE* fout = fopen(fileDir, "w");
    for (int d = 0; d < D && d<outputLimit; d ++)
    {
        Document* doc = corpus -> docs[d];
        /*for (unsigned int i = 0; i < doc -> words.size(); i ++)
        {
            fprintf(fout, "%s ", corpus -> terms[doc -> words[i]].c_str());
        }
        fprintf(fout, "\n");*/
        fprintf(fout, "%c ", doc->type);
        fprintf(fout, "%s ", doc->dir.c_str());
		fprintf(fout, "%s ", doc->pic_id.c_str());
        for (int k = 0; k < K; k ++)
        {
            fprintf(fout, "%.5lf ", pzd[k][d]);
        }
        fprintf(fout, "\n");
    }
    fclose(fout);
    return 0;
}
