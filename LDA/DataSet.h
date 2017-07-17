#pragma once

#include "Util.h"

#include <string>
#include <vector>
#include <map>

using std::string;
using std::vector;
using std::map;

class Document 
{
public:
    int                 id;
    vector<int>         words;
	//add by hyf
    char                type;
    string              dir;
	string              pic_id; //picture id
};



class Corpus
{
public:
    int                 docNum;
    int                 wordNum;
    vector<string>      terms;
    vector<Document*>   docs; // docs[i]: doc with id = i
    
    void                Clear();
    Corpus();
};

class DataSet
{
public:
    set<string>         stopwords;
    map<string, int>    termMap;
    Corpus*             corpus;
    int                 ReadCorpus(const char* fileDir);
    int                 GetOrInsertTermId(const string& key);
    DataSet();
};
