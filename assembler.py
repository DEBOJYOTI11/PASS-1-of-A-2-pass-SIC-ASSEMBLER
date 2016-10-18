import sys
from collections import OrderedDict


#intitialization
location = 0
symtab = OrderedDict()
littab= OrderedDict()
pooltab=[]
pooltab.append(1)

pp = 1
lp= 1
sp =0
lc=0

fi = open("program.txt","r+")
fo = open("imm_code.txt", "w+")
fm = open("optab.txt","r+")

reg = {"AREG,":1,"BREG,":2,"CREG,":3}

def cat(inpt):
     k,j=0,0
     ar = []
     temp=[]
     

     for i in inpt:
          if i.isspace() and j!=0:
               x = ''.join(temp)
               ar.append(x)
               temp = []
               j = 0
               k= k+1
               continue
          elif not i.isspace():
               temp.append(i)
               j = len(temp)

     if len(temp)!=0:
          x = ''.join(temp)
          ar.append(x)
     return ar




def procedure(i):
      global lc
      global location
      global label
      global lp
      global sp
      global pp
      if len(arr)!=0:
           lc = lc +1

      while True:
           
          op = fm.readline()
          if len(op)==0:
               break
          opt = cat(op)
          
          #after finding the required opcode
          try:
               res = cmp(arr[i].upper(),opt[0].upper())
          except:
               label=1
               return
          

          if res ==0:

               #if addesmbler directive
               if cmp(opt[1],"AD")==0:
                    
                    if cmp(opt[0].upper(),"END")==0 :
                         for p in range(pooltab[pp-1],lp):
                              tt = littab.keys()[p-1]
                              littab[tt] = location
                              location = location +1
                         pp = pp+1
                         pooltab.append(lp)
                         
                         fo.write( "    ("+opt[1]+","+opt[2][1:3]+")")
                         
                    if cmp(opt[0].upper(),"START") ==0:
                         location = int(arr[i+1])
                         p =   "   (" + opt[1] +"," + opt[2][1:3]+")" + "  ("+ "C" + ","+ arr[i+1] + ")"
                         fo.write(p)

                    if cmp(opt[0].upper(),"ORIGIN")==0:
                         location = int(arr[i+1])
                         p ="    (" + opt[1] +"," + opt[2][1:3]+")" + "    ("+"C"+","+arr[i+1]+")"
                         fo.write(p)

                    if cmp(opt[0].upper(),"EQU")==0:
                         try:
                              symtab[arr[i]] = int(arr[i+2])
                              fo.write(str(location) + "    ("+ optp[1]+","+opt[2][1:3]+")"+"  ("+"C"+","+str(arr[i+2])+")")
                         except:
                              symtab[arr[0]]=symtab[arr[i+2]]
                              fo.write(str(location) + "    ("+ optp[1]+","+opt[2][1:3]+")"+"  ("+"S"+","+arr[i+2]+")")

               
                         


               # If DL statements
               if cmp(opt[1],"DL")==0:
                    
                    if cmp(opt[0].upper(),"LTORG") == 0 :
                         for p in range(pooltab[pp-1],lp):
                              
                              tt = littab.keys()[p-1]
                              littab[tt] = location
                              location = location +1
                              
                         pp = pp+1
                         pooltab.append(lp)
                         fo.write(str(location)+"  (AD,"+opt[2][1:3]+")")

                    if cmp(opt[0].upper(),"DC") ==0:
                         
                         code = int(arr[i+1][1:2])
                         fo.write(str(location)+"  (DL," +opt[2][1:3]+")"+"     (C,"+arr[i+1][1:2]+")")
                         location = location + code
                         
                    if  cmp(opt[0].upper().upper(),"DS") ==0:
                         
                         code = int(arr[i+1])
                         fo.write(str(location)+" (DL," +opt[2][1:3]+")"+"      (C,"+arr[i+1]+")")
                         location = location + code

                         
               
               #IF Imperative statements
               if cmp(opt[1].upper(),"IS")==0:
                  fo.write(str(location) + " ("+opt[1]+","+opt[2][1:3]+")")

                  if cmp(opt[0].upper(),"STOP") == 0:
                       label=1
                       location = location +1
                       fo.write("\n")
                       break
                  xx=0
                  for y in reg:
                       if cmp(y,arr[i+1]) == 0:
                            fo.write(" ("+str(reg[y])+")")
                            xx = 1
                   
                  if xx == 0:
                       try:
                            arr[i+2]=arr[i+2].upper()
                            xx = i+2
                       except:
                            xx = i+1
                  else:
                       xx = i+2

                  

                  if arr[xx][0]=='=':
                       littab[arr[xx]] = location
                       fo.write("  (L,"+str(lp)+")")
                       lp = lp +1
                  else:
                       if symtab.has_key(arr[xx]) == False:
                            symtab[arr[xx]]=location
                            sp = sp+1
                       fo.write("  (S," + str(symtab.keys().index(arr[xx]) +1) + ")")
                      
                  location = location + int(opt[2][4:5])     
               fo.write("\n")
               label=1


      fm.seek(0,0)


#main loop of execution
if __name__ == '__main__':
     while True:
          inpt = fi.readline()
          if len(inpt) == 0:
               break
          arr = cat(inpt)
          
          label,nex= 0,0
          procedure(0)
          
          if label == 0:
               symtab[arr[0]]=location
               sp = sp+1
               procedure(1)
               if label ==0:
                    print("Syntax error at line "+ str(lc))
                    sys.exit()

fm.close()
fi.close()
fo.close()
print("ASSEMBLED CORRECTLY\nIMM_CODE FORMED IN THE SMAE FOLDER")


fo = open("data.txt","w")
print(symtab)
print(littab)
print(pooltab)
fo.write("SYMTAB\nLABEL\t\tADDRESS\n")
for x,y in symtab.items():
     fo.write(str(x) + "\t\t" +str(y) +"\n")
fo.write("\n\n\nLITTAB\nLITERALS   \tADDRESS\n")
for x,y in littab.items():
     fo.write(str(x) + "\t\t" +str(y) +"\n")

fo.close()

               
               
     
     



