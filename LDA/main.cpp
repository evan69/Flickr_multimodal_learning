#include "Model.h"
#include "DataSet.h"
#include "Util.h"
#include <iostream>
#include <cstdlib>
#include <string>
#include <fstream>
#include <sstream>

using std::string;

int   main(int argc, char* argv[])
{
    string INPUT_FILE = "/Users/zsp/Desktop/2017MM/04_text_content.txt";
    string STOPWORD_FILE = "";
    string TOPIC_FILE = "output/topics.txt";
    string PZD_FILE = "/Users/zsp/Desktop/2017MM/04_text_feature.txt";
    
    
    //string INSTANCE_FILE = "output/emotion_instance.txt";
    if(argc < 4)
    {
        printf("Usage: main [topic num] [max iter] [input file]\n");
        return 0;
    }
    int TOPIC_NUM = atoi(argv[1]);
    int MAX_ITER = atoi(argv[2]);
    int BURN_IN = (int) (MAX_ITER / 5);
    int SAMPLE_LAG = (int) 10;
    
    
//    ifstream vecFin("/Users/zsp/Desktop/2017MM/04_textname.txt");
//    
//    string line = "";
//    int count = 0;
//    vector<int> docnum;
//    while (getline(vecFin, line))
//    {
//        count += 1;
//        if (count > 3)
//            break;
//        INPUT_FILE = "/Users/zsp/Desktop/2017MM/data/seg_data/seg_04_text/" + line;
//        PZD_FILE = "/Users/zsp/Desktop/2017MM/data/seg_data/feature_04_text/" + line;
//        TOPIC_FILE = "/Users/zsp/Desktop/2017MM/seg_data/topic_04_text/" + line;
//
//        cout << PZD_FILE << " <<<<<<<<<<< " << count << endl;
//        // 读入文件
//        
//        
//        
//        vector<string> inputs = Util::ReadFromFile(INPUT_FILE);
//        unsigned int i = 0;
//    
//        while (i < inputs.size()) {
//            
//            //∞¥ø’∏Ò∞—√ø–– ˝æ›«–∑÷ø™
//            vector<string> tokens = Util::StringTokenize(inputs[i]);
//        }
//        File* fpin = fopen(fileDir, "w")
//        FILE* fout = fopen(fileDir, "w");
//        for (int d = 0; d < D && d<outputLimit; d ++)
//        {
//            Document* doc = corpus -> docs[d];
//            /*for (unsigned int i = 0; i < doc -> words.size(); i ++)
//             {
//             fprintf(fout, "%s ", corpus -> terms[doc -> words[i]].c_str());
//             }
//             fprintf(fout, "\n");*/
//            for (int k = 0; k < K; k ++)
//            {
//                fprintf(fout, "%.5lf ", pzd[k][d]);
//            }
//            fprintf(fout, "\n");
//        }
//        fclose(fout);
//        
//        
//    }
    
    
    
    
    //        dataForm(infile, outfile);
    DataSet* dataSet = new DataSet();
    //∂¡»Î”Ô¡œ
    //dataSet -> ReadCorpus(INPUT_FILE.c_str());
    //INPUT_FILE = "text_modal_data_part_2.txt";
    INPUT_FILE = argv[3];
    dataSet -> ReadCorpus(INPUT_FILE.c_str());
    //return 0;
    //≥ı ºªØƒ£–Õ
    Model* model = new Model(TOPIC_NUM,dataSet -> corpus);
    model -> K = TOPIC_NUM;
    model -> Train(MAX_ITER, BURN_IN, SAMPLE_LAG);
    PZD_FILE = "text_modal.txt";
    //¥¢¥Êƒ£–Õ
    TOPIC_FILE = "topic.txt";
    model -> SaveTopic(TOPIC_FILE.c_str(), 50);
    model -> SavePzd(PZD_FILE.c_str());
    
//    vecFin.clear();
//    vecFin.close();
    

}
