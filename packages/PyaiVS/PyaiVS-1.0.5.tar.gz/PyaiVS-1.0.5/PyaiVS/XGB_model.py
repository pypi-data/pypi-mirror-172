import time
from xgboost import XGBClassifier,XGBRegressor
import warnings
from PyaiVS.splitdater import split_dataset
from PyaiVS.feature_create import create_des
from PyaiVS.data_utils import TVT,statistical
from hyperopt import fmin, tpe, hp, STATUS_OK, Trials
from sklearn.metrics import roc_auc_score, confusion_matrix, precision_recall_curve, auc, mean_squared_error, \
    r2_score, mean_absolute_error
import pandas as pd
import numpy as np

def all_one_zeros(data):
    if (len(np.unique(data)) == 2):
        flag = False
    else:
        flag = True
    return flag


import joblib
start = time.time()
warnings.filterwarnings("ignore")


def best_model_runing(seed,best_hyper,data,split_type='random',FP_type='ECFP4',task_type='cla',model_dir=False):
    pd_res = []
    patience = 30
    min_child_weight_ls = range(1, 6)
    max_depth_ls = range(3, 10)
    n_estimators_ls = [100, 200, 300, 400, 500, 1000, 1500, 2000]
    if task_type =='cla':
        while True:

            # data_tr_x, data_va_x, data_te_x, data_tr_y, data_va_y, data_te_y = split_dataset(X, Y,
            #                                                                                      split_type=split_type,
            #                                                                                      valid_need=True,
            #                                                                                      random_state=seed)
            data_x, data_te_x, data_y, data_te_y = data.set2ten(seed)

            data_tr_x, data_va_x, data_tr_y, data_va_y = split_dataset(data_x, data_y, split_type=split_type, valid_need=False,
                                                                       random_state=seed, train_size=(8 / 9))

            data_tr_x, data_tr_y = create_des(data_tr_x, data_tr_y, FP_type=FP_type,model_dir=model_dir)
            data_va_x, data_va_y = create_des(data_va_x, data_va_y, FP_type=FP_type,model_dir=model_dir)
            data_te_x, data_te_y = create_des(data_te_x, data_te_y, FP_type=FP_type,model_dir=model_dir)
            if (all_one_zeros(data_tr_y) or all_one_zeros(data_va_y) or all_one_zeros(data_te_y)):
                # print(
                #     '\ninvalid random seed {} due to one class presented in the {} splitted sets...'.format(seed,
                #                                                                                             split_type))
                # print('Changing to another random seed...\n')
                seed = np.random.randint(50, 999999)
            else:

                break
    else:
        data_x, data_te_x, data_y, data_te_y = data.set2ten(seed)

        data_tr_x, data_va_x, data_tr_y, data_va_y = split_dataset(data_x, data_y, split_type=split_type,
                                                                   valid_need=False,
                                                                   random_state=seed, train_size=(8 / 9))
        data_tr_x, data_tr_y = create_des(data_tr_x, data_tr_y, FP_type=FP_type)
        data_va_x, data_va_y = create_des(data_va_x, data_va_y, FP_type=FP_type)
        data_te_x, data_te_y = create_des(data_te_x, data_te_y, FP_type=FP_type)



    model = XGBClassifier(n_estimators=n_estimators_ls[best_hyper['n_estimators']],
                          max_depth=max_depth_ls[best_hyper['max_depth']],
                          min_child_weight=min_child_weight_ls[best_hyper['min_child_weight']],
                          learning_rate=best_hyper['learning_rate'],
                          gamma=best_hyper['gamma'],
                          subsample=best_hyper['subsample'],
                          colsample_bytree=best_hyper['colsample_bytree'],
                          n_jobs=6, random_state=1, seed=1) \
        if task_type == 'cla' else XGBRegressor(
        n_estimators=n_estimators_ls[best_hyper['n_estimators']],
        max_depth=max_depth_ls[best_hyper['max_depth']],
        min_child_weight=min_child_weight_ls[best_hyper['min_child_weight']],
        learning_rate=best_hyper['learning_rate'],
        gamma=best_hyper['gamma'],
        subsample=best_hyper['subsample'],
        colsample_bytree=best_hyper['colsample_bytree'],
        n_jobs=6, random_state=1, seed=1)

    model.fit(data_tr_x, data_tr_y, eval_metric='auc' if task_type == 'cla' else 'rmse',
              eval_set=[(data_va_x, data_va_y)],
              early_stopping_rounds=patience, verbose=False)
    num_of_compounds = data_x.shape[0]+data_te_x.shape[0]
    if task_type == 'cla':
        # training set
        tr_pred = model.predict_proba(data_tr_x, ntree_limit=model.best_ntree_limit)
        tr_results = [seed, FP_type, split_type, 'tr', num_of_compounds]
        tr_results.extend(statistical(data_tr_y, np.argmax(tr_pred, axis=1), tr_pred[:, 1]))
        pd_res.append(tr_results)
        # validation set
        va_pred = model.predict_proba(data_va_x, ntree_limit=model.best_ntree_limit)
        va_results = [seed, FP_type, split_type, 'va', num_of_compounds]
        va_results.extend(statistical(data_va_y, np.argmax(va_pred, axis=1), va_pred[:, 1]))
        pd_res.append(va_results)
        # test set
        te_pred = model.predict_proba(data_te_x, ntree_limit=model.best_ntree_limit)
        te_results = [seed, FP_type, split_type, 'te', num_of_compounds]
        te_results.extend(statistical(data_te_y, np.argmax(te_pred, axis=1), te_pred[:, 1]))
        pd_res.append(te_results)
    else:
        # training set
        tr_pred = model.predict(data_tr_x, ntree_limit=model.best_ntree_limit)
        tr_results = [seed, FP_type, split_type, 'tr', num_of_compounds,
                      np.sqrt(mean_squared_error(data_tr_y, tr_pred)), r2_score(data_tr_y, tr_pred),
                      mean_absolute_error(data_tr_y, tr_pred)]
        pd_res.append(tr_results)
        # validation set
        va_pred = model.predict(data_va_x, ntree_limit=model.best_ntree_limit)
        va_results = [seed, FP_type, split_type, 'va', num_of_compounds,
                      np.sqrt(mean_squared_error(data_va_y, va_pred)), r2_score(data_va_y, va_pred),
                      mean_absolute_error(data_va_y, va_pred)]
        pd_res.append(va_results)
        # test set
        te_pred = model.predict(data_te_x, ntree_limit=model.best_ntree_limit)
        te_results = [seed, FP_type, split_type, 'te', num_of_compounds,
                      np.sqrt(mean_squared_error(data_te_y, te_pred)), r2_score(data_te_y, te_pred),
                      mean_absolute_error(data_te_y, te_pred)]
        pd_res.append(te_results)
    return pd_res
