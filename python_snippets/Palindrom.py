class Manacher:
    def __init__(self,string:str,extra_char = "$*^"):
        self.str = string
        beg,comb,end = extra_char
        self._modified = beg+comb + comb.join(i for i in string) +comb+end
        self.raidus_arr = [0]*len(self._modified)
        self._max_pal =  None 
        self.calculate()

    
    def calculate(self):
        # the radius is the largest number r such that for a given index i, 
        # substring [i-r,i+r] is a palindrome (the endpoints are inclusive)
        center = 1 # starting center
        end = center + 0 # the starting radius is assumed to be zero therfore the end of the center is center+radius
        for index in range(1,len(self._modified)-1):
            # reflection = center -(distance to i from center)
            # reflection = center - (i - center) = 2*center -i
            reflection = 2*center -index
            self.raidus_arr[index] = max( # setting the radius of the current index to the maximum value given the current information
                0, # to prevent negaative values because we are out of range of the end 
                min(
                    # since the center represents a palindrome the current index will have a radius
                    # equal to the reflection as long as that is within the radius of the center
                    # however if that is not the case i.e. radius_of_relfection +i > end
                    # then the radius will only go upto end of the current center
                    self.raidus_arr[reflection], 
                    end -index
                )
            )

            #now check all the surrounding characters from our current radius and if it better increase the radius
            while(
                self._modified[index-self.raidus_arr[index]-1] == self._modified[index+self.raidus_arr[index]+1]
                ):
                self.raidus_arr[index] +=1

            # if the end that can be caluclated from the current index is better than the previous one then we can use that in
            # the next iterations
            if(index+self.raidus_arr[index] >end):
                center = index
                end = index+self.raidus_arr[index]
    def calculate_max_pal(self):
        '''
        returns the one indexed indices of the maximum palindrome
        '''
        if(self._max_pal is None):
            max_radius,max_middle = max((radius,index) for (index,radius) in enumerate(self.raidus_arr))
            self._max_pal =  (max_middle -max_radius+1)//2,(max_middle+max_radius-1)//2
        return self._max_pal
        

    def max_centerd_at_range_one_indexed(self,start,end):
        '''
        returns the length and the start and end (inclusive range) of the palindrome centerd at the given range (one indexed)
        '''
        if(start >end):
            return 0,None
        start,end = start*2 ,2*end
        middle = (start+end) //2 
        
        pals,pale = middle -self.raidus_arr[middle],middle+self.raidus_arr[middle]

        # the inices will be that of stars to get the actual letter we add one for the first and substract one from the last. 
        pals,pale = (pals+1)//2,(pale-1)//2 
        length = pale - pals +1
        if(length == 0):
            return 0,None
        return length, (pals,pale)
    
    def is_pal(self,start,end):
        if(start >end): return False
        l,_ =  self.max_centerd_at_range_one_indexed(start,end)
        return l >= (end - start+1)
        

            
            

