import time
import datetime
from .GetResult import Save_Result

class SendLog:
    def __init__(self,collection):
        self.__db = collection

#private 함수
    def __ReshapeModel(self, model) -> list:
        shape_model = []
        for child in model.children():
            shape_model.append(str(child))
        return shape_model
    # hyper = dict 에서 인자 하나하나로 바꾸기->끝
    def on_train_start(self,
                        model_name:str="",
                        experiment_count:int=0,
                        datas_count:int=0,
                        epoch:int=0,
                        batch_size:int=0,
                        learning_rate:float=0.0,
                        criterion:str="",
                        optimizer:str="",
                        model_shape:object=None,
                        LR_scheduler:str="",
                        etc:str="",
                        hyper:dict=None,
                        custom=False) -> None:
        if custom == False:
            __model_shape = self.__ReshapeModel(model_shape)
            __experiment_model_name = model_name + '_' + str(experiment_count)
            self.__hyper_data = {
                'model_name': __experiment_model_name,
                'datas_count' : datas_count,
                'epoch' : epoch,
                'batch_size' : batch_size,
                'learning_rate' : learning_rate,
                'criterion' : criterion,
                'optimizer' : optimizer,
                'model_shape' : __model_shape,
                'LR_scheduler' : LR_scheduler,
                'etc' : etc,
                'test_acc' : 0.0
            }
            #모델명 중복여부 체크
            if self.__db.find_one({'model_name':__experiment_model_name}) is not None:
                self.__db.insert_one(self.__hyper_data)
            else:
                print("Error>>>>The Model Name is Duplicated!")
        else:
            self.__hyper_data = hyper


        self.start_epoch_time = time.time()
        self.start_train_time = time.time()

#set으로 말고 push형식으로 바꾸기
    def on_epoch_end(self, epoch, logs=None, custom=False) -> None:
        end_epoch_time = time.time()
        self.__log_data={
            'epoch' : epoch,
            'loss' : logs.get('loss'),
            'acc' : logs.get('accuracy'),
            'val_loss' : logs.get('val_loss'),
            'val_acc' : logs.get('val_accuracy'),
            'time' : str(round(end_epoch_time-self.start_epoch_time,3))+' sec'
        }
        self.start_epoch_time = time.time()
        self.__db.update_one({'model_name': self.__hyper_data.get('model_name')}, {"$set": {"logs":self.__log_data}})

#url은 그냥 고정으로 해놓기 url 에서 / 여부가 오류만들기 쉬움->끝
    def on_train_end(self,save_graph_url=False) -> None:
        end_train_time = time.time()
        all_train_time = end_train_time - self.start_train_time
        date_time = str(datetime.timedelta(seconds=all_train_time))
        result_time = date_time.split(".")[0]

        self.__db.update_one({'model_name': self.__hyper_data.get('model_name')}, {"$set": {"all_train_time":result_time}})

        if save_graph_url is False:
            Save_Result.Show_EndTrain_Graph(self.__log_data)
        else:
            Save_Result.Save_EndTrain_Graph(self.__log_data)

#요기도 좀 수정이 필요 test_acc만 딱 넣기에는 사용하기가 좀 헷갈림
    def on_test_end(self, test_acc=None) -> None:
        self.__db.update_one({'model_name':self.__hyper_data.get('model_name')},{"$set":{"test_acc":test_acc}})

    def DownLoad_SingleLogs(self, model_name) -> None:
        model_info = self.__db.find_one({'model_name': model_name})
        Save_Result.Save_logs_Dir(url = '',hyper_data = model_info)

    def DownLoad_MultiLogs(self, model_name) -> None:
        model_info = self.__db.find_many({'model_name': model_name})


    def DownLoad_AllLogs(self) -> None:
        model_info = self.__db.find()


