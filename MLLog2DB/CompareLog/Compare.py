

def __Calc_Overfitting_rate(model1:dict, model2:dict):
    acc_over_list = []
    loss_over_list = []
    model1_acc_over_rate = 0.0
    model1_loss_over_rate = 0.0
    model2_acc_over_rate = 0.0
    model2_loss_over_rate = 0.0
    if len(model1.get('acc')) == len(model1.get('val_acc')):
        for i in range(0,model1.get('acc').length):
            acc_over_list.append(abs(model1.get('acc')[i] - model1.get('val_acc')[i]))
        for i in range(0,model1.get('loss').length):
            loss_over_list.append(abs(model1.get('loss')[i] - model1.get('val_loss')[i]))
    model1_acc_over_rate = sum(acc_over_list) / len(model1.get('acc'))
    model1_loss_over_rate = sum(loss_over_list) / len(model1.get('loss'))

    acc_over_list.clear()
    loss_over_list.clear()

    if len(model2.get('acc')) == len(model2.get('val_acc')):
        for i in range(0,model2.get('acc').length):
            acc_over_list.append(abs(model2.get('acc')[i] - model2.get('val_acc')[i]))
        for i in range(0,model2.get('loss').length):
            loss_over_list.append(abs(model2.get('loss')[i] - model2.get('val_loss')[i]))

    model2_acc_over_rate = sum(acc_over_list) / len(model1.get('acc'))
    model2_loss_over_rate = sum(loss_over_list) / len(model1.get('loss'))

    return model1_acc_over_rate, model1_loss_over_rate, model2_acc_over_rate, model2_loss_over_rate


def __Find_test_best_score(score1, score2):
    if score1 > score2:
        return 0, score1, abs(score1-score2)
    else:
        return 1, score2, abs(score1-score2)

def Compare_Both(model_1, model_2):
    model1_acc,model1_loss,model2_acc,model2_loss = __Calc_Overfitting_rate(model_1.get('logs'),model_2.get('logs'))
    selection,test_acc,difference_value = __Find_test_best_score(model_1.get('test_acc'),model_2.get('test_acc'))

    print('====RESULT====\n\n')
    print('>models overffiting rate\n')
    print(model_1.get('model_name')+'의 acc 오버피팅 평균: '+ model1_acc +'\n')
    print(model_1.get('model_name')+'의 loss 오버피팅 평균: '+ model1_loss +'\n')
    print(model_2.get('model_name')+'의 acc 오버피팅 평균: '+ model2_acc +'\n')
    print(model_2.get('model_name')+'의 loss 오버피팅 평균: '+ model2_loss +'\n\n')
    print('>'+model_1.get('model_name')+'의 가장 best acc: '+model_1.get('logs').get('val_acc').index(max(model_1.get('logs').get('val_acc')))+'에서 '+max(model_1.get('logs').get('val_acc'))+'\n')
    print('>'+model_2.get('model_name')+'의 가장 best acc: '+model_2.get('logs').get('val_acc').index(max(model_2.get('logs').get('val_acc')))+'에서 '+max(model_2.get('logs').get('val_acc'))+'\n\n')
    print('>best test acc\n')
    print(lambda a: model_1.get('model_name') if a==0 else model_2.get('model_name')(selection)+'의 test_acc가 '+test_acc+'으로, '+difference_value+'만큼 차이가 납니다.\n')
    print('result report 끝\n')
    


def Compare_List():
    pass