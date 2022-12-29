import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import pandas as pd
import seaborn as sn
# from sklearn.metrics import precision_score, recall_score, f1_score

__all__ = ['Draw_Graph','Draw_All_Graph','Draw_Confusion']

#일단 DB에 올리고 그 뒤에 다운받은 뒤 txt로 저장하도록 하기
def Save_logs_Dir(url, hyper_data):
    with open(url + hyper_data.get('model_name')+'.txt', 'w') as f:
        f.write('====HYPER PARAMETERS====\n')
        f.write('model_name: '+hyper_data.get('model_name')+'\n')
        f.write('datas_count: '+hyper_data.get('datas_count')+'\n')
        f.write('epoch: '+hyper_data.get('epoch')+'\n')
        f.write('batch_size: '+hyper_data.get('batch_size')+'\n')
        f.write('learning_rate: '+hyper_data.get('learning_rate')+'\n')
        f.write('criterion: '+hyper_data.get('criterion')+'\n')
        f.write('optimizer: '+hyper_data.get('optimizer')+'\n')
        f.write('model_shape: '+hyper_data.get('model_shape')+'\n')
        f.write('LR_scheduler: '+hyper_data.get('LR_scheduler')+'\n')
        f.write('etc: '+hyper_data.get('etc')+'\n')
        f.write('test_acc: '+hyper_data.get('test_acc')+'\n')


def Draw_Confusion(true_datas, predict_datas, save_url=None):
    cf = confusion_matrix(true_datas,predict_datas)
    df_cm = pd.DataFrame(cf, list(predict_datas.classes), list(true_datas.classes))
    sn.heatmap(df_cm, annot=True, annot_kws={"size":16}, cmap=plt.cm.Blues, fmt='d')
    plt.title('Confusion Matrix\n')

    if save_url is not None:
        plt.savefig(save_url)
    
    plt.show()
    plt.clf()

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
def Save_EndTrain_Graph(log_data, save_url):
    plt.plot(log_data.get('acc'))
    plt.plot(log_data.get('val_acc'))
    plt.ylabel('acc')
    plt.xlabel('epoch')
    plt.legend(['train_acc','val_acc'])
    plt.title('accuracy')
    plt.savefig(save_url+'/acc.png')
    plt.clf()

    plt.plot(log_data.get('loss'))
    plt.plot(log_data.get('val_loss'))
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train_loss','val_loss'])
    plt.title('loss')

    plt.savefig(save_url+'/loss.png')
    plt.clf()

def Draw_Graph(collection,model_name, save_url=None):
    result = collection.find_one({'model_name': model_name})
    plt.plot(result['logs']['acc'])
    plt.plot(result['logs']['val_acc'])
    plt.ylabel('acc')
    plt.xlabel('epoch')
    plt.legend(['train_acc','val_acc'])
    plt.title('accuracy')
    plt.show()
    if save_url is not None:
        plt.savefig(save_url+'/acc.png')
    plt.clf()

    plt.plot(result['logs']['loss'])
    plt.plot(result['logs']['val_loss'])
    plt.ylabel('acc')
    plt.xlabel('epoch')
    plt.legend(['train_loss','val_loss'])
    plt.title('loss')
    plt.show()
    if save_url is not None:
        plt.savefig(save_url+'/loss.png')
    plt.clf()

def Draw_All_Graph(collection,save_url=None):
    for result in collection.find():
        plt.subplot(1,2,1)
        plt.plot(result['logs']['acc'])
        plt.plot(result['logs']['val_acc'])
        plt.ylabel('acc')
        plt.xlabel('epoch')
        plt.legend(['train_acc','val_acc'])
        plt.title('accuracy')

        plt.savefig(save_url+'/acc.png')
        plt.clf()

        plt.subplot(1,2,2)
        plt.plot(result['logs']['loss'])
        plt.plot(result['logs']['val_loss'])
        plt.ylabel('acc')
        plt.xlabel('epoch')
        plt.legend(['train_loss','val_loss'])
        plt.title('loss')

        plt.savefig(save_url+'/loss.png')
        plt.clf()

