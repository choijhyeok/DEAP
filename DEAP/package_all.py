#!/usr/bin/env python
# coding: utf-8

# In[1]:

import pandas as pd
import numpy as np
import random

from deap import base
from deap import creator
from deap import tools
from deap import algorithms

import random
import numpy
import matplotlib.pyplot as plt
import seaborn as sns

from . import new_environment

plt.rcParams['figure.figsize'] = [15, 8]




def region_mapping(real_data,env): # 지역매핑
    yester = []
    local_df = pd.DataFrame()
    for num,i in enumerate(real_data['product_code']):
        local_list = [] # 첫 loop때 마다 local_list 초기화용

        if(num in yester): # 중복 num 방지 num1이 num이 될경우 방지
            pass

        else:
            for num1,d in enumerate(real_data['product_code']):
                if((i == d)&(real_data.iloc[num]['amount'] == real_data.iloc[num1]['amount'])&(num != num1)&(real_data.iloc[num]['company_code'] != real_data.iloc[num1]['company_code'])): # product,amount같고 회사 다르고 자기 자신이 아닌것 선정
                    if((real_data.iloc[num]['first_area'] == real_data.iloc[num1]['shipping_area']) & (real_data.iloc[num]['shipping_area'] == real_data.iloc[num1]['first_area'])): # first_area,shipping 크로스 로 같은거
                        local_list.append(num1)

            if(len(local_list)<1): # 빈 리스트 무시
                pass

            else:

                local_list.append(num) # num 과 num1을 비교했는데 num의 중복을 막기위해서 for loop 끝난후에 추가

                yester += local_list # local_list에 담긴 내용을 yester 에 추가해서 num이 나중에 num1의 인덱스를 가져도 안돌아가게 하기위한 중복방지용


                local_list = list(set(local_list)) # 중복방지
                save_list = [real_data.iloc[i]['cost'] * env.get_saving_rate(real_data.iloc[i]['company_code'],real_data.iloc[i]['shipping_area'],real_data.iloc[i]['first_area']) for i in local_list] #절감비 구하기

                for d,i in enumerate(local_list):
#                     if(d != save_list.index(max(save_list))): #절감비중 최대값 따로 데이터프레임 만들기 위해서
                    local_df = local_df.append({'order_id':real_data.iloc[i]['order_id'],'company_code':real_data.iloc[i]['company_code'],'product_code':real_data.iloc[i]['product_code'],'amount':real_data.iloc[i]['amount'],'shipping_area':real_data.iloc[i]['shipping_area'],'first_area':real_data.iloc[i]['first_area'],'cost':real_data.iloc[i]['cost'],'get_save':save_list[d]}, ignore_index=True)

#                     else:
#                         local_df = local_df.append({'order_id':real_data.iloc[i]['order_id'],'company_code':real_data.iloc[i]['company_code'],'product_code':real_data.iloc[i]['product_code'],'amount':real_data.iloc[i]['amount'],'shipping_area':real_data.iloc[i]['shipping_area'],'first_area':real_data.iloc[i]['first_area'],'cost':real_data.iloc[i]['cost'],'change_id': 0,'get_save': 0}, ignore_index=True)
    
    return local_df.drop_duplicates() #중복 방지




def logistics_mapping(real_data,env): # 물류비 절감률 우선 
    yester = []
    local_df = pd.DataFrame()
    for num,i in enumerate(real_data['product_code']):
        local_list = [] # 첫 loop때 마다 local_list 초기화용

        if(num in yester):  # 중복 방지용
            pass

        else:
            for num1,d in enumerate(real_data['product_code']):
                if((i == d)&(real_data.iloc[num]['amount'] == real_data.iloc[num1]['amount'])&(num != num1)&(real_data.iloc[num]['company_code'] != real_data.iloc[num1]['company_code'])):  # product,amount 같고 인덱스는 다르고 company도 다른것 고르고
                    if(real_data.iloc[num]['shipping_area'] == real_data.iloc[num1]['shipping_area']): # 물류비 절감 우선의 핵심인 shipping area를 같은 것을 뽑고
                        local_list.append(num1) # 저장

            if(len(local_list)<1): # 빈 리스트일경우 무시
                pass

            else:
                local_list.append(num) # num 과 num1을 비교했는데 num의 중복을 막기위해서 for loop 끝난후에 추가
                yester += local_list # local_list에 담긴 내용을 yester 에 추가해서 num이 나중에 num1의 인덱스를 가져도 안돌아가게 하기위한 중복방지용

                local_list = list(set(local_list)) # 중복방지


                save_list = [real_data.iloc[i]['cost'] * env.get_saving_rate(real_data.iloc[i]['company_code'],real_data.iloc[i]['shipping_area'],real_data.iloc[i]['first_area']) for i in local_list]  # local_list에 담겨져있는 index를 통해서 절감물류비를 계산하여 save_list에 담는 코드

                for d,i in enumerate(local_list):
