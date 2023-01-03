

def __Calc_Overfitting_rate(model1:dict):
    acc_over_list = []
    loss_over_list = []
    model1_acc_over_rate = 0.0
    model1_loss_over_rate = 0.0
    if len(model1.get('acc')) == len(model1.get('val_acc')):
        for i in range(0,len(model1.get('acc'))):
            acc_over_list.append(abs(model1.get('acc')[i] - model1.get('val_acc')[i]))
        for i in range(0,len(model1.get('loss'))):
            loss_over_list.append(abs(model1.get('loss')[i] - model1.get('val_loss')[i]))
    model1_acc_over_rate = sum(acc_over_list) / len(model1.get('acc'))
    model1_loss_over_rate = sum(loss_over_list) / len(model1.get('loss'))


    return model1_acc_over_rate, model1_loss_over_rate


def __Find_test_best_score(score1, score2):
    if score1 > score2:
        return 0, score1, abs(score1-score2)
    else:
        return 1, score2, abs(score1-score2)

def __FindModel(coll, modelname):
    return coll.find_one({'model_name':modelname})

def Compare_Both(coll, model_1_name, model_2_name):
    model_1 = __FindModel(coll, model_1_name)
    model_2 = __FindModel(coll, model_2_name)
    model1_acc,model1_loss = __Calc_Overfitting_rate(model_1.get('logs'))
    model2_acc,model2_loss = __Calc_Overfitting_rate(model_2.get('logs'))
    selection,test_acc,difference_value = __Find_test_best_score(model_1.get('test_acc'),model_2.get('test_acc'))

    if selection == 0:
        best_acc_model_name = model_1.get('model_name')
    else:
        best_acc_model_name = model_2.get('model_name')


    print('====RESULT====\n\n')
    print('>models overffiting rate\n')
    print(model_1.get('model_name')+'의 acc 오버피팅 평균: '+ str(model1_acc) +'\n')
    print(model_1.get('model_name')+'의 loss 오버피팅 평균: '+ str(model1_loss) +'\n')
    print(model_2.get('model_name')+'의 acc 오버피팅 평균: '+ str(model2_acc) +'\n')
    print(model_2.get('model_name')+'의 loss 오버피팅 평균: '+ str(model2_loss) +'\n\n')
    print('>'+model_1.get('model_name')+'의 가장 best acc: '+str(model_1.get('logs').get('val_acc').index(max(model_1.get('logs').get('val_acc'))))+'에서 '+str(max(model_1.get('logs').get('val_acc')))+'\n')
    print('>'+model_2.get('model_name')+'의 가장 best acc: '+str(model_2.get('logs').get('val_acc').index(max(model_2.get('logs').get('val_acc'))))+'에서 '+str(max(model_2.get('logs').get('val_acc')))+'\n\n')
    print('>best test acc\n')
    print(str(best_acc_model_name)+'의 test_acc가 '+str(test_acc)+'으로, '+str(difference_value)+'만큼 차이가 납니다.\n')
    print('result report 끝\n')
    


def Compare_List():
    pass