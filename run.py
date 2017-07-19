import os,shutil
cur = os.getcwd()
# os.system('python merge.py -a') # merge all into text_modal_data.txt
# os.system('python merge.py image_modal.txt') # compare text_modal_data.txt and image_modal.txt and output to text_modal_data_part_2.txt
os.chdir(os.getcwd() + '/LDA/')
os.system('make')
os.system('main.exe 50 10 ../text_modal_data_part_2.txt')
os.system('make clean')
shutil.move(os.getcwd() + '/text_modal.txt',cur + '/text_modal.txt')
os.chdir(cur)
os.system('python matGenerator.py -w ../image_crawler/text_modal.txt') # translate text_modal.txt to .mat file
os.system('python matGenerator.py -w ../image_crawler/image_modal.txt') # translate image_modal.txt to .mat file
# os.system('make')
