#Kevin Rodriguez
import numpy as np
#a.)
# 2-gray level Encoder for 2D NumPy array with pixel values
def encoder(data):
    height, width = data.shape
    #print(width)
    encoded_data =  np.zeros((height, width), np.int32)
    for i in range(height):
        for j in range(width):
            if data[i][j]>127:
                encoded_data[i][j] = 1
            
    return encoded_data
#b.)
# 2-gray level decoder for 2D NumPy array
def decoder(data):
    height, width = data.shape
    
    decoded_data = np.zeros((height, width), np.int32)
    for i in range(height):
        for j in range(width):
            if data[i][j]==0:
                decoded_data[i][j] = 63
            else:
                decoded_data[i][j] = 191
    return decoded_data
            
#read file
def readpgm(name):
    
    with open(name) as f:
        lines = f.readlines()

    # Ignores commented lines
    for l in list(lines):
        if l[0] == '#':
            lines.remove(l)

    # Makes sure it is ASCII format (P2)
    #print('first',lines[0])
    assert lines[0].strip() == 'P2' 
    
    #read # baboon.pgma created by PGMA_IO::PGMA_WRITE.
    #512  512
    #255
    index = 1
    if lines[0][0] == '#':
        index += 1
    width = int(lines[index].split()[0])
    height = int(lines[index].split()[0])
    index += 1
    maxval = int(lines[index])
    index += 1

    image = []
    # Converts data to a list of integers
    for line in lines[index:]:
        image.extend([int(c) for c in line.split()])
        
    #
    # Initialise a 2D numpy array 
    #
    data = np.zeros((height, width), np.int32)
    for r in range(height):
        for c in range(width):
            data[r, c] = image[r*width + c]
    return [width, height, data]

def write_pgma(filename, comment, data, maxval):
    height, width = data.shape
    
    #Writing the headers of a pgma file
    #P2
    #512  512
    #255
    filetype = "P2"
    f_handle = open(filename,'w')
    f_handle.write(filetype+'\n')
    f_handle.write(comment+'\n')
    f_handle.write(str(height)+' '+str(width)+'\n')
    f_handle.write(str(maxval)+'\n')
    
    #Writing the data to the file
    for i in range(height):
        for j in range(width):
            f_handle.write(str(data[i][j]) + ' ')
        f_handle.write('\n')
    
#c.)
#calculating distortion mean square error   
def distortion(original_data, reconstructed_data):
    square_sum = 0
    height, width = original_data.shape 
    for i in range(height):
        for j in range(width):
            difference = original_data[i][j] - reconstructed_data[i][j]
            #print(difference)
            sq_diff = difference ** 2
            #print(sq_diff)
            square_sum += sq_diff
    
    mean_square_error = square_sum / (height*width)
    return mean_square_error

#d.)

#producing an error image
def produce_error_image(original_data, reconstructed_data):
    height, width = original_data.shape
    maxval = -9999
    error_data = np.zeros((height,width),np.int32)
    for i in range(height):
        for j in range(width):
            #if(original_data[i][j]>255):
            #    print("error in original_data")
            error_data[i][j] = abs(original_data[i][j] - reconstructed_data[i][j])
            if error_data[i][j] == 247:
                print("error value present i:"+str(i)+" j: "+str(j))
                print(reconstructed_data[i][j])
                print(original_data[i][j])
            if error_data[i][j] > maxval:
                maxval = error_data[i][j]

    print("Maxval is : "+ str(maxval))
    return error_data, maxval


#1st part
#Encoder for 15 level
def encoder_15_gray_level(data):
    height, width = data.shape
    encoded_data = np.zeros((height, width),np.int32)
    
    for row in range(height):
        for col in range(width):
            start = 0
            end = 16
            for i in range(17):
                if (data[row][col] >= start and data[row][col] <= end):
                    encoded_data[row][col] = (data[row][col]/17)
                if (data[row][col]==255):
                    encoded_data[row][col] = 14
                if i==0: 
                    start += 17
                else:
                    start += 16
                end += 16

    return encoded_data

#Decoder for 15 level
def decoder_15_level(data):
    height, width = data.shape
    decoded_data = np.zeros((height,width),np.int32)
    for row in range(height):
        for col in range(width):
            start = 0
            end = 16
            for i in range(15):
                if (data[row][col] == i):
                    decoded_data[row][col] = (i+1) * 8

    return decoded_data               


#main function
def main():

#First part encoding 15-gray level
#a.)
    [width, height, original_data] = readpgm("baboon.pgma")
    encoded_15_level = encoder_15_gray_level(original_data)
    print("Pixel value in 15 level encoded data:")
    print(encoded_15_level)
    print()
    #Writing the the encoded file to pgma with maxval
    write_pgma('baboon_encoded_15_level.pgma', '# Created by PGMA_WRITE',encoded_15_level,14)
#b.)
    decoded_15_level = decoder_15_level(encoded_15_level)
    print("Pixel value in decoded 15 level data:")
    print(decoded_15_level)
    print()
    
    write_pgma('baboon_decoded_15_level.pgma', '# Created by PGMA_WRITE',decoded_15_level,15*8)
#c.)
    mse_15_level = distortion(original_data, decoded_15_level)
    print("Distortion for the reconstructed image is (MSE): " + str(mse_15_level))
#d.)
    print()
    error_data_15_level, maxval_15_level = produce_error_image(original_data,decoded_15_level)
    print("Pixel value in error data:")
    print(error_data_15_level)
    #print(maxval_15_level)
    #Write the error data into pgma file
    write_pgma('baboon_error_15_level_image.pgma','# Created by PGMA WRITE', error_data_15_level,maxval_15_level)

#Second part 2-gray level    
#a.)    
    #read and process
    [width, height, original_data] = readpgm("baboon.pgma")
    print("Pixel value in original data:")
    print(original_data)
    print()
    #Encoding the pgma file : 2-gray levels
    encoded_data = encoder(original_data)
    print("Pixel value in encoded data:")
    print(encoded_data)
    print()
    
 #b.)   
    #Writing the the encoded file to pgma with maxval
    write_pgma('baboon_encoded_2_level.pgma', '# Created by PGMA_WRITE',encoded_data,1)
    
    #Decoding the pgma file
    [width, height, encoded_data] = readpgm("baboon_encoded_2_level.pgma")
    decoded_data = decoder(encoded_data)
    print("Pixel value in reconstructed data:")
    print(decoded_data)
    print()
    
    #Write decode data into a pgma file
    write_pgma('baboon_decoded_2_level.pgma', '# Created by PGMA_WRITE',decoded_data,191)
    
#c.)
    mse = distortion(original_data, decoded_data)
    print("Distortion for the reconstructed image is (MSE): " + str(mse))
#d.)
    print()
    error_data, maxval = produce_error_image(original_data,decoded_data)
    print("Pixel value in error data:")
    print(error_data)
    #print(maxval)
    #Write the error data into pgma file
    write_pgma('baboon_error_image.pgma','# Created by PGMA WRITE', error_data,maxval)

    
    
    
if __name__ == "__main__":
    main()
