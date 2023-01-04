import matplotlib.pyplot as plt
import os
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score

def __createFolder(directory):
    try:
        if not os.path.exists(directory):#파일존재여부 확인
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)

    
#일단 DB에 올리고 그 뒤에 다운받은 뒤 txt로 저장하도록 하기
def Save_logs_Dir(hyper_data):
    result_url = 'result/'
    __createFolder(result_url)
    with open(result_url + hyper_data.get('model_name')+'.txt', 'w') as f:
        f.write('====HYPER PARAMETERS====\n')
        f.write('model_name: '+hyper_data.get('model_name')+'\n')
        f.write('datas_count: '+ str(hyper_data.get('datas_count'))+'\n')
        f.write('epoch: '+ str(hyper_data.get('epoch'))+'\n')
        f.write('batch_size: '+ str(hyper_data.get('batch_size'))+'\n')
        f.write('learning_rate: '+ str(hyper_data.get('learning_rate'))+'\n')
        f.write('criterion: '+hyper_data.get('criterion')+'\n')
        f.write('optimizer: '+hyper_data.get('optimizer')+'\n')
        f.write('model_shape: '+'\n'.join((hyper_data.get('model_shape')))+'\n')
        f.write('LR_scheduler: '+hyper_data.get('LR_scheduler')+'\n')
        f.write('etc: '+hyper_data.get('etc')+'\n')
        f.write('test_acc: '+str(hyper_data.get('test_acc'))+'\n')
        f.write('precision: '+str(hyper_data.get('precision'))+'\n')
        f.write('recall: '+str(hyper_data.get('recall'))+'\n')
        f.write('f1_score: '+str(hyper_data.get('f1_score'))+'\n')
        
#private
def Show_EndTrain_Graph(log_data):
    plt.plot(log_data.get('acc'))
    plt.plot(log_data.get('val_acc'))
    plt.ylabel('acc')
    plt.xlabel('epoch')
    plt.legend(['train_acc','val_acc'])
    plt.title('accuracy')
    plt.show()
    plt.clf()

    plt.plot(log_data.get('acc'))
    plt.plot(log_data.get('val_acc'))
    plt.ylabel('acc')
    plt.xlabel('epoch')
    plt.legend(['train_acc','val_acc'])
    plt.title('loss')

    plt.show()
    plt.clf()




#private
def Save_EndTrain_Graph(log_data,model_name):
    result_url = 'result/'
    __createFolder(result_url+model_name)
    plt.plot(log_data.get('acc'))
    plt.plot(log_data.get('val_acc'))
    plt.ylabel('acc')
    plt.xlabel('epoch')
    plt.legend(['train_acc','val_acc'])
    plt.title('accuracy')
    plt.savefig(result_url+model_name+'/acc.png')
    plt.clf()

    plt.plot(log_data.get('loss'))
    plt.plot(log_data.get('val_loss'))
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train_loss','val_loss'])
    plt.title('loss')

    plt.savefig(result_url+model_name+'/loss.png')
    plt.clf()


def Calc_scores(true_datas:list, predict_datas:list)->tuple:
    return precision_score(true_datas,predict_datas), recall_score(true_datas,predict_datas), f1_score(true_datas,predict_datas), accuracy_score(true_datas,predict_datas)