#                     if(d != save_list.index(max(save_list))):  # 만약 최대값의 절감비 는 change_id , save 부분을 0,0 으로 하기위해서 최대값 절감이외의 작업
                    local_df = local_df.append({'order_id':real_data.iloc[i]['order_id'],'company_code':real_data.iloc[i]['company_code'],'product_code':real_data.iloc[i]['product_code'],'amount':real_data.iloc[i]['amount'],'shipping_area':real_data.iloc[i]['shipping_area'],'first_area':real_data.iloc[i]['first_area'],'cost':real_data.iloc[i]['cost'],'get_save':save_list[d]}, ignore_index=True)

#                     else: # 최대일때 작업
#                         local_df = local_df.append({'order_id':real_data.iloc[i]['order_id'],'company_code':real_data.iloc[i]['company_code'],'product_code':real_data.iloc[i]['product_code'],'amount':real_data.iloc[i]['amount'],'shipping_area':real_data.iloc[i]['shipping_area'],'first_area':real_data.iloc[i]['first_area'],'cost':real_data.iloc[i]['cost'],'change_id': 0,'get_save': 0}, ignore_index=True)
    
    return local_df.drop_duplicates() #중복 방지


def minus_min(save_list):

    bound = []
    C = []
    final_index = []
    for z,i in enumerate(range(len(save_list))):
        for j in range(i+1,len(save_list)):
            bound.append(abs(save_list[i]-save_list[j]))


    for z,i in enumerate(range(len(save_list))):
        for j in range(i+1,len(save_list)):
            if(min(bound) == abs(save_list[i]-save_list[j])):
                final_index.append(i)
                final_index.append(j)
    
    return final_index 




def nearest_logistics_mapping(real_data,env):  #근접 물류비 절감률 우선
    yester = []
    local_df = pd.DataFrame()

    for num,i in enumerate(real_data['product_code']):
        local_list = [] # 첫 loop때 마다 local_list 초기화용

        if(num in yester):  # 중복 방지용
            pass

        else:
            for num1,d in enumerate(real_data['product_code']):
                if((i == d)&(real_data.iloc[num]['amount'] == real_data.iloc[num1]['amount'])&(num != num1)):  # product,amount 같고 인덱스는 다르고 이중 가격으로만 중심을 두고 최대 가격을 중심으로 매핑
                    local_list.append(num1) # 저장

            if(len(local_list)<2): # 빈 리스트일경우 무시
                pass

            else:
                local_list.append(num) # num 과 num1을 비교했는데 num의 중복을 막기위해서 for loop 끝난후에 추가
                yester += local_list # local_list에 담긴 내용을 yester 에 추가해서 num이 나중에 num1의 인덱스를 가져도 안돌아가게 하기위한 중복방지용

                local_list = list(set(local_list)) # 중복방지
#                 print(local_list)

                save_list = [real_data.iloc[i]['cost'] * env.get_saving_rate(real_data.iloc[i]['company_code'],real_data.iloc[i]['shipping_area'],real_data.iloc[i]['first_area']) for i in local_list]
#                 print(save_list)
#                 print(minus_min(save_list))
                for i in minus_min(save_list):
                    local_df = local_df.append({'order_id':real_data.iloc[local_list[i]]['order_id'],'company_code':real_data.iloc[local_list[i]]['company_code'],'product_code':real_data.iloc[local_list[i]]['product_code'],'amount':real_data.iloc[local_list[i]]['amount'],'shipping_area':real_data.iloc[local_list[i]]['shipping_area'],'first_area':real_data.iloc[local_list[i]]['first_area'],'cost':real_data.iloc[local_list[i]]['cost'],'get_save':save_list[i]}, ignore_index=True)
                    
    return local_df.drop_duplicates() #중복 방지


def list_in_tuple(data):
    all_list = []
    for i in range(len(data)):
        all_list.append(tuple(data.iloc[i]))
        
    return all_list


def ran_weight(data):
    
    weight_list =[]
    for i in range(len(data)):
        weight_list.append(random.randrange(1,251))
    
    data['weight'] = weight_list
    return data




    
