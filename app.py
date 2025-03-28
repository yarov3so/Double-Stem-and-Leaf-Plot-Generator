#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import streamlit as st

st.set_page_config(
    page_title="Double Stem and Leaf Plot Generator",
    page_icon="MHT.png", 
)

st.title("Double Stem and Leaf Plot Generator")

def comprehend(mystring):
    
    mystring=mystring.replace(" ", "")
    data_list=mystring.split(",")
    data =[]
    for el in data_list:
        try:
            data.append(float(el))
        except: 
            for i in range(int(re.findall(r'\d+', el)[0])):
                data.append(None)
    return data

def magnitude(num):
    
    num=str(num)
    if num[0]!="0":
        if "." in num:
            return num.find(".") - 1
        else:
            return len(num) -1 
    else:
        num=num[2:]
        for i in range(len(num)):
            if num[i]!="0":
                return -i-1 
        return 0

def add_zeros(numstr,numchar):

    while len(numstr[:numstr.index(".")])<numchar:
        numstr="0"+numstr
    return numstr
    
def stempos(numlist):
    
    magnitudes=[magnitude(num) for num in numlist]

   # if all(mag==magnitudes[0] for mag in magnitudes)==False:
   #     raise ValueError("The values in your data set must have similar scale!")

    #mag=magnitudes[0]
    mag=max(magnitudes)


    if mag>=0:
        stemposition=mag
        maxlen_whole=max([len(str(num)[0:str(num).index(".")]) for num in numlist])
        #numlist=[str(num).replace(".","") for num in numlist]
        #maxlen=max([len(num) for num in numlist])
        
        #numlist=[num for num in numlist if len(num)==maxlen] # to be changed 
        numlist=[str(num).replace(".","") for num in numlist if len(str(num)[0:str(num).index(".")])==maxlen_whole]
        
        try:
            all((num[0]==numlist[0][0] for num in numlist))
        except:
            return stemposition
            
        while all((num[0]==numlist[0][0] for num in numlist)):
            stemposition-=1
            numlist=[num[1:] for num in numlist]
            try:
                all((num[0]==numlist[0][0] for num in numlist))
            except:
                return stemposition
    else:
        
        stemposition=mag
        numlist=[str(num).replace(".","")[-mag:] for num in numlist]

        try:
            all((num[0]==numlist[0][0] for num in numlist))
        except:
            return stemposition
        
        while all((num[0]==numlist[0][0] for num in numlist)):
            
            stemposition-=1
            numlist=[num[1:] for num in numlist]

            try:
                all((num[0]==numlist[0][0] for num in numlist))
            except:
                return stemposition
                
    return stemposition

def sl_range(numlist,pos):
    
    digits=[]
    for num in numlist:
        try:
            digits.append(int(str(num)[pos]))
        except:
            digits.append(0)

    return [i for i in range(min(digits),max(digits)+1)]

def try_int(num):
    
    num_int=None
    try:
        num_int=int(num)
    except:
        return num
    if num==num_int:
        return num_int
    else:
        return float(num)

def pos_rep(pos):

    if pos==0:
        return "unit"

    if pos>0:
        return "1"+"0"*pos

    if pos<0:
        return "0."+"0"*(-pos-1)+"1"

def truncate(num,pos):

    num=float(num)
        
    if pos >= 0:
        try:
            return int(str(num)[:str(num).index(".")-pos-1]) #str(num)
        except:
            return 0

    if pos ==-1:
        return int(str(num)[:str(num).index(".")-pos-1])

    if pos < -1:
        return float(str(num)[:str(num).index(".")-pos])
        

