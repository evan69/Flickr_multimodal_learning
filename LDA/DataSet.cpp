#include "Util.h"
#include "DataSet.h"

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

using std::string;
using std::vector;
using std::map;



// Corpus
Corpus::Corpus()
{
    terms.clear();
    docs.clear();
}





void        Corpus::Clear()
{
    wordNum = 0;
    docNum = 0;
    terms.clear();
    docs.clear();
}

// DataSet
DataSet::DataSet()
{
    corpus = new Corpus();
    termMap.clear();
}

int				DataSet::GetOrInsertTermId(const string& key)
{
    map<string, int>::iterator it = termMap.find(key);
    if (it != termMap.end()) { 
        return it -> second;
    } 
    int id = (int) corpus -> terms.size();
    corpus -> terms.push_back(key);
    termMap.insert(make_pair(key, id));
	return id;
}

int	DataSet::ReadCorpus(const char* fileDir)
{
    printf("Read Corpus now!\n");
    vector<string> inputs = Util::ReadFromFile(fileDir);
    unsigned int i = 0;
    while (i < inputs.size()) {

        //按空格把每行数据切分开 
        if(inputs[i].length() < 3)
        {
            i++;
            continue;
        }
        vector<string> tokens = Util::StringTokenize(inputs[i]);
        //printf("readin: %s \n",tokens[2].c_str());
        if(tokens.size() < 4)
        {
            printf("tokens size < 4 %s \n",tokens[2].c_str());
            i++;
            continue;
        }
 
        // 读取文本内容 
        Document* doc = new Document();
        doc -> id = corpus -> docs.size();
		doc -> type = tokens[0][0];
        doc -> dir = tokens[1];
        doc -> pic_id = tokens[2];
		
        for (int j = 3; j<tokens.size(); j ++) {
            
            //string word = ReplaceAll(tokens[j].c_str());
            string word = tokens[j]; //学长貌似用的是英文语料，中文的话这里不作替换了
										//输入语料前，先用别的程序做剔除标点，剔除停用词，英文大小写转换 
            int tid = GetOrInsertTermId(word);
            doc -> words.push_back(tid);
        }
//        if (doc -> words.size() > 0) {
        corpus -> docs.push_back(doc);
//        }
        i ++;
    } // end while
    


    corpus -> docNum = (int) corpus -> docs.size();
    corpus -> wordNum = (int) termMap.size();
    printf("#documents: %d\n", corpus -> docNum);
    printf("#terms: %d\n", corpus -> wordNum);
    return 0;
}
