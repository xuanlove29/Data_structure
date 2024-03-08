import random
import plotly.graph_objs as go
def gragh_dense(points_x,points_y):
    lines_x,lines_y=[],[]
    points_num=len(points_x)
    #初始化邻接表
    G={id:{} for id in range(points_num)}
    for id_i in range(points_num):
        for id_j in range(id_i+1,points_num):
            #取消头尾相连
            if id_i+id_j==1:
                continue
            lines_x.extend([points_x[id_i],points_x[id_j]])
            lines_y.extend([points_y[id_i],points_y[id_j]])
            d=((points_x[id_i]-points_x[id_j])**2+(points_y[id_i]-points_y[id_j])**2)**0.5
            G[id_i][id_j]=G[id_j][id_i]=d
    return G,lines_x,lines_y
#设置id：0为起始点，1为终止点，随机连通路径，通过layer控制图的稀疏程度
def gragh_sprase(points_x,points_y,layer=3):
    # 初始化邻接表
    points_num=len(points_x)
    #G为邻接表
    G={id:{} for id in range(points_num)}
    # 初始化路径信息
    traces=[]
    #设置layer索引
    index=list(range(2,len(points_x)))
    random.shuffle(index)
    split_len=len(points_x)//layer
    part_index=[]
    for i in range(layer):
        part_index.append(index[i*split_len:(i+1)*split_len])
    #起始点链接
    for id_i in part_index[0]:
        G[id_i][0]=G[0][id_i]=((points_x[id_i]-points_x[0])**2+(points_y[id_i]-points_y[0])**2)**0.5
        traces.append(go.Scatter(x=[points_x[0],points_x[id_i]],y=[points_y[0],points_y[id_i]],mode='lines',
                                 line=dict(color='green', width=1)))
    #终止点链接
    for id_i in part_index[-1]:
        G[id_i][1]=G[1][id_i] = ((points_x[id_i] - points_x[1]) ** 2 + (points_y[id_i] - points_y[1]) ** 2) ** 0.5
        traces.append(go.Scatter(x=[points_x[1], points_x[id_i]], y=[points_y[1], points_y[id_i]], mode='lines',
                                 line=dict(color='green', width=1)))
    #层级互联
    for i in range(0,layer-1):
        for id_l in part_index[i]:
            for id_r in part_index[i+1]:
                G[id_l][id_r]=G[id_r][id_r]=((points_x[id_r]-points_x[id_l])**2+(points_y[id_r]-points_y[id_l])**2)**0.5
                traces.append(go.Scatter(x=[points_x[id_r], points_x[id_l]], y=[points_y[id_r], points_y[id_l]], mode='lines',
                                         line=dict(color='green', width=1)))
    return G,traces

#dijkstra算法（邻接表）
def dijkstra(gragh, start_id):
    # 初始化距离和路径
    dist = {v: float('infinity') for v in gragh}
    path_pre = {v: None for v in gragh}
    for w,d in gragh[start_id].items():
        dist[w]=gragh[start_id][w]
        path_pre[w]=start_id
    # 集合
    vis = set()
    vis.add(start_id)
    while (len(vis) < len(gragh)):
        # 选择最短节点
        mindis_v = min((v for v in gragh if v not in vis), key=dist.get)
        vis.add(mindis_v)
        # 更新
        for w,d in gragh[mindis_v].items():
            if w not in vis and dist[mindis_v]+gragh[mindis_v][w]<dist[w]:
                dist[w]=dist[mindis_v]+gragh[mindis_v][w]
                path_pre[w]=mindis_v
    print(path_pre)
    return dist, path_pre
#路径id解析
def path_parse(path_pre, target):
    path = []
    cur_v = target
    while cur_v is not None:
        path.insert(0, cur_v)
        cur_v = path_pre[cur_v]
    return path
#Dijsktra求路径
def dijkstra_path(gragh,start,end,reverse=False):
    #调用dijkstra算法
    dist,path_pre=dijkstra(gragh,start)
    #从路径前缀获取路径信息
    path=path_parse(path_pre,target=end)
    return path

#路径id可视化
def line_bypath(path,points_x,points_y):
    lines_x=[points_x[id] for id in path]
    lines_y=[points_y[id] for id in path]
    return lines_x,lines_y
