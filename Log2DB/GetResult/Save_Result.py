import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import pandas as pd
import seaborn as sn
import os



def __createFolder(directory):
    try:
        if not os.path.exists(directory):#파일존재여부 확인
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)

def Draw_Graph(collection:object,model_name:str, save_url:bool=False)->None:
    """
    모델명을 이용하여 모델 조회 후 정확도와 손실도 그래프 출력 및 저장
        Args
            collection `object` : 설정된 db collection
            model_name `str` : 모델명
            save_url `bool` : 저장여부
        Return
            None
    """
    result_url = 'result/'
    __createFolder(result_url)
    result = collection.find_one({'model_name': model_name})
    plt.plot(result['logs']['acc'])
    plt.plot(result['logs']['val_acc'])
    plt.ylabel('acc')
    plt.xlabel('epoch')
    plt.legend(['train_acc','val_acc'])
    plt.title('accuracy')
    plt.show()
    if save_url is True:
        plt.savefig(result_url+model_name+'/acc.png')
    plt.clf()

    plt.plot(result['logs']['loss'])
    plt.plot(result['logs']['val_loss'])
    plt.ylabel('acc')
    plt.xlabel('epoch')
    plt.legend(['train_loss','val_loss'])
    plt.title('loss')
    plt.show()
    if save_url is True:
        plt.savefig(save_url+'/loss.png')
    plt.clf()

def Draw_All_Graph(collection:object)->None:
    """
    전체 모델 조회 후 정확도와 손실도 그래프 저장
    Args
        collection `object` : 설정된 db collection
    Return
        None
    """
    result_url = 'result/'
    __createFolder(result_url)
    for result in collection.find():
        plt.subplot(1,2,1)
        plt.plot(result['logs']['acc'])
        plt.plot(result['logs']['val_acc'])
        plt.ylabel('acc')
        plt.xlabel('epoch')
        plt.legend(['train_acc','val_acc'])
        plt.title('accuracy')

        plt.savefig(result_url+result['model_name']+'/acc.png')
        plt.clf()

        plt.subplot(1,2,2)
        plt.plot(result['logs']['loss'])
        plt.plot(result['logs']['val_loss'])
        plt.ylabel('acc')
        plt.xlabel('epoch')
        plt.legend(['train_loss','val_loss'])
        plt.title('loss')

        plt.savefig(result_url+result['model_name']+'/loss.png')
        plt.clf()



def Draw_Confusion(true_datas:list, predict_datas:list,model_name:str, save_url:bool=False)->None:
    """
    실제값 리스트와 예측값 리스트를 이용하여 모델 조회 후 혼돈행렬 출력 및 저장
        Args
            true_datas `list` : 실제 값 리스트
            predict_datas `list` : 모델이 예측한 값 리스트
            model_name `str` : 모델명
            save_url `bool` : 저장여부
        Return
            None
    """
    result_url = 'result/'
    __createFolder(result_url)
    cf = confusion_matrix(true_datas,predict_datas)
    df_cm = pd.DataFrame(cf, predict_datas, true_datas)
    sn.heatmap(df_cm, annot=True, annot_kws={"size":16}, cmap=plt.cm.Blues, fmt='d')
    plt.title('Confusion Matrix\n')

    if save_url is True:
        plt.savefig(result_url+model_name+'/confusion_matrix.png')
    
    plt.show()
    plt.clf()