def doublestemandleaf():
    
    st.markdown("Generates a compact and a full double stem and leaf plot for two (reasonably well-behaved) sets of values.")

    data1=st.text_input("Enter all the values from the first data set, separated by commas: ")
    data2=st.text_input("Enter all the values from the second data set, separated by commas: ")

    if data1=="" or data2=="":
        st.stop() 
    
    data1=comprehend(data1)
    data2=comprehend(data2)
    
    data=data1+data2
    stem_pos=stempos(data)

    ml=max([len(str(num)[:str(num).index(".")]) for num in data])

    data_ml=data[0]
    for i in range(len(data)):
        if len(str(data[i])[:str(data[i]).index(".")]) == ml:
            data_ml=data[i]

    data_copy1=data1[:]
    data_copy2=data2[:]
    
    try:
        data1_copy=[int(num) for num in data1]
    except:
        None

    try:
        data2_copy=[int(num) for num in data2]
    except:
        None

    if data_copy1!=data1:
        data_copy=data[:]

    if data_copy1!=data1:
        data_copy=data[:]
    
    st.text("\nYou have entered:")
    st.code(f"\nFirst data set: {[try_int(num) for num in data1]}")
    st.code(f"\nSecond data set: {[try_int(num) for num in data2]}")

    st.text(f"\nThe double stem and leaf plot will represent variation in your data sets at the {pos_rep(stem_pos)}s position and lower, since, at each higher magnitude position, every data value has the same digit.")
    st.text(f"Indeed, truncating each value in your data sets right before the {pos_rep(stem_pos)}s position results in a data set with identical values (and possibly zeros when truncation eats up the entire number):\n")
    st.code([truncate(num,stem_pos) for num in data])

    if len(set([truncate(num,stem_pos) for num in data])-{0})>=2:
        st.text("ERROR: The data set has inconsistent spread or sharp jumps in magnitude - did you forget to exclude outliers? This can happen if removing one or more data points drastically (by orders of magnitude) reduces the overall spread of your data set.")
        return "ERROR: The data set has inconsistent spread or sharp jumps in magnitude - did you forget to exclude outliers? This can happen if removing one or more data points drastically (by orders of magnitude) reduces the overall spread of your data set."
                          
    #st.code("\nNOTE: If above list has more several distinct non-zero values, then the stem-and-leaf plots below will be incorrect! This can happen if you forgot to exclude outliers from your data set.")
    
    if stem_pos==0:
        st.text(f"\nAs such, to reconstruct the data values from the compact double stem and leaf plot, you can simply concatenate (join) \'{truncate(data_ml,stem_pos)}\' (on the left) with any stem-leaf combination (on the right). Remember to add a dot (decimal point) betweem stems and leaves!")
    elif stem_pos==-1:
        st.text(f"\nAs such, to reconstruct the data values from the compact double stem and leaf plot, you can simply concatenate (join) \'{truncate(data_ml,stem_pos)}\' (on the left), \'.\' (decimal point) and any stem-leaf combination (on the right).")
    else:
        st.text(f"\nAs such, to reconstruct the data values from the compact double stem and leaf plot, you can simply concatenate (join) \'{truncate(data_ml,stem_pos)}\' (on the left) with any stem-leaf combination (on the right), except when the number is preceded by an apostrophe ('). In the latter case, the leaf itself is the original number.")

    if stem_pos>=0:
        stem_pos_py=ml - stem_pos-1
    else:
        stem_pos_py=str(data_ml).index(".") - stem_pos
    
    st.markdown(" #### Compact Double Stem and Leaf Plot:")

    stems=sl_range([add_zeros(str(num),ml) for num in data],stem_pos_py)

    if (any([len(str(num)[:str(num).index(".")])!=ml for num in data])==True) and (0 not in stems):
        stems.append(0)
        stems=sorted(stems)

    dict1={}
    dict2={}
    
    for stem in stems:

        leaves1=[add_zeros(str(num),ml)[stem_pos_py+1:] for num in data1 if ((add_zeros(str(num),ml))+"0")[stem_pos_py]==str(stem) and ((((add_zeros(str(num),ml))+"0")[stem_pos_py-1]!="0" and stem_pos_py>0) or stem_pos_py==0  )  ] #and ((add_zeros(str(num),ml))+"0")[stem_pos_py-1]!="0" 
        for i in range(len(leaves1)):
            if leaves1[i]=="":
                leaves1[i]=0

        leaves2=[add_zeros(str(num),ml)[stem_pos_py+1:] for num in data2 if ((add_zeros(str(num),ml))+"0")[stem_pos_py]==str(stem) and ((((add_zeros(str(num),ml))+"0")[stem_pos_py-1]!="0" and stem_pos_py>0) or stem_pos_py==0  )  ] #and ((add_zeros(str(num),ml))+"0")[stem_pos_py-1]!="0" 
        for i in range(len(leaves2)):
            if leaves2[i]=="":
                leaves2[i]=0

        leaves1=sorted([try_int(float(leaf)) for leaf in leaves1])
        leaves2=sorted([try_int(float(leaf)) for leaf in leaves2])

        leaves1=[str(leaf) for leaf in leaves1]
        leaves2=[str(leaf) for leaf in leaves2]

        if len(leaves1)!=0:
            maxlenleaves1=max([len(leaf) for leaf in leaves1])
            for i in range(len(leaves1)):
                if leaves1[i]=="0":
                    while len(leaves1[i]) < maxlenleaves1:
                        leaves1[i]=leaves1[i] + "0"
                else:
                    while len(leaves1[i]) < maxlenleaves1:
                        leaves1[i]="0"+leaves1[i]

        if len(leaves2)!=0:
            maxlenleaves2=max([len(leaf) for leaf in leaves2])
            for i in range(len(leaves2)):
                if leaves2[i]=="0":
                    while len(leaves2[i]) < maxlenleaves2:
                        leaves2[i]=leaves2[i] + "0"
                else:
                    while len(leaves2[i]) < maxlenleaves2:
                        leaves2[i]="0"+leaves2[i]

        if stem==0:
            smallerleaves1=[add_zeros(str(num),ml)[stem_pos_py:] for num in data1 if ((add_zeros(str(num),ml))+"0")[stem_pos_py-1]=="0" and stem_pos_py>0]
            smallerleaves2=[add_zeros(str(num),ml)[stem_pos_py:] for num in data2 if ((add_zeros(str(num),ml))+"0")[stem_pos_py-1]=="0" and stem_pos_py>0]
            if len(smallerleaves1)!=0:
                for i in range(len(smallerleaves1)):
                    if smallerleaves1[i]=="":
                        smallerleaves1[i]=0
                smallerleaves1=sorted([try_int(float(leaf)) for leaf in smallerleaves1])
                smallerleaves1=["'"+str(leaf) for leaf in smallerleaves1]
                leaves1=smallerleaves1+leaves1[:]
            if len(smallerleaves2)!=0:
                for i in range(len(smallerleaves2)):
                    if smallerleaves2[i]=="":
                        smallerleaves2[i]=0
                smallerleaves2=sorted([try_int(float(leaf)) for leaf in smallerleaves2])
                smallerleaves2=["'"+str(leaf) for leaf in smallerleaves2]
                leaves2=smallerleaves2+leaves2[:]
        
        leaves_pretty1=" "
        leaves_pretty2=" "

        dict1[stem]=[]
        dict2[stem]=[]
        
        for leaf in leaves1:
            if stem_pos==0 and leaf!="0" and str(leaf)[0]!="'": 
                dict1[stem].append((str(leaf)[1:])[::-1])
            elif stem_pos==0 and leaf=="0":
                dict1[stem].append(".0"[::-1])
            else:
                dict1[stem].append((str(leaf))[::-1])

        for leaf in leaves2:
            if stem_pos==0 and leaf!="0" and str(leaf)[0]!="'": 
                dict2[stem].append(str(leaf)[1:])
            elif stem_pos==0 and leaf=="0":
                dict2[stem].append(".0")
            else:
                dict2[stem].append(str(leaf))

    allkeys=set(dict1.keys()).union(set(dict2.keys()))

    for key in allkeys:
        if key not in dict1.keys():
            dict1[key]=[""]
        if key not in dict2.keys():
            dict2[key]=[""]

    maxsl=max(len(("  ".join(dict1[key]))) for key in allkeys) #2+

    output=""
    for key in sorted(list(allkeys)):
        leafstring1=("  ".join(dict1[key]))
        leafstring2=("  ".join(dict2[key]))
        pad=maxsl-len(leafstring1)
        output+=((" "*pad) + leafstring1[::-1]+"  |  " + str(key) + "  |  " + leafstring2+"\n\n")
    
    st.code(f"```\n{output}```",language="")
        

    st.text("\nIn the full stem and leaf plot below, the 'L' row, if present, contains data values of magnitudes lower than the ones represented on the remainder of the plot. Their stem L does not contribute any digits, so their original values are precisely their leaf values.")
    st.markdown("*NOTE: When the stems capture variation in the first digit of each value, the compact and full stem and leaf plots are identical.*")


    st.markdown("#### Full Double Stem and Leaf Plot:")

    stems=sl_range([add_zeros(str(num),ml) for num in data],stem_pos_py)

    if (any([len(str(num)[:str(num).index(".")])!=ml for num in data])==True) and (0 not in stems):
        stems.append(0)
        stems=sorted(stems)

    dict1={}
    dict2={}
    
    for stem in stems:

        leaves1=[add_zeros(str(num),ml)[stem_pos_py+1:] for num in data1 if ((add_zeros(str(num),ml))+"0")[stem_pos_py]==str(stem) and ((((add_zeros(str(num),ml))+"0")[stem_pos_py-1]!="0" and stem_pos_py>0) or stem_pos_py==0  )  ] #and ((add_zeros(str(num),ml))+"0")[stem_pos_py-1]!="0" 
        for i in range(len(leaves1)):
            if leaves1[i]=="":
                leaves1[i]=0

        leaves2=[add_zeros(str(num),ml)[stem_pos_py+1:] for num in data2 if ((add_zeros(str(num),ml))+"0")[stem_pos_py]==str(stem) and ((((add_zeros(str(num),ml))+"0")[stem_pos_py-1]!="0" and stem_pos_py>0) or stem_pos_py==0  )  ] #and ((add_zeros(str(num),ml))+"0")[stem_pos_py-1]!="0" 
        for i in range(len(leaves2)):
            if leaves2[i]=="":
                leaves2[i]=0

        leaves1=sorted([try_int(float(leaf)) for leaf in leaves1])
        leaves2=sorted([try_int(float(leaf)) for leaf in leaves2])

        leaves1=[str(leaf) for leaf in leaves1]
        leaves2=[str(leaf) for leaf in leaves2]

        if len(leaves1)!=0:
            maxlenleaves1=max([len(leaf) for leaf in leaves1])
            for i in range(len(leaves1)):
                if leaves1[i]=="0":
                    while len(leaves1[i]) < maxlenleaves1:
                        leaves1[i]=leaves1[i] + "0"
                else:
                    while len(leaves1[i]) < maxlenleaves1:
                        leaves1[i]="0"+leaves1[i]

        if len(leaves2)!=0:
            maxlenleaves2=max([len(leaf) for leaf in leaves2])
            for i in range(len(leaves2)):
                if leaves2[i]=="0":
                    while len(leaves2[i]) < maxlenleaves2:
                        leaves2[i]=leaves2[i] + "0"
                else:
                    while len(leaves2[i]) < maxlenleaves2:
                        leaves2[i]="0"+leaves2[i]

        if stem==0:
            smallerleaves1=[add_zeros(str(num),ml)[stem_pos_py:] for num in data1 if ((add_zeros(str(num),ml))+"0")[stem_pos_py-1]=="0" and stem_pos_py>0]
            smallerleaves2=[add_zeros(str(num),ml)[stem_pos_py:] for num in data2 if ((add_zeros(str(num),ml))+"0")[stem_pos_py-1]=="0" and stem_pos_py>0]
            sml1=[]
            sml2=[]
            if len(smallerleaves1)!=0:
                for i in range(len(smallerleaves1)):
                    if smallerleaves1[i]=="":
                        smallerleaves1[i]=0
                smallerleaves1=sorted([try_int(float(leaf)) for leaf in smallerleaves1])
                smallerleaves1_copy=[str(leaf) for leaf in smallerleaves1]
                smallerleaves1=["'"+str(leaf) for leaf in smallerleaves1]
                #leaves1=smallerleaves1+leaves[:]

                for leaf in smallerleaves1_copy:
                    if stem_pos==0 and leaf!="0" and str(leaf)[0]!="'": 
                        sml1.append((str(leaf)[1:])[::-1])
                    elif stem_pos==0 and leaf=="0":
                        sml1.append(".0"[::-1])
                    else:
                        sml1.append((str(leaf))[::-1])
                
            if len(smallerleaves2)!=0:
                for i in range(len(smallerleaves2)):
                    if smallerleaves2[i]=="":
                        smallerleaves2[i]=0
                smallerleaves2=sorted([try_int(float(leaf)) for leaf in smallerleaves2])
                smallerleaves2_copy=[str(leaf) for leaf in smallerleaves2]
                smallerleaves2=["'"+str(leaf) for leaf in smallerleaves2]
                #leaves2=smallerleaves2+leaves[:]
                
                for leaf in smallerleaves2_copy:
                    if stem_pos==0 and leaf!="0" and str(leaf)[0]!="'": 
                        sml2.append(str(leaf)[1:])
                    elif stem_pos==0 and leaf=="0":
                        sml2.append(".0")
                    else:
                        sml2.append(str(leaf))
            
        
        dict1[stem]=[]
        dict2[stem]=[]
        
        for leaf in leaves1:
            if stem_pos==0 and leaf!="0" and str(leaf)[0]!="'": 
                dict1[stem].append((str(leaf)[1:])[::-1])
            elif stem_pos==0 and leaf=="0":
                dict1[stem].append(".0"[::-1])
            else:
                dict1[stem].append((str(leaf))[::-1])

        for leaf in leaves2:
            if stem_pos==0 and leaf!="0" and str(leaf)[0]!="'": 
                dict2[stem].append(str(leaf)[1:])
            elif stem_pos==0 and leaf=="0":
                dict2[stem].append(".0")
            else:
                dict2[stem].append(str(leaf))

    allkeys=set(dict1.keys()).union(set(dict2.keys()))

    for key in allkeys:
        if key not in dict1.keys():
            dict1[key]=[""]
        if key not in dict2.keys():
            dict2[key]=[""]

    if 0 in stems:
        maxsl=max(max(len(("  ".join(dict1[key]))) for key in allkeys),len("  ".join(sml1))) #2+
    else:
        maxsl=max(len(("  ".join(dict1[key]))) for key in allkeys)
        
    output=""
    
    if (0 in stems) and (len(smallerleaves1)!=0 or len(smallerleaves2)!=0):

        if stem_pos==-1:
            fullkey=str(truncate(data_ml,stem_pos))+"."+str(key)
        elif truncate(data_ml,stem_pos)!=0:
            fullkey=str(truncate(data_ml,stem_pos))+str(key)
        else:
            fullkey=str(key)

        Lpad=len(fullkey)

        leafstring1=("  ".join(sml1))
        leafstring2=("  ".join(sml2))
        pad=maxsl-len(leafstring1)
        output+=("  "+(" "*pad) + leafstring1[::-1]+"  |  " + "L"+ " "*(Lpad-1) + "  |  " + leafstring2+"\n\n")
        
    for key in sorted(list(allkeys)):
        
        if stem_pos==-1:
            fullkey=str(truncate(data_ml,stem_pos))+"."+str(key)
        elif truncate(data_ml,stem_pos)!=0:
            fullkey=str(truncate(data_ml,stem_pos))+str(key)
        else:
            fullkey=str(key)
            
        leafstring1=("  ".join(dict1[key])) #[::-1]
        leafstring2=("  ".join(dict2[key]))
        pad=maxsl-len(leafstring1)
        output+=("  "+(" "*pad) + leafstring1[::-1]+"  |  " + fullkey + "  |  " + leafstring2+"\n\n")

    st.code(f"```\n{output}```",language="")

    st.text("")
    st.markdown("""*Crafted by yarov3so*   
<a href="https://www.buymeacoffee.com/yarov3so" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="width: 9em; height: auto; padding-top: 0.7em; padding-bottom: 1em" ></a>  
See my other [Math Help Tools](https://mathh3lptools.streamlit.app)""",unsafe_allow_html=True)

    return None


doublestemandleaf()
