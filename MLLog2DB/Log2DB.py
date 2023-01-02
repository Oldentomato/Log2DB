import time
import datetime
from .GetResult import Private_Save_Result

class SendLog:
    def __init__(self,collection):
        self.__db = collection
        self.__timelist = []
        self.__checkDuplicated = False
        self.__acc_arr = []
        self.__val_acc_arr = []
        self.__loss_arr = []
        self.__val_loss_arr = []

#private 함수
    def __ReshapeModel(self, model) -> list:
        shape_model = []
        for child in model.children():
            shape_model.append(str(child))
        return shape_model
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
                        hyper:dict=None
                        ) -> None:
        if hyper is None:
            __model_shape = self.__ReshapeModel(model_shape)
            self.__experiment_model_name = model_name + '_' + str(experiment_count)
            self.__hyper_data = {
                'model_name': self.__experiment_model_name,
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
            if self.__db.find_one({'model_name':self.__experiment_model_name}) is None:
                self.__db.insert_one(self.__hyper_data)
            else:
                print("Error>>>>The Model Name is Duplicated!")
                self.__checkDuplicated = True
        else:
            self.__hyper_data = hyper


        self.start_epoch_time = time.time()
        self.start_train_time = time.time()

#클래스 내부 리스트를 이용하여 업로드하도록 변경
    def on_epoch_end(self, epoch, loss=0.0, acc=0.0, val_loss=0.0, val_acc=0.0, custom=False) -> None:
        if self.__checkDuplicated is False:
            self.__acc_arr.append(acc)
            self.__val_acc_arr.append(val_acc)
            self.__loss_arr.append(loss)
            self.__val_loss_arr.append(val_loss)

            end_epoch_time = time.time()
            self.__timelist.append(str(round(end_epoch_time-self.start_epoch_time,3))+' sec')
            self.__log_data={
                'epoch' : epoch,
                'loss' : self.__loss_arr,
                'acc' : self.__acc_arr,
                'val_loss' : self.__val_loss_arr,
                'val_acc' : self.__val_acc_arr,
                'time' : self.__timelist
            }
            self.start_epoch_time = time.time()
            self.__db.update_one({'model_name': self.__hyper_data.get('model_name')}, {"$set": {"logs":self.__log_data}})
        else:
            print('Caution')


    def on_train_end(self,save_graph_url=False) -> None:
        end_train_time = time.time()
        all_train_time = end_train_time - self.start_train_time
        date_time = str(datetime.timedelta(seconds=all_train_time))
        result_time = date_time.split(".")[0]

        self.__db.update_one({'model_name': self.__hyper_data.get('model_name')}, {"$set": {"all_train_time":result_time}})

        if save_graph_url is False:
            Private_Save_Result.Show_EndTrain_Graph(self.__log_data)
        else:
            Private_Save_Result.Save_EndTrain_Graph(self.__log_data,self.__experiment_model_name)

#요기도 좀 수정이 필요 test_acc만 딱 넣기에는 사용하기가 좀 헷갈림
    def on_test_end(self, test_acc=None) -> None:
        self.__db.update_one({'model_name':self.__hyper_data.get('model_name')},{"$set":{"test_acc":test_acc}})

    def DownLoad_SingleLogs(self, model_name) -> None:
        model_info = self.__db.find_one({'model_name': model_name})
        Private_Save_Result.Save_logs_Dir(hyper_data = model_info)

    def DownLoad_MultiLogs(self, model_name) -> None:
        model_info = self.__db.find_many({'model_name': model_name})


    def DownLoad_AllLogs(self) -> None:
        model_info = self.__db.find()


