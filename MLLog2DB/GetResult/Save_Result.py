import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import pandas as pd
import seaborn as sn

# from sklearn.metrics import precision_score, recall_score, f1_score


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



def Draw_Confusion(true_datas, predict_datas, save_url=None):
    cf = confusion_matrix(true_datas,predict_datas)
    df_cm = pd.DataFrame(cf, list(predict_datas.classes), list(true_datas.classes))
    sn.heatmap(df_cm, annot=True, annot_kws={"size":16}, cmap=plt.cm.Blues, fmt='d')
    plt.title('Confusion Matrix\n')

    if save_url is not None:
        plt.savefig(save_url)
    
    plt.show()
    plt.clf()