def tvt_xgb(X,Y,split_type='random',FP_type='ECFP4',task_type='cla',model_dir=False):
    random_state = 42
    while True:

        # data_tr_x, data_va_x, data_te_x, data_tr_y, data_va_y, data_te_y = split_dataset(X, Y,
        #                                                                                  split_type=split_type,
        #                                                                                  valid_need=True,
        #                                                                                  random_state=random_state)
        data = TVT(X, Y)
        data_x, data_te_x, data_y, data_te_y = data.set2ten(0)
        
        data_tr_x, data_va_x, data_tr_y, data_va_y = split_dataset(data_x, data_y, split_type=split_type, valid_need=False,
                                                                   random_state=random_state, train_size=(8 / 9))
        data_tr_x, data_tr_y = create_des(data_tr_x, data_tr_y, FP_type=FP_type, model_dir=model_dir)
        data_va_x, data_va_y = create_des(data_va_x, data_va_y, FP_type=FP_type, model_dir=model_dir)
        data_te_x, data_te_y = create_des(data_te_x, data_te_y, FP_type=FP_type, model_dir=model_dir)

        if (all_one_zeros(data_tr_y) or all_one_zeros(data_va_y) or all_one_zeros(data_te_y)):
            # print(
            #     '\ninvalid random seed {} due to one class presented in the {} splitted sets...'.format('None',
            #                                                                                             split_type))
            # print('Changing to another random seed...\n')
            random_state = np.random.randint(50, 999999)
        else:

            break


    pd_res = []
    OPT_ITERS = 50
    patience = 30

    space_ = {'learning_rate': hp.uniform('learning_rate', 0.01, 0.2),
              'gamma': hp.uniform('gamma', 0, 0.2),
              'min_child_weight': hp.choice('min_child_weight', range(1, 6)),
              'subsample': hp.uniform('subsample', 0.7, 1.0),
              'colsample_bytree': hp.uniform('colsample_bytree', 0.7, 1.0),
              'max_depth': hp.choice('max_depth', range(3, 10)),
              'n_estimators': hp.choice('n_estimators', [50, 100, 200, 300, 400, 500, 1000])}
    min_child_weight_ls = range(1, 6)
    max_depth_ls = range(3, 10)
    n_estimators_ls = [100, 200, 300, 400, 500, 1000, 1500, 2000]
    trials = Trials()
    def hyper_opt(args):
        model = XGBClassifier(**args, n_jobs=6, random_state=1, seed=1) if task_type == 'cla' else XGBRegressor(**args, n_jobs=6,
                                                                                                   random_state=1,
                                                                                                   seed=1)

        model.fit(data_tr_x, data_tr_y, eval_metric='auc' if task_type == 'cla' else 'rmse',
                  eval_set=[(data_va_x, data_va_y)],
                  early_stopping_rounds=patience, verbose=False)
        val_preds = model.predict_proba(data_va_x, ntree_limit=model.best_ntree_limit) if task_type == 'cla' else \
            model.predict(data_va_x, ntree_limit=model.best_ntree_limit)
        loss = 1 - roc_auc_score(data_va_y, val_preds[:, 1]) if task_type == 'cla' else np.sqrt(
            mean_squared_error(data_va_y, val_preds))
        return {'loss': loss, 'status': STATUS_OK}


    # start hyper-parameters optimization
    best_results = fmin(hyper_opt, space_, algo=tpe.suggest, max_evals=OPT_ITERS, trials=trials, show_progressbar=False)

    best_model = XGBClassifier(n_estimators=n_estimators_ls[best_results['n_estimators']],
                               max_depth=max_depth_ls[best_results['max_depth']],
                               min_child_weight=min_child_weight_ls[best_results['min_child_weight']],
                               learning_rate=best_results['learning_rate'],
                               gamma=best_results['gamma'],
                               subsample=best_results['subsample'],
                               colsample_bytree=best_results['colsample_bytree'],
                               n_jobs=6, random_state=1, seed=1) \
        if task_type == 'cla' else XGBRegressor(
        n_estimators=n_estimators_ls[best_results['n_estimators']],
        max_depth=max_depth_ls[best_results['max_depth']],
        min_child_weight=min_child_weight_ls[best_results['min_child_weight']],
        learning_rate=best_results['learning_rate'],
        gamma=best_results['gamma'],
        subsample=best_results['subsample'],
        colsample_bytree=best_results['colsample_bytree'],
        n_jobs=6, random_state=1, seed=1)

    best_model.fit(data_tr_x, data_tr_y)
    if model_dir :
        model_name = str(model_dir) +'/%s_%s_%s_%s'%(split_type,task_type,FP_type,'XGB_bestModel.pkl')
        joblib.dump(best_model,model_name)
    num_of_compounds = len(X)
    if task_type == 'cla':
        # training set
        tr_pred = best_model.predict_proba(data_tr_x)

        tr_results = [FP_type, split_type, 'tr', num_of_compounds,
                      n_estimators_ls[best_results['n_estimators']],
                      max_depth_ls[best_results['max_depth']],
                      min_child_weight_ls[best_results['min_child_weight']],
                      best_results['learning_rate'], best_results['gamma'], best_results['subsample'],
                      best_results['colsample_bytree']]
        tr_results.extend(statistical(data_tr_y, np.argmax(tr_pred, axis=1), tr_pred[:, 1]))
        pd_res.append(tr_results)
        # validation set
        va_pred = best_model.predict_proba(data_va_x)
        va_results = [FP_type, split_type, 'va', num_of_compounds,
                      n_estimators_ls[best_results['n_estimators']],
                      max_depth_ls[best_results['max_depth']],
                      min_child_weight_ls[best_results['min_child_weight']],
                      best_results['learning_rate'], best_results['gamma'], best_results['subsample'],
                      best_results['colsample_bytree']]
        va_results.extend(statistical(data_va_y, np.argmax(va_pred, axis=1), va_pred[:, 1]))
        pd_res.append(va_results)
        # test set
        te_pred = best_model.predict_proba(data_te_x)
        te_results = [FP_type, split_type, 'te', num_of_compounds,
                      n_estimators_ls[best_results['n_estimators']],
                      max_depth_ls[best_results['max_depth']],
                      min_child_weight_ls[best_results['min_child_weight']],
                      best_results['learning_rate'], best_results['gamma'], best_results['subsample'],
                      best_results['colsample_bytree']]
        te_results.extend(statistical(data_te_y, np.argmax(te_pred, axis=1), te_pred[:, 1]))
        pd_res.append(te_results)
        para_res = pd.DataFrame(pd_res, columns=['FP_type', 'split_type', 'type', 'num_of_compounds',
                                                 'n_estimators', 'max_depth','min_child_weight','learning_rate',
                                                 'gamma','subsample','colsample_bytree',
                                                 'precision', 'se', 'sp',
                                                 'acc', 'mcc', 'auc_prc', 'auc_roc'])
    else:
        # training set
        tr_pred = best_model.predict(data_tr_x, ntree_limit=best_model.best_ntree_limit)
        tr_results = [FP_type, split_type, 'tr', num_of_compounds,
                      n_estimators_ls[best_results['n_estimators']],
                      max_depth_ls[best_results['max_depth']],
                      min_child_weight_ls[best_results['min_child_weight']],
                      best_results['learning_rate'], best_results['gamma'], best_results['subsample'],
                      best_results['colsample_bytree'],
                      np.sqrt(mean_squared_error(data_tr_y, tr_pred)), r2_score(data_tr_y, tr_pred),
                      mean_absolute_error(data_tr_y, tr_pred)]
        pd_res.append(tr_results)
        # validation set
        va_pred = best_model.predict(data_va_x, ntree_limit=best_model.best_ntree_limit)
        va_results = [FP_type, split_type, 'va', num_of_compounds,
                      n_estimators_ls[best_results['n_estimators']],
                      max_depth_ls[best_results['max_depth']],
                      min_child_weight_ls[best_results['min_child_weight']],
                      best_results['learning_rate'], best_results['gamma'], best_results['subsample'],
                      best_results['colsample_bytree'],
                      np.sqrt(mean_squared_error(data_va_y, va_pred)), r2_score(data_va_y, va_pred),
                      mean_absolute_error(data_va_y, va_pred)]
        pd_res.append(va_results)
        # test set
        te_pred = best_model.predict(data_te_x, ntree_limit=best_model.best_ntree_limit)
        te_results = [FP_type, split_type, 'te', num_of_compounds,
                      n_estimators_ls[best_results['n_estimators']],
                      max_depth_ls[best_results['max_depth']],
                      min_child_weight_ls[best_results['min_child_weight']],
                      best_results['learning_rate'], best_results['gamma'], best_results['subsample'],
                      best_results['colsample_bytree'],
                      np.sqrt(mean_squared_error(data_te_y, te_pred)), r2_score(data_te_y, te_pred),
                      mean_absolute_error(data_te_y, te_pred)]
        pd_res.append(te_results)

        para_res = pd.DataFrame(pd_res, columns=['FP_type', 'split_type', 'type','num_of_compounds',
                'n_estimators', 'max_depth','min_child_weight',
                'learning_rate','gamma','subsample','colsample_bytree','rmse', 'r2', 'mae'])


    pd_res = []
    for i in range(9):
        item = best_model_runing((i+1),best_results,data,split_type=split_type,FP_type=FP_type,task_type=task_type,model_dir=model_dir)
        pd_res.extend(item)

    if task_type == 'cla':
        best_res = pd.DataFrame(pd_res, columns=['seed','FP_type', 'split_type', 'type',
                                                         'num_of_compounds', 'precision', 'se', 'sp',
                                                         'acc', 'mcc', 'auc_prc', 'auc_roc'])
        pd1 = para_res[['FP_type', 'split_type', 'type',
                        'num_of_compounds', 'precision', 'se', 'sp',
                        'acc', 'mcc', 'auc_prc', 'auc_roc']]
        pd1['seed'] = 0
        best_res = pd.concat([pd1, best_res], ignore_index=True)
    else:
        best_res = pd.DataFrame(pd_res, columns=['seed', 'FP_type', 'split_type', 'type',
                                                 'num_of_compounds', 'rmse', 'r2', 'mae'])
        pd1 = para_res[['FP_type', 'split_type', 'type',
                        'num_of_compounds', 'rmse', 'r2', 'mae']]
        pd1['seed'] = 0
        best_res = pd.concat([pd1, best_res], ignore_index=True)
    return  para_res,best_res
# df = pd.read_csv('/data/jianping/bokey/OCAICM/dataset/aurorab/aurorab.csv')
# a,b =tvt_xgb(df['Smiles'],df['activity'],split_type='cluster')
# print(a,b)
