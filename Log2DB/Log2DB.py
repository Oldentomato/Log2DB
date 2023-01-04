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
                        model_shape:any=None,
                        LR_scheduler:str="",
                        etc:str="",
                        hyper:dict=None
                        ) -> None:
        """
        Training을 시작할 때 호출할 함수, 초기에 하이퍼파라미터들을 DB업로드하는 작업
        최종 model_name 은 model_name + experiment_cout 로 지정됨
        (custom으로 작성하고 싶을 경우에는 hyper매개변수에 Dictionary형식으로 작성)
            Args:
                model_name `str` : 학습할 모델의 이름
                experiment_count `int` : 실험 횟수(동일한 모델명 중복방지)
                datas_count `int` : 데이터 갯수
                epoch `int` : 에포크 수
                batch_size `int` : 배치 사이즈
                learning_rate `float` : 학습률
                criterion `str` : 손실함수 명
                optimizer `str` : 최적화 알고리즘 명
                model_shape `any` : 파이토치 기준 torch.nn.modules.container.Sequential 형식의 모델 변수
                LR_scheduler `str` : Learning_rate 스케줄러 알고리즘 명
                etc `str` : 기타 메모할 내용
                hyper `dict` : custom 로그 저장시 사용
            Returns:
                None
        """
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
                'test_acc' : 0.0,
                'precision' : 0.0,
                'recall' : 0.0,
                'f1_score' : 0.0
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
    def on_epoch_end(self, epoch:int, loss:float, acc:float, val_loss:float, val_acc:float, custom_log:dict=None) -> None:
        """
        학습의 매 에포크마다 호출하는 함수입니다. 에포크가 끝날때마다 나온 결과를 DB에 업로드합니다.
        (DB에 같은 모델명이 존재할 경우 Caution 알림이 지속적으로 뜸)
            Args:
                epoch `int` : 현재 에포크 수
                loss `float` : 현재 에포크에서 Training Loss 값
                acc `float` : 현재 에포크에서 Training Accuracy 값
                val_loss `float` : 현재 에포크에서 Validation Loss 값
                val_acc `float` : 현재 에포크에서 Validation Accuracy 값
                custom_log `dict` : Custom Log를 사용할 시 사용
            Returns:
                None
        """
        if self.__checkDuplicated is False:
            if custom_log is None:
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
            else:
                self.__log_data=custom_log

            self.start_epoch_time = time.time()
            self.__db.update_one({'model_name': self.__hyper_data.get('model_name')}, {"$set": {"logs":self.__log_data}})
        else:
            print('Caution')


    def on_train_end(self,save_graph_url:bool=False) -> None:
        """
        Training이 끝날 경우 호출하는 함수. 전체 정확도와 손실도의 그래프를 시각화 혹은 저장하는 함수이다.
            Args
                save_graph_url `bool` : 사진을 저장하려면 True로 할 것

            Return 
                None
        """
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
    def on_test_end(self, true_datas:list, predict_datas:list) -> None:
        """
        Test 단계가 끝날 경우 Test에서 나온 Precision, Recall, f1_score, Accuracy를 DB에 업로드, 
            Args
                true_datas `list` : 정답 데이터 리스트
                predict_datas `list` : 예측 데이터 리스트
            Return
                None
        """
        precision, recall, f1, acc = Private_Save_Result.Calc_scores(true_datas,predict_datas)
        self.__db.update_one({'model_name':self.__hyper_data.get('model_name')},{"$set":{"precision":precision}})
        self.__db.update_one({'model_name':self.__hyper_data.get('model_name')},{"$set":{"recall":recall}})
        self.__db.update_one({'model_name':self.__hyper_data.get('model_name')},{"$set":{"f1_score":f1}})
        self.__db.update_one({'model_name':self.__hyper_data.get('model_name')},{"$set":{"test_acc":acc}})

    def DownLoad_SingleLogs(self, model_name:str) -> None:
        """
        DB에 올라가 있는 모델의 하이퍼파라미터를 txt로 다운로드
            Args
                model_name `str` : 모델명 
            Return
                None
        """
        model_info = self.__db.find_one({'model_name': model_name})
        Private_Save_Result.Save_logs_Dir(hyper_data = model_info)

    # def DownLoad_MultiLogs(self, model_name) -> None:
    #     model_info = self.__db.find_many({'model_name': model_name})


    def DownLoad_AllLogs(self) -> None:
        """
        DB에 올라가 있는 모든모델의 하이퍼파라미터를 txt로 다운로드
            Return
                None
        """
        model_info = self.__db.find()
        for model in model_info:
            Private_Save_Result.Save_logs_Dir(hyper_data = model)


