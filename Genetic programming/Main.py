from random import random,randint,choice
from copy import deepcopy
from math import log
import sys
sys.setrecursionlimit(1000000000)

class node:
    def __init__(self,childrens,fun):
        self.fun=fun
        self.childrens=childrens
    def getChilds(self):
        return self.childrens
    def getChild1(self):
        return self.childrens[0]
    def getChild2(self):
        return self.childrens[1]
    def getFun(self):
        return self.fun
    def setChilds(self,childs):
        self.childrens=childs
    def setChild1(self,child):
        self.childrens[0]=child
    def setChild2(self,child):
        self.childrens[1]=child
    def setFun(self,fun):
        self.fun=fun
    def getStruct(self):
        a = self.childrens[0]
        b = self.childrens[1]
        f = self.fun
        f_name = fun_to_symbol(f)
        
        if isinstance(a,node):
            a=a.getStruct()
        elif isinstance(a,param):
            a=a.getName()
        if isinstance(b,node):
            b=b.getStruct()
        elif isinstance(b,param):
            b=b.getName()
        return ("("+str(a)+str(f_name)+str(b)+")")
    def getRes(self,var_s,c=0):
        a = self.childrens[0]
        b = self.childrens[1]
        f = self.fun
        
        if isinstance(a,node):
            a=a.getRes(var_s,c+1)
        elif isinstance(a,param):
            a=var_s[a.getPos()]
        if isinstance(b,node):
            b=b.getRes(var_s,c+1)
        elif isinstance(b,param):
            b=var_s[b.getPos()]
        return f(a,b)
class param:
    def __init__(self,name,pos):
        self.name = name
        self.pos = pos
    def getName(self):
        return self.name
    def getPos(self):
        return self.pos


def fun_to_symbol(fun):
    mp = {summ:'+',minn:'-',mult:'*'}
    return mp[fun]    

def orig_fun(params):
    return 4*params[1]+params[0]-3

def build_data(params_count=2,count=20,spread=1000):
    rows=[]
    for i in range(count):
        pars = []
        for j in range(params_count):
            pars.append(randint(-spread,spread))
        rows.append([pars,orig_fun(pars)])
    return rows

def error(top,data):
    er=0
    for s in data:
        er+=abs(top.getRes(s[0])-s[1])
    return er

def mutate(top,p=50,params=['a','b'],c_p=[30,70],spread=3):
    r=randint(1,100)
    if r<=p:
        k=randint(1,3)
        if k==1:
            top.setFun(choice(funs))
        elif k==2:
            g=randint(1,100)
            if g<=30:
                top.setChild1(randint(-spread,spread))
            else:
                t=randint(0,len(params)-1)
                top.setChild1(param(params[t],t))
        else:
            g=randint(1,100)
            if g<=30:
                top.setChild2(randint(-spread,spread))
            else:
                t=randint(0,len(params)-1)
                top.setChild2(param(params[t],t))
    
    if(isinstance(top.getChild1(),node)): top.setChild1(mutate(top.getChild1()))
    if(isinstance(top.getChild2(),node)): top.setChild2(mutate(top.getChild2()))
    return top

def get_rand_node(top,p=30):
    r=randint(1,100)
    t=randint(1,2)
    if not isinstance(top,node):
        return top
    if t==1:
        tp=top.getChild1()
        if r<=p and not isinstance(tp,node): return top
        return get_rand_node(tp)
    else:
        tp=top.getChild2()
        if r<=p and not isinstance(tp,node): return top
        return get_rand_node(tp)
    
def set_rand_node(top,n,p=40):
    if not isinstance(top,node):
        return top
    t=randint(1,2)
    r=randint(1,100)
    if t==1:
        if r<=p: top.setChild1(n)
        else: top.setChild1(set_rand_node(top.getChild1(),n))
    else:
        if r<=p: top.setChild2(n)
        else: top.setChild2(set_rand_node(top.getChild2(),n))
    return top
def crossover(top1,top2):
    n=get_rand_node(top2)
    r2=randint(1,2)
    if r2==1:
        top1.setChild1(n)
    else:
        top1.setChild2(n)
    return top1
    
def summ(a,b): return a+b
def minn(a,b): return a-b
def mult(a,b): return a*b

funs = [summ,minn,mult]

def make_tree(max_depth=3,p=[70,20,10],parms=['a','b'],spread=3):
    n=[None,None]
    f=choice(funs)
    if max_depth>1:
        s = sum(p)
        r = [randint(1,s),randint(1,s)]
        for i in range(0,len(r)):
            if r[i]<=p[0]:
                n[i]=make_tree(max_depth-1,p)
            elif r[i]<=p[0]+p[1]:
                k=randint(0,len(parms)-1)
                n[i]=param(parms[k],k)
            else:
                n[i]=randint(-spread,spread)
    else:
        s = sum(p[1:])
        r = [randint(1,s),randint(1,s)]
        for i in range(0,len(r)):
            if r[i]<=p[1]:
                k=randint(0,len(parms)-1)
                n[i]=param(parms[k],k)
            else:
                n[i]=randint(-spread,spread)
    return node(n,f)
    
def evolve(start_count=5,max_err=1000,cross_top=3):
    scores = {}
    data = build_data()
    while len(scores)!=start_count:
        top = make_tree()
        e = round(error(top,data),5)
        if e==0:
            print(top.getStruct())
            print(0)
            return
        if e<=max_err:
            if e not in scores:
                scores[e]=top
                print(len(scores),"/",start_count)
    sorted_keys = sorted(scores)
    print(scores[sorted_keys[0]].getStruct())
    print(sorted_keys[0],len(scores))
    while sorted_keys[0]!=0:
        for i in range(cross_top,len(sorted_keys)):
            pred_err=sorted_keys[i]
            tree=mutate(scores[pred_err])
            e=round(error(tree,data),5)
            if e<pred_err:
                scores.pop(pred_err)
                scores[e]=tree
                sorted_keys[i]=e
        h=min(cross_top,len(sorted_keys))
        for i in range(h):
            for j in range(i+1,h):
                e1=sorted_keys[i]
                e2=sorted_keys[j]
                tree=crossover(scores[e1],scores[e2])
                e=round(error(tree,data),5)
                if e<e1:
                    scores.pop(e1)
                    scores[e]=tree
                    sorted_keys[i]=e
        sorted_keys=sorted(scores)
        while len(scores)!=start_count:
            top = make_tree()
            e = round(error(top,data),5)
            if e<=max_err: scores[e]=top
        print(scores[sorted_keys[0]].getStruct())
        print(sorted_keys[0],len(scores))
        
evolve()
#(params[0]-params[1]+84)*2
#n1 = node([param('a',0),param('b',1)],minn)
#n2 = node([n1,84],summ)
#N = node([n2,2],mult)
#print(N.getRes([342546576.265,34254645]))