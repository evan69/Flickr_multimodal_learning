# example of transporting python data to .mat file for matlab program
# evan69
import numpy as np
import scipy.io
import sys

def writeMat():
    fin = open(sys.argv[2],'r')
    all_data = []
    lines = fin.readlines()
    num_of_lines = 0
    demen_of_lines = len(lines[0].split(' ')) - 4
    print 'demen_of_lines',demen_of_lines
    for line in lines:
        res = line.split(' ')
        all_data.extend(res[3:3+demen_of_lines])
        # print len(res[3:3+demen_of_lines])
        num_of_lines += 1
    all_data = [float(item) for item in all_data]
    all_data = np.array(all_data).reshape(num_of_lines,demen_of_lines)
    print all_data
    scipy.io.savemat('D:/learn/grade3-3/multimodal_dictionary_learning/image_modal.mat', mdict={'image_modal': all_data})
    
def readMat():
    fin = open(sys.argv[2],'w')
    lines = fin.readlines()
    for line in readlines:
        pass
    modal_data = np.array([123123, 1.2, 2.3, 3.4])
    scipy.io.savemat('d:/out.mat', mdict={'modal_data': modal_data})
    


if __name__ == '__main__':
    if sys.argv[1] == '-w':
        writeMat()
    else:
        if sys.argv[1] == '-r':
            readMat()
        else:
            print 'wrong parameters. -w/-r'