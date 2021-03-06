import argparse
import math
# Created by Arya Kaul - 1/12/2017
# Modified by Ferhat Ay - 1/13/2017

def outputfithicform(bedPath, matrixPath, intCPath, fragMapPath, biasVectorPath=None, biasVectorOutput=None):
    print "Loading matrix file..."
    fragDic = {}
    res=0 # resolution of data to be determined
    with open(bedPath, 'r') as bedFile:
        for lines in bedFile:
            line = lines.rstrip().split()
            chrNum = line[0]
            start = line[1]
            en = line[2]
            if res==0: res=int(en)-int(start)
            mid = int(start)+ int(res/2)
            index = int(line[3])
            fragDic[index] = [chrNum, start, mid, 0] # last field is total contact count: tcc

    lineCount=0
    with open(matrixPath, 'r') as matrixFile:
        with open(intCPath, 'w') as interactionCountsFile:
            for lines in matrixFile:
                line = lines.rstrip().split()
                i = int(line[0])
                j = int(line[1])
                cc = float(line[2]) # this can be float or int
                fragDic[i][3] += cc
                fragDic[j][3] += cc
                interactionCountsFile.write(str(fragDic[i][0])+'\t'+str(fragDic[i][2])+'\t'+str(fragDic[j][0])+'\t'+str(fragDic[j][2])+'\t'+str(cc)+"\n")
                lineCount+=1
                if lineCount%1000000==0: print "%d million lines read" % int(lineCount/1000000)

    with open(fragMapPath, 'w') as fragmentMappabilityFile:
        for indices in sorted(fragDic): # sorted so that we start with the smallest index
            toWrite = 0
            if fragDic[indices][3]> 0: toWrite=1 
            fragmentMappabilityFile.write(str(fragDic[indices][0])+'\t'+str(fragDic[indices][1])+'\t'+str(fragDic[indices][2])+'\t'+str(fragDic[indices][3])+'\t'+str(toWrite)+'\n')

    if biasVectorPath is not None and biasVectorOutput is not None:
        print "Converting bias file..."

        biasVec=[0,0] # bias sum and biasCount
        biasDic={} # bias for each index
	i=1 # one-based indices
        with open(biasVectorPath, 'r') as biasVectorFile:
                for lines in biasVectorFile:
                    value = float(lines.rstrip()) #just one entry that can be nan or a float
                    index = int(i)
                    i+=1
                    biasDic[index]=value
                    if not math.isnan(value):
                        biasVec[0]+=value #sum
                        biasVec[1]+=1 # count
	#

        # Centering the bias values on 1.
        biasAvg=biasVec[0]/biasVec[1]

        with open(biasVectorOutput, 'w') as biasVectorOutputFile:
            for index in sorted(biasDic):
                value=biasDic[index]
                if not math.isnan(value):
                    value=value/biasAvg
                else: 
                    value=-1
                biasVectorOutputFile.write(str(fragDic[index][0])+'\t'+str(fragDic[index][2])+'\t'+str(value)+'\n')
    print "Conversion from HiC-Pro to Fit-Hi-C format completed"

#outputfithicform(args.bedPath, args.matrixPath, args.intCPath, args.fragMapPath, args.biasVectorPathandOutput[0], args.biasVectorPathandOutput[1])

def main():
    # Example without bias files
    outputfithicform('raw/1000000/hIMR90_HindIII_r1_1000000_abs.bed', 'raw/1000000/hIMR90_HindIII_r1_1000000.matrix', 'fithic.interactionCounts', 'fithic.fragmentMappability')
    # Example with bias files
    outputfithicform('raw/1000000/hIMR90_HindIII_r1_1000000_abs.bed', 'raw/1000000/hIMR90_HindIII_r1_1000000.matrix', 'fithic.interactionCounts', 'fithic.fragmentMappability','hicpro.biases','fithic.biases')

if __name__=="__main__":
    main()
