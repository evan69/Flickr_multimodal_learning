# example of transporting python data to .mat file for matlab program
# evan69
import numpy as np
import scipy.io
import sys,os

def writeMat():
    fin = open(sys.argv[2],'r')
    all_data = []
    lines = fin.readlines()
    num_of_lines = 0
    demen_of_lines = len(lines[0].split(' ')) - 3
    print 'demen_of_lines',demen_of_lines
    for line in lines:
        res = line.split(' ')
        all_data.extend(res[3:3+demen_of_lines])
        # print len(res[3:3+demen_of_lines])
        num_of_lines += 1
    all_data = [float(item) for item in all_data]
    all_data = np.array(all_data).reshape(num_of_lines,demen_of_lines)
    print all_data
    name = sys.argv[2].split('/')[-1].split('.')[0]
    print name
    scipy.io.savemat(os.getcwd() + '/multimodal_dictionary_learning/' + name + '.mat', mdict={name: all_data})
    
def readMat():
    if sys.argv[2] == 'train' or sys.argv[2] == 'test':
        type = sys.argv[2]
    else:
        print 'error in parameters: if should be "-r test/train"'
        return
    data = scipy.io.loadmat(os.getcwd() + '/multimodal_dictionary_learning/DL_result_' + type + '.mat')
    print data['Atr']
    demen = len(data['Atr'][0])
    fin = open('image_modal_train.txt','r')
    fout1 = open('DL_image_result_' + type + '.txt','w')
    fout2 = open('DL_text_result_' + type + '.txt','w')
    lines = fin.readlines()
    for i in range(len(lines)):
        line = lines[i]
        line = line.split(' ')
        out = line[0] + ' ' + line[1] + ' ' + line[2]
        fout1.write(out)
        fout2.write(out)
        for j in range(demen / 2):
            fout1.write(' ')
            fout1.write(str(data['Atr'][i][j]))
            fout2.write(' ')
            fout2.write(str(data['Atr'][i][j + demen / 2]))
        fout1.write('\n')
        fout2.write('\n')
        # fout1.write(out)
        # for item in data[]


if __name__ == '__main__':
    if sys.argv[1] == '-w':
        writeMat()
    else:
        if sys.argv[1] == '-r':
            readMat()
        else:
            print 'wrong parameters. -w/-r'