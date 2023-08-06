def repr(classname,self,args):
    ret=f"{classname}("
    for v in args.split(","):
        try:
            ret += f'{v}={eval(f"self.{v}")},'
        except:
            pass
    ret += "\b)"
    return ret
if __name__ == "__main__":
    class test:
        def __init__(self,a,b,c) -> None:
            self.a=a
            self.b=b
            self.c=c
        def test(self):
            return repr("test",self,"a,c")
    print(test(1,2,3).test())