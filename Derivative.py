import math
import sys

def Error(string):
    print(string)
    sys.exit()

class Calc:
    def __init__(self,op=None,l=None,r=None):
        self.operation=op
        self.left=l
        self.right=r
        if(op!=None):
            if(l==None):
                self.type="F"#Function
            else:
                self.type="O"#Operation
        else:
            if(r==None):
                self.type='K'#Known
            else:
                self.type='U'#Unknown

    @staticmethod
    def __Add(l,r):
        return l+r

    @staticmethod
    def __Subtract(l,r):
        return l-r

    @staticmethod
    def __Multply(l,r):
        return l*r

    @staticmethod
    def __Divide(l,r):
        return l/r

    @staticmethod
    def __Power(l,r):
        return pow(l,r)

    @staticmethod
    def __exp(x):
        return pow(math.e,x)

    Operation_dic={'^':__Power.__func__,'/':__Divide.__func__,
                '*':__Multply.__func__,'+':__Add.__func__,'-':__Subtract.__func__}
    Bracket_set={'(',')'}
    Order_Operation=['^','/','*','+','-']
    Function_dic={'sin':math.sin,'cos':math.cos,'tan':math.tan,
                        'asin':math.asin,'acos':math.acos,'atan':math.atan,
                        'hsin':math.sinh,'hcos':math.cosh,'htan':math.tanh,
                        'ln':math.log,'log':math.log10,'exp':__exp.__func__}

    def __str__(self):
        if(self.type=='K'):
            if(int(self.left)==self.left):
                return str(int(self.left))
            return str(self.left)
        if(self.type=='U'):
            return str(self.right)
        if(self.type=='F'):
            return self.operation+'('+str(self.right)+')'
        if(self.type=='O'):
            l=str(self.left)
            r=str(self.right)
            if(self.left.type=='O'):
                if(self.operation=='^'):
                    if(self.left.operation!='^'):
                        l='('+l+')'
                elif(self.operation in ['/','*']):
                    if(self.left.operation in ['+','-']):
                        l='('+l+')'
            if(self.right.type=='O'):
                if(self.operation=='^'):
                    if(self.right.operation!='^'):
                        r='('+r+')'
                elif(self.operation=='/'):
                    if(self.right.operation in ['*','+','-']):
                        r='('+r+')'
                elif(self.operation=='*'):
                    if(self.right.operation in ['+','-']):
                        r='('+r+')'
                elif(self.operation=='-'):
                    if(self.right.operation=='+'):
                        r='('+r+')'
            return l+self.operation+r

    def __repr__(self):
        return str(self)
    
    @staticmethod
    def __getFn(s,unk):
        t=''.join(s)
        if(t in Calc.Function_dic.keys()):
            return t
        if(t=='e'):
            return Calc(l=math.e)
        if(t=='pi'):
            return Calc(l=math.pi)
        if(len(t)==1 and t in unk):
            return t
        return None

    @staticmethod
    def const(c):
        return Calc(None,c,None)

    @staticmethod
    def var(c):
        return Calc(None,None,c)
    
    @staticmethod
    def fn(fn,c):
        return Calc(fn,None,c)
    
    @staticmethod
    def op(op,l,r):
        return Calc(op,l,r)

    def __isZero(self):
        if(self.type=='K' and self.left==0):
            return True
        return False

    def __isOne(self):
        if(self.type=='K' and self.left==1):
            return True
        return False


    def __add__(self,o):
        if(self.type=='K' and o.type=='K'):
            return Calc.const(self.left+o.left)
        if(self.__isZero()):
            return o
        if(o.__isZero()):
            return self
        return Calc.op('+',self,o)
    
    def __xor__(self,o):#for power
        if(self.type=='K' and o.type=='K'):
            if(o.__isZero() and self.__isZero()):
                Error("Math Error: 0^0 is not defined")
            return Calc.const(pow(self.left,o.left))
        if(self.__isZero()):
            return Calc.const(0)
        if(o.__isZero() or self.__isOne()):
            return Calc.const(1)
        return Calc.op('^',self,o)
    
    def __mul__(self,o):
        if(self.type=='K' and o.type=='K'):
            return Calc.const(self.left*o.left)
        if(self.__isZero() or o.__isZero()):
            return Calc.const(0)
        if(self.__isOne()):
            return o
        if(o.__isOne()):
            return self
        return Calc.op('*',self,o)
    
    def __truediv__(self,o):
        if(o.__isZero()):
            Error("Math Error: /0 is not defined")
        if(o.type=='K' and self.type=='K'):
            return Calc.const(self.left/o.left)
        if(o.__isOne()):
            return self
        return Calc.op('/',self,o)
    
    def __sub__(self,o):
        if(self.type=='K' and o.type=='K'):
            return Calc.const(self.left-o.left)
        if(o.__isZero()):
            return self
        return Calc.op('-',self,o)


    @staticmethod
    def __Parse_toList(string,unk=None):
        string='('+string.replace(" ","")+')'
        num_str=[]
        output=[]
        fn_str=[]

        for i in range(len(string)):
            if(string[i] in Calc.Operation_dic.keys() or string[i] in Calc.Bracket_set):
                if(len(fn_str)>0):
                    output.append(Calc.__getFn(fn_str,unk))
                    if(output[-1]==None):
                        Error("Missing Bracket at position: "+str(i-1))
                    fn_str=[]
                elif(len(num_str)>0):
                    t=float(''.join(num_str))
                    output.append(Calc(None,t,None))
                    num_str=[]
                output.append(string[i])
            elif(string[i].isdigit() or string[i]=='.'):
                if(len(fn_str)>0):
                    Error("Missing Bracket at position: "+str(i-1))
                num_str.append(string[i])
            else:
                if(len(num_str)>0):
                    t=float(''.join(num_str))
                    output.append(Calc(None,t,None))
                    num_str=[]
                fn_str.append(string[i])

        for i in range(len(output)-1):
            if(type(output[i])==Calc):
                if(not(output[i+1] in Calc.Operation_dic.keys() or output[i+1]==')')):
                    output.insert(i+1,'*')

        i=1
        while i<len(output)-1:
            if(output[i]=='-'):
                if(output[i+1]!='('):
                    if(type(output[i-1])!=Calc and output[i-1]!=')'):
                        if(type(output[i+1])==Calc):
                            output[i+1].left*=-1
                        else:
                            output.insert(i+1,Calc(l=-1))
                            output.insert(i+2,'*')
                        output.pop(i)        
            i+=1

        return output           
    
    @staticmethod
    def __ParseVar(a,unk):
        i=0
        while i<len(a):
            if(a[i] in unk):
                a[i]=Calc(r='x')
            i+=1
        return a

    @staticmethod
    def __ParseFn(a):
        i=0
        while i<len(a):
            if(a[i] in Calc.Function_dic.keys()):
                a[i]=Calc(a[i],None,a[i+1])
                a.pop(i+1)
            i+=1
        return a
                
    @staticmethod
    def __ParseOp(a,op):
        i=1
        while i<len(a)-1:
            if(a[i] in op):
                temp=a[i]
                if(type(a[i-1])!=Calc or type(a[i+1])!=Calc):
                    Error("Syntax Error")
                a[i-1]=Calc(temp,a[i-1],a[i+1])
                del a[i:i+2]
                continue
            i+=1
                
    @staticmethod
    def __ParseAllOp(a,unk):
        if(a[-1] in Calc.Operation_dic.keys()):
            Error("Syntax Error")
        Calc.__ParseVar(a,unk)
        Calc.__ParseFn(a)
        Calc.__ParseOp(a,['^'])
        Calc.__ParseOp(a,['*','/'])
        Calc.__ParseOp(a,['+','-'])
        return a

    @staticmethod
    def __Parse(a,unk):
        left_brac=[]
        i=0
        while i<len(a):
            if(a[i]=='('):
                left_brac.append(i)
            elif(a[i]==')'):
                try:
                    lpos=left_brac.pop(-1)
                except:
                    Error("Unbalanced Brackets")
                val=Calc.__ParseAllOp(a[lpos+1:i],unk)[0]
                del a[lpos+1:i+1]
                a[lpos]=val
                i=lpos
            i+=1
        
        if(len(left_brac)>0):
            Error("Unbalanced Brackets")

    @staticmethod
    def Parse(input_string,unk=None):    
        input_list=Calc.__Parse_toList(input_string,unk)
        Calc.__Parse(input_list,unk)
        return input_list[0]


    def Evaluate(self,unk=None):
        if(self.type=='U'):
            return unk[self.right]
        if(self.type=='K'):
            return self.left
        if(self.type=='O'):
            return Calc.Operation_dic[self.operation](self.left.Evaluate(unk),self.right.Evaluate(unk))
        if(self.type=='F'):
            return Calc.Function_dic[self.operation](self.right.Evaluate(unk))
        