def DEAP_float(data,local_list,count,num):
    
    MAX_GENERATIONS = 500
    gen_set = 0
    number = num

    while(True):
        POPULATION_SIZE = 30
        P_CROSSOVER = 0.9  
        P_MUTATION = 0.1  
        HALL_OF_FAME_SIZE = 1
        RANDOM_SEED = 42
        random.seed(RANDOM_SEED)

        from . import knapsack_random
        knapsack = knapsack_random.Knapsack01Problem()


        data = ran_weight(data)
        knapsack.getItems(list_in_tuple(data.iloc[local_list][['order_id','cost','get_save','weight']]))
        def knapsackValue_all(individual):
            return knapsack.getValue_all(individual),  # return a tuple



        genetic_tool = base.Toolbox()
        genetic_tool.register("attr_float", random.random)
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMax)
        genetic_tool.register("individualCreator", tools.initRepeat, creator.Individual, genetic_tool.attr_float, len(knapsack))
        genetic_tool.register("populationCreator", tools.initRepeat, list, genetic_tool.individualCreator)
        genetic_tool.register("evaluate", knapsackValue_all)
        genetic_tool.register("select", tools.selTournament, tournsize=3)
        genetic_tool.register("mate", tools.cxTwoPoint)
        genetic_tool.register("mutate", tools.mutGaussian, mu=0, sigma=0.5, indpb=0.2)


        population = genetic_tool.populationCreator(n=POPULATION_SIZE)
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("max", np.max)
        stats.register("avg", np.mean)

        hof = tools.HallOfFame(HALL_OF_FAME_SIZE)

        if gen_set == 0:
            population, logbook = algorithms.eaSimple(population, genetic_tool, cxpb=P_CROSSOVER, mutpb=P_MUTATION,
                                              ngen=MAX_GENERATIONS, stats=stats, halloffame=hof, verbose=False)
        else:
            population, logbook = algorithms.eaSimple(population, genetic_tool, cxpb=P_CROSSOVER, mutpb=P_MUTATION,
                                              ngen=MAX_GENERATIONS, stats=stats, halloffame=hof, verbose=True)
  
        best = hof.items[0]

        maxFitnessValues, meanFitnessValues = logbook.select("max", "avg")
        print()

        if gen_set == 1:
            
            sns.set()

            plt.plot(maxFitnessValues, label='maxFitnessValues')
            plt.plot(meanFitnessValues, label='meanFitnessValues')
            plt.xlabel('Generation',fontsize=20)
            plt.ylabel('Max / Average Fitness',fontsize=20)
            plt.title('Max and Average fitness over Generations',fontsize=30, fontweight='bold')
            plt.grid(True)
            plt.legend(fontsize=20, loc = 'lower right')
            
            if number == 0:
                plt.savefig('./data_image/region_mapping/지역_맵핑_result_{}.png'.format(count), dpi=100)
            elif number == 1:
                plt.savefig('./data_image/logistics_mapping/물류비_절감_우선_맵핑_result_{}.png'.format(count), dpi=100)
            else:
                plt.savefig('./data_image/nearest_logistics_mapping/근접_물류비_절감_맵핑_result_{}.png'.format(count), dpi=100)

            
            print("-- Best Ever Individual = ", best)
            print("-- Best Ever Fitness = ", best.fitness.values[0])

            print("-- Knapsack Items = ")
            knapsack.printItems_all(best)

            plt.show()
            plt.cla()

        best_avg = 0.0
        best_gen = 0
        
        for i in logbook:
            if(i["max"] <= knapsack.maxCapacity):
                if(best_avg < i['avg']):
                    best_avg = i['avg']
                    best_gen = i['gen']
        
        print()
        if MAX_GENERATIONS == best_gen:
            print('\n 현재 수행결과가 가장좋은 결과입니다.')
            break
        else:
            print('최고의 설정은 best avg : {}, best gen : {} 입니다.'.format(best_avg,best_gen))
            if gen_set == 0:
                MAX_GENERATIONS = best_gen
                gen_set = 1
                pass
            else:
                break

    
    
    
def mapping(data,num):

    counter = 0
    pass_list = []
    number = num

    for num1,i in enumerate(data['product_code']):
        globals()['local_list_{}'.format(counter)] = []
        if num1 in pass_list:
            pass
        else:
            for num2,j in enumerate(data['product_code']):
                if((num1 != num2) & (i == j) & (data.iloc[num1]['amount'] == data.iloc[num2]['amount'])):
                    globals()['local_list_{}'.format(counter)].append(num2)
                    pass_list.append(num2)

            globals()['local_list_{}'.format(counter)].append(num1)

            if(len(globals()['local_list_{}'.format(counter)]) == 0):
                break
            else:
                counter +=1
    
    
    print('\n총비교 횟수 :', counter)
    print()
 
    
    for i in range(counter):
        
        if(len(globals()['local_list_{}'.format(i)]) == 2):
            print('\n개수가 2개 단일비교 수행 해당되는 index : {}'.format(globals()['local_list_{}'.format(i)]))

            num1,num2 = data.iloc[globals()['local_list_{}'.format(i)][0]],data.iloc[globals()['local_list_{}'.format(i)][1]]
            print('더 좋은 절감률은 order_id : {}, 그때의 절감률 : {}'.format(num1['order_id'],num1['get_save'])) if num1['get_save'] < num2['get_save'] else print('더 좋은 절감률은 order_id : {}, 그때의 절감률 : {}'.format(num2['order_id'],num2['get_save'])) if num1['get_save'] > num2['get_save'] else print('order_id : {} 와 {}은 같은 절감률 {}을 가짐'.format(num1['order_id'],num2['order_id'],num1['get_save']))

            del  globals()['local_list_{}'.format(i)]

        else:
            
            print('\n 개수가 3개 이상 해당되는 index : {}'.format(globals()['local_list_{}'.format(i)]))
            print()
            print()
            DEAP_float(data,globals()['local_list_{}'.format(i)],i,number)
            
            del  globals()['local_list_{}'.format(i)]

