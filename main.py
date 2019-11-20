import imageio
import matplotlib.pyplot as plt
import decimal

pic = imageio.imread('/Users/playment/Parth /Codes/data/frame190.jpg')
pic1 = imageio.imread('/Users/playment/Parth /Codes/data/frame2.jpg')
height = int(format(pic.shape[0]))
width = int(format(pic.shape[1]))
tcount = height * width

change = []
rdiff = decimal.Decimal(0)
gdiff = decimal.Decimal(0)
bdiff = decimal.Decimal(0)

for i in range(pic.shape[0]):
    for j in range(pic.shape[1]):
        #RGB values of fist frame:
        R1 = int(format(pic[i,j,0]))
        G1 = int(format(pic[i,j,1]))
        B1 = int(format(pic[i,j,2]))

        #RGB values of second frame:
        R2 = int(format(pic1[i,j,0]))
        G2 = int(format(pic1[i,j,1]))
        B2 = int(format(pic1[i,j,2]))
        rdiff += abs(R2 - R1) / decimal.Decimal('255')
        gdiff += abs(G2 - G1) / decimal.Decimal('255')
        bdiff += abs(B2 - B1) / decimal.Decimal('255')


#average values of each channel:
rdiff =  rdiff / decimal.Decimal(tcount)
gdiff =  gdiff / decimal.Decimal(tcount)
bdiff =  bdiff / decimal.Decimal(tcount)

change.append(float(rdiff + gdiff + bdiff) / 3)




print(change)