class DerFn:
    @staticmethod
    def __sin(x):
        return Calc.fn("cos",x)

    @staticmethod
    def __cos(x):
        return Calc.const(-1)*Calc.fn("sin",x)

    @staticmethod
    def __tan(x):
        return Calc.fn("cos",x)^Calc.const(-2)

    @staticmethod
    def __ln(x):
        return Calc.const(1)/x
    
    @staticmethod
    def __log(x):
        return Calc.const(math.log10(math.e))/x
    
    @staticmethod
    def __asin(c):
        return Calc.const(1)/(Calc.const(1)-c^Calc.const(2))^Calc.const(1/2)

    @staticmethod
    def __acos(c):
        return Calc.const(-1)/(Calc.const(1)-c^Calc.const(2))^Calc.const(1/2)
    
    @staticmethod
    def __atan(c):
        return Calc.const(1)/(Calc.const(1)+c^Calc.const(2))

    @staticmethod
    def __hsin(c):
        return Calc.fn('hcos',c)

    @staticmethod
    def __hcos(c):
        return Calc.fn('hsin',c)
    
    @staticmethod
    def __htan(c):
        return Calc.fn('hcos',c)^Calc.const(-2)
    
    @staticmethod
    def __exp(x):
        return Calc.const(math.e)^x


    @staticmethod 
    def __Add(l,r,var):
        return Differentiate(l,var)+Differentiate(r,var)
    
    @staticmethod
    def __Subtract(l,r,var):
        return Differentiate(l,var)-Differentiate(r,var)
    
    @staticmethod
    def __Multply(l,r,var):
        return Differentiate(l,var)*r+Differentiate(r,var)*l

    @staticmethod
    def __Divide(l,r,var):
        return (Differentiate(l,var)*r-Differentiate(r,var)*l)/(r^Calc.const(2))

    @staticmethod
    def __Power(l,r,var):
        t1=r*Differentiate(l,var)/l+Differentiate(r,var)*Calc.fn("ln",l)
        return t1*(l^r)

    Function_dic={"sin":__sin.__func__,"cos":__cos.__func__,"tan":__tan.__func__,
    "asin":__asin.__func__,"acos":__acos.__func__,"atan":__atan.__func__,
    "hsin":__hsin.__func__,"hcos":__hcos.__func__,"htan":__htan.__func__,
    "ln":__ln.__func__,"log":__log.__func__,"exp":__exp.__func__}

    Operation_dic={"^":__Power.__func__,"/":__Divide.__func__,"*":__Multply.__func__,
                    "+":__Add.__func__,"-":__Subtract.__func__}

def Differentiate(t,var):#To Differentiate
    if(t.type=='K'):
        return Calc.const(0)
    if(t.type=='U'):
        if(t.right==var):
            return Calc.const(1)
        else:
            return Calc.const(0)
    
    if(t.type=='F'):
        return Calc.op('*',DerFn.Function_dic[t.operation](t.right),Differentiate(t.right,var))

    if(t.type=='O'):
        return DerFn.Operation_dic[t.operation](t.left,t.right,var)
            
    return Calc.const(0)


# a="exp(e)"
# p=Calc.Parse(a,['x'])
# print(p)
# print(p.Evaluate({'x':2}))
# print(Differentiate(p,'x').Evaluate({'x':2}))