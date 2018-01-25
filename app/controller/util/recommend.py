import math
def ItemSimilarity(train):
    #计算每个用户两两物品间的相似度矩阵
    C = dict()  #存储物品两两间的相似矩阵
    N = dict()  #存储喜欢视频i的用户数
    for users, itemsWeight in train.items():
        for i in itemsWeight.keys():
            if i not in N:
                N[i] = 0
            N[i] += 1
            for j in itemsWeight.keys():
                if i == j:
                    continue
                if i in C:
                    if j in C[i]:
                        C[i].update({j: C[i][j] + 1})
                    else:
                        C[i].update({j: 1})
                else:
                    C.update({i: {j: 1}})

    #将所有用户的相似度矩阵归一，计算物品间最终的相似度矩阵w
    W = dict()
    for i,related_items in C.items():
        for j, cij in related_items.items():
            if i in W :
                W[i].update({j: cij / math.sqrt(N[i] * N[j])})
            else:
                W.update({i: {j: cij / math.sqrt(N[i] * N[j])}})

    return W

def Recommendation(train, user_id, W, K):
    rank = dict()
    ru = train[user_id]     #目标用户的视频权重列表
    for i,pi in ru.items():
        for j, wj in sorted(W[i].items(), key=lambda s: s[1], reverse=True)[0:K]:   #取与视频i最相似的前k个视频
            if j in ru:
                continue
            if j not in rank:
                rank[j] = 0
            rank[j] += pi * wj  #由用户感兴趣视频权重和推荐视频的相似度计算出推荐程度
    return rank